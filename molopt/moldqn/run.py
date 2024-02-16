import os, torch
import numpy as np 
import sys
path_here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path_here)
# sys.path.append('.')
from molopt.base import BaseOptimizer
from molopt.moldqn.agents.agent import DQN 

class MolDQN(BaseOptimizer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = "moldqn"

    def _optimize(self, oracle, config):

        ## set default value 
        if 'max_steps_per_episode' not in config:
            config['max_steps_per_episode'] = 40
        if 'init_mol' not in config:
            config['init_mol'] = 'C'
        if 'fingerprint_radius' not in config:
            config['fingerprint_radius'] = 2
        if 'fingerprint_length' not in config:
            config['fingerprint_length'] = 1024
        if 'discount_factor' not in config:
            config['discount_factor'] = 0.9
        if 'num_episodes' not in config:
            config['num_episodes'] = 200000
        if 'replay_buffer_size' not in config:
            config['replay_buffer_size'] = 500
        if 'batch_size' not in config:
            config['batch_size'] = 32
        if 'gamma' not in config:
            config['gamma'] = 1.0
        if 'update_frequency' not in config:
            config['update_frequency'] = 3
        if 'num_bootstrap_heads' not in config:
            config['num_bootstrap_heads'] = 6
        if 'prioritized_alpha' not in config:
            config['prioritized_alpha'] = 0.6
        if 'prioritized_beta' not in config:
            config['prioritized_beta'] = 0.4
        if 'prioritized_epsilon' not in config:
            config['prioritized_epsilon'] = 0.000001
        if 'save_frequency' not in config:
            config['save_frequency'] = 200
        if 'max_num_checkpoints' not in config:
            config['max_num_checkpoints'] = 10
        if 'distribution' not in config:
            config['distribution'] = False
        if 'noisy' not in config:
            config['noisy'] = True
        if 'n_layers' not in config:
            config['n_layers'] = 1
        if 'n_neurons' not in config:
            config['n_neurons'] = 512
        if 'activation' not in config:
            config['activation'] = 'ReLU'
        if 'optimizer' not in config:
            config['optimizer'] = 'Adam'
        if 'dropout' not in config:
            config['dropout'] = 0
        if 'learning_frequency' not in config:
            config['learning_frequency'] = 4
        if 'learning_rate' not in config:
            config['learning_rate']= 0.0001
        if 'learning_rate_decay_steps' not in config:
            config['learning_rate_decay_steps'] = 10000
        if 'learning_rate_decay_rate' not in config:
            config['learning_rate_decay_rate'] = 0.9
        if 'adam_beta_1' not in config:
            config['adam_beta_1'] = 0.9
        if 'adam_beta_2' not in config:
            config['adam_beta_2'] = 0.999
        if 'grad_clipping' not in config:
            config['grad_clipping'] = 10


        self.oracle.assign_evaluator(oracle)

        agent = DQN(
            oracle=self.oracle,
            q_fn = 'mlp', 
            n_max_oracle_call=self.max_oracle_calls,
            args=config,
        )

        print('Print Q function architecture:')
        print(agent.q_fn)

        global_step = 0

        for episode in range(agent.num_episodes):

            epsilon = agent.exploration.value(len(self.oracle))
            # print(f"Episode: {episode}, epsilon: {epsilon}")

            _, _ = agent.env.reset()
            head = np.random.randint(agent.num_bootstrap_heads)

            for step in range(agent.max_steps_per_episode):

                state_mol, reward, done = agent._step(epsilon=epsilon, head=head)

                # Training the network
                start_train = 50 # if self.args.noisy else 50
                if (episode > min(start_train, agent.num_episodes / 10)) and (global_step % agent.learning_frequency == 0):

                    # Update learning rate
                    if (global_step % agent.learning_rate_decay_steps == 0) and (agent.lr_schedule is not None):
                        agent.lr_schedule.step()

                    # Compute td error and optimize the network
                    td_error = agent._compute_td_loss(agent.batch_size, episode)

                    # Update the target network
                    if agent.double and (episode % agent.update_frequency == 0):
                        agent.q_fn_target.load_state_dict(agent.q_fn.state_dict())

                global_step += 1
        
            # Save checkpoint
            if episode % agent.save_frequency == 0:
                model_name = 'dqn_checkpoint_' + str(episode) + '.pth'
                torch.save(agent.q_fn.state_dict(), os.path.join(agent.log_path, model_name))

            if self.finish:
                print('max oracle hit... abort!')
                break