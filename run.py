# import argparse, yaml, os 
# def generate_args():
#     parser = argparse.ArgumentParser()
#     # parser.add_argument('method', default='graph_ga')
#     parser.add_argument('--smi_file', default=None)
#     parser.add_argument('--config_default', default='hparams_default.yaml')
#     parser.add_argument('--config_tune', default='hparams_tune.yaml')
#     parser.add_argument('--pickle_directory', help='Directory containing pickle files with the distribution statistics', default=None)
#     parser.add_argument('--n_jobs', type=int, default=-1)
#     parser.add_argument('--output_dir', type=str, default='results')
#     parser.add_argument('--patience', type=int, default=5)
#     parser.add_argument('--max_oracle_calls', type=int, default=10000)
#     parser.add_argument('--freq_log', type=int, default=100)
#     parser.add_argument('--n_runs', type=int, default=5)
#     parser.add_argument('--seed', type=int, nargs="+", default=[0])
#     parser.add_argument('--task', type=str, default="simple", choices=["tune", "simple", "production"])
#     parser.add_argument('--oracles', nargs="+", default=["QED"]) ### 
#     parser.add_argument('--log_results', action='store_true')
#     parser.add_argument('--log_code', action='store_true')
#     parser.add_argument('--wandb', type=str, default="disabled", choices=["online", "offline", "disabled"])
#     args = parser.parse_args()
#     return args 

# args = generate_args() 
# config_default = yaml.safe_load(open(args.config_default))
# seed = args.seed[0] 

# os.environ["WANDB_MODE"] = args.wandb
# if not args.log_code:
#     os.environ["WANDB_DISABLE_CODE"] = "false"

# if args.output_dir is None:
#     args.output_dir = os.path.join(path_main, "results")

# if not os.path.exists(args.output_dir):
#     os.mkdir(args.output_dir)

# path_main = os.path.dirname(os.path.realpath(__file__))
# # path_main = os.path.join(path_main, "main", args.method)

# if args.pickle_directory is None:
#     args.pickle_directory = path_main

from molopt import GraphGA
optimizer = GraphGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
optimizer.optimize(oracle='qed', config='hparams_default.yaml', patience=5, seed=0)



'''

from molopt import GraphGA
optimizer = GraphGA(n_jobs = -1) 
optimizer.optimize(oracle='qed', max_oracle_calls=10000, patience=5, config='hparams_default.yaml', output_dir='results')
or 
optimizer.hparam_tune(oracle='qed', max_oracle_calls=10000, patience=5, config='hparam_tune.yaml', output_dir='results')


'''



