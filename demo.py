# print('-- graph ga -- ')
# from molopt.graph_ga import GraphGA
# optimizer = GraphGA(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)

# print('-- screening -- ')
# from molopt.screening import Screening
# optimizer = Screening(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)

# print('-- smiles ga -- ')
# from molopt.smiles_ga import SmilesGA
# optimizer = SmilesGA(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)

# print('-- stoned -- ')
# from molopt.stoned import Stoned
# optimizer = Stoned(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)


# print('-- graph mcts -- ')
# from molopt.graph_mcts import Graph_MCTS
# optimizer = Graph_MCTS(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)


# print('-- moldqn -- ')
# from molopt.moldqn import MolDQN
# optimizer = MolDQN(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)

# print('-- gpbo -- ')
# from molopt.gpbo import GPBO
# optimizer = GPBO(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)


# print('-- reinvent --')  
# from molopt.reinvent import REINVENT
# optimizer = REINVENT(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)


# print('-- reinvent_selfies --') 
# from molopt.reinvent_selfies import REINVENT_SELFIES
# optimizer = REINVENT_SELFIES(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)


# print('-- mimosa --')  
# from molopt.mimosa import MIMOSA
# optimizer = MIMOSA(smi_file=None, n_jobs=-1, max_oracle_calls=5000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)


# print('SmilesVAE') ## bug 
# from molopt.smiles_vae import SmilesVAE
# optimizer = SmilesVAE(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/smiles_vae/hparams_default.yaml', patience=5, seed=0)


# print('-- selfies ga --') ## bug  
# from molopt.selfies_ga import SelfiesGA
# optimizer = SelfiesGA(smi_file=None, n_jobs=-1, max_oracle_calls=1000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', patience=5, seed=0)




# ### need cuda 
print('-- jt_vae --')
from molopt.jt_vae import JTVAE
optimizer = JTVAE(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/project/molecular_data/graphnn/mol-opt/molopt/jt_vae/hparams_default.yaml', patience=5, seed=0)
optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/jt_vae/hparams_default.yaml', patience=5, seed=0)












