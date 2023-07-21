# from molopt import GraphGA
# optimizer = GraphGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='molopt/graph_ga/hparams_default.yaml', patience=5, seed=0)


# from molopt import Screening
# optimizer = Screening(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/screening/hparams_default.yaml', patience=5, seed=0)



# from molopt import SmilesGA
# optimizer = SmilesGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
# optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/smiles_ga/hparams_default.yaml', patience=5, seed=0)


from molopt import SelfiesGA
optimizer = SelfiesGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
optimizer.optimize(oracle='qed', config='/Users/tianfanfu/Downloads/mol-opt/molopt/selfies_ga/hparams_default.yaml', patience=5, seed=0)

