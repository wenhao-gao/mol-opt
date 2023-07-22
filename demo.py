# from molopt import GraphGA
# optimizer = GraphGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='molopt/graph_ga/hparams_default.yaml', patience=5, seed=0)


# from molopt import Screening
# optimizer = Screening(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/screening/hparams_default.yaml', patience=5, seed=0)


# from molopt import SmilesGA
# optimizer = SmilesGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/smiles_ga/hparams_default.yaml', patience=5, seed=0)


# from molopt import SelfiesGA
# optimizer = SelfiesGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/selfies_ga/hparams_default.yaml', patience=5, seed=0)

# from molopt import Stoned
# optimizer = Stoned(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/stoned/hparams_default.yaml', patience=5, seed=0)


# from molopt import Graph_MCTS
# optimizer = Graph_MCTS(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/graph_mcts/hparams_default.yaml', patience=5, seed=0)


# from molopt import MIMOSA
# optimizer = MIMOSA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/mimosa/hparams_default.yaml', patience=5, seed=0)


# from molopt import REINVENT
# optimizer = REINVENT(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/reinvent/hparams_default.yaml', patience=5, seed=0)


# from molopt import REINVENT_SELFIES
# optimizer = REINVENT_SELFIES(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/reinvent_selfies/hparams_default.yaml', patience=5, seed=0)


# from molopt import MolDQN
# optimizer = MolDQN(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/moldqn/hparams_default.yaml', patience=5, seed=0)


# from molopt import GPBO
# optimizer = GPBO(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/gpbo/hparams_default.yaml', patience=5, seed=0)


# from molopt import SmilesVAE
# optimizer = SmilesVAE(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/smiles_vae/hparams_default.yaml', patience=5, seed=0)



# ### need cuda 
from molopt import JTVAE
optimizer = JTVAE(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/project/molecular_data/graphnn/mol-opt/molopt/jt_vae/hparams_default.yaml', patience=5, seed=0)
optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/jt_vae/hparams_default.yaml', patience=5, seed=0)


