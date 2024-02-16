import os, time
import sys
path_here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path_here)
sys.path.append('.')
from selfies import decoder, encoder 
import multiprocessing
import torch
# import evolution_functions as evo
# import generation_props as gen_func
from ..base import BaseOptimizer 
from .discriminator import obtain_initial_discriminator, do_x_training_steps, save_model
from .generation_props import obtain_previous_gen_mol, obtain_fitness, apply_generation_cutoff, obtain_next_gen_molecules, \
  update_gen_res, obtain_discrm_data
from .evolution_functions import make_clean_results_dir, make_clean_directories, sanitize_multiple_smiles, read_dataset_encoding

class SelfiesGA(BaseOptimizer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = "selfies_ga"

    def _optimize(self, oracle, config):
        ## set default value 
        if 'generation_size' not in config:
            config['generation_size'] = 300
        if 'patience' not in config:
            config['patience'] = 5
        if 'beta' not in config:
            config['beta'] = 0
        if 'max_generations' not in config:
            config['max_generations'] = 1000

        self.oracle.assign_evaluator(oracle)

        beta = config['beta']
        max_generations = config['max_generations'] ## 1000
        generation_size = config['generation_size'] ##  500

        results_dir = make_clean_results_dir()
        i = 0 
        max_fitness_collector = []
        image_dir, saved_models_dir, data_dir = make_clean_directories(beta, results_dir, i) # clear directories 

        torch.cuda.empty_cache()

        starting_selfies = [encoder('C')]
        max_molecules_len = 81
        disc_epochs_per_generation = 10
        disc_enc_type = 'properties_rdkit'    # 'selfies' or 'smiles' or 'properties_rdkit'
        disc_layers = [100, 10]
        training_start_gen = 0   # generation index to start training discriminator
        device = 'cpu'
        num_processors = multiprocessing.cpu_count()
        impose_time_adapted_pen = True

        # Obtain starting molecule
        starting_smiles = sanitize_multiple_smiles([decoder(selfie) for selfie in starting_selfies])
        
        # Recording Collective results
        smiles_all         = []    # all SMILES seen in all generations
        selfies_all        = []    # all SELFIES seen in all generation
        smiles_all_counter = {}    # Number of times a SMILE string is recorded in GA run
        
        # Initialize a Discriminator
        discriminator, d_optimizer, d_loss_func = obtain_initial_discriminator(disc_enc_type, disc_layers, max_molecules_len, device)
        
        # Read in the Zinc data set 
        molecules_reference = read_dataset_encoding(disc_enc_type)
        molecules_reference = dict.fromkeys(molecules_reference, '') # convert the zinc data set into a dictionary

        # Set up Generation Loop 
        total_time = time.time()
        for generation_index in range(1, max_generations+1):
            # print("   ###   On generation %i of %i"%(generation_index, max_generations))
                  
            # Obtain molecules from the previous generation 
            smiles_here, selfies_here = obtain_previous_gen_mol(starting_smiles,   
                                                                         starting_selfies, 
                                                                         generation_size, 
                                                                         generation_index,  
                                                                         selfies_all,      
                                                                         smiles_all)

            # Calculate fitness of previous generation (shape: (generation_size, ))
            value = self.oracle(smiles_here)
            fitness_here, order, fitness_ordered, smiles_ordered, selfies_ordered = obtain_fitness(
                                                                                        disc_enc_type,      
                                                                                        smiles_here,   
                                                                                        selfies_here,  
                                                                                        self.oracle,    
                                                                                        discriminator, 
                                                                                        generation_index,
                                                                                        max_molecules_len,  
                                                                                        device,        
                                                                                        generation_size,  
                                                                                        num_processors,     
                                                                                        beta,            
                                                                                        image_dir,          
                                                                                        data_dir,      
                                                                                        max_fitness_collector, 
                                                                                        impose_time_adapted_pen)

            if self.finish:
                break 

            # Obtain molecules that need to be replaced & kept
            to_replace, to_keep = apply_generation_cutoff(order, generation_size)
            # Obtain new generation of molecules 
            smiles_mutated, selfies_mutated = obtain_next_gen_molecules(order,
                                                                                to_replace,     
                                                                                to_keep, 
                                                                                selfies_ordered, 
                                                                                smiles_ordered, 
                                                                                max_molecules_len)
            # Record in collective list of molecules 
            smiles_all, selfies_all, smiles_all_counter = update_gen_res(smiles_all, 
                                                                                  smiles_mutated, 
                                                                                  selfies_all, 
                                                                                  selfies_mutated, 
                                                                                  smiles_all_counter)


            # Obtain data for training the discriminator (Note: data is shuffled)
            dataset_x, dataset_y = obtain_discrm_data(disc_enc_type, 
                                                               molecules_reference, 
                                                               smiles_mutated, 
                                                               selfies_mutated, 
                                                               max_molecules_len, 
                                                               num_processors, 
                                                               generation_index)
            # Train the discriminator (on mutated molecules)
            if generation_index >= training_start_gen:
                discriminator = do_x_training_steps(dataset_x, 
                                                      dataset_y, 
                                                      discriminator, 
                                                      d_optimizer, 
                                                      d_loss_func , 
                                                      disc_epochs_per_generation, 
                                                      generation_index-1, 
                                                      device, 
                                                      data_dir)
                save_model(discriminator, generation_index-1, saved_models_dir) # Save the discriminator 



