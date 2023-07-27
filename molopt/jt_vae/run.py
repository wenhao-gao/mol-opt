import os, torch
import sys
path_here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path_here)
sys.path.append('.')
from ..base import BaseOptimizer

from tdc.chem_utils.oracle.oracle import smiles_to_rdkit_mol
import rdkit
from random import shuffle, choice
from .fast_jtnn import *

lg = rdkit.RDLogger.logger() 
lg.setLevel(rdkit.RDLogger.CRITICAL)

from botorch.models import SingleTaskGP
from botorch.fit import fit_gpytorch_model
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.acquisition import UpperConfidenceBound
from botorch.optim import optimize_acqf
import requests
from tqdm import tqdm 


class JTVAE(BaseOptimizer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = "jt_vae_bo"

    def _optimize(self, oracle, config):
        self.oracle.assign_evaluator(oracle)

        ## 0. load vae model 
        print('Loading traiend model ...')

        path_here = os.path.dirname(os.path.realpath(__file__))
        vocab_path = os.path.join(path_here, 'data/zinc/vocab.txt')
        model_path = 'jtvae.ckpt'


        if not os.path.exists(model_path):
            #### download pretrained model 
            url = "https://github.com/wenhao-gao/mol_opt/raw/main/main/jt_vae/fast_molvae/vae_model/model.iter-25000"
            response = requests.get(url, stream=True)
            total_size_in_bytes = int(response.headers.get("content-length", 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
            save_path = model_path
            with open(save_path, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()




        vocab = [x.strip("\r\n ") for x in open(vocab_path)] 
        vocab = Vocab(vocab)
        hidden_size = int(config['hidden_size'])
        latent_size = int(config['latent_size'])
        depthT = int(config['depthT'])
        depthG = int(config['depthG'])
        model = JTNNVAE(vocab, hidden_size, latent_size, depthT, depthG)
        model.load_state_dict(torch.load(model_path))
        vae_model = model.cuda() ### cuda() 
        print('Finish loading!')

        ## 0.1 training data 
        print('Fit initial GP model.')
        smiles_lst = self.all_smiles
        shuffle(smiles_lst)
        train_smiles_lst = smiles_lst[:config['train_num']]
        # y = self.oracle(train_smiles_lst)
        y = []
        train_X = []
        for smiles in train_smiles_lst:
            # x = vae_model.string2tensor(smiles)
            # x = x.unsqueeze(0)
            # z, _ = vae_model.forward_encoder(x) 
            batch = [smiles]
            try:
                mol_vec = vae_model.encode_latent_mean(batch)
                z = mol_vec.view(1,-1)
                train_X.append(z)
                yy = self.oracle(smiles)
                y.append(yy)
            except:
                pass 
        train_X = torch.cat(train_X, dim=0)
        train_X = train_X.detach()
        train_Y = torch.FloatTensor(y).view(-1,1)

        patience = 0
        
        while True:

            if len(self.oracle) > 100:
                self.sort_buffer()
                old_scores = [item[1][0] for item in list(self.mol_buffer.items())[:100]]
            else:
                old_scores = 0
            
            # 1. Fit a Gaussian Process model to data
            gp = SingleTaskGP(train_X, train_Y)
            mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
            fit_gpytorch_model(mll)

            # 2. Construct an acquisition function
            UCB = UpperConfidenceBound(gp, beta=0.1) 

            # 3. Optimize the acquisition function 
            for _ in range(config['bo_batch']):
                bounds = torch.stack([torch.min(train_X, 0)[0], torch.max(train_X, 0)[0]])
                z, _ = optimize_acqf(
                    UCB, bounds=bounds, q=1, num_restarts=5, raw_samples=20,
                )
                #### z: shape [1, d]

                ######## decode
                for i in range(z.shape[0]):
                    _z = z[i].view(1,-1)
                    tree_vec, mol_vec = torch.hsplit(_z, 2)
                    new_smiles = model.decode(tree_vec, mol_vec, prob_decode=False)

                if new_smiles is None or smiles_to_rdkit_mol(new_smiles) is None:
                    new_smiles = choice(smiles_lst)
                    new_score = self.oracle(new_smiles)
                else:
                    new_score = self.oracle(new_smiles)
                    if new_score == 0:
                        new_smiles = choice(smiles_lst)
                        new_score = self.oracle(new_smiles)

                new_score = torch.FloatTensor([new_score]).view(-1,1)

                train_X = torch.cat([train_X, z], dim = 0)
                train_Y = torch.cat([train_Y, new_score], dim = 0)
                if train_X.shape[0] > config['train_num']:
                    train_X = train_X[-config['train_num']:]
                    train_Y = train_Y[-config['train_num']:]

            # early stopping
            if len(self.oracle) > 800:
                self.sort_buffer()
                new_scores = [item[1][0] for item in list(self.mol_buffer.items())[:100]]
                if new_scores == old_scores:
                    patience += 1
                    if patience >= self.patience * 5:
                        self.log_intermediate(finish=True)
                        print('convergence criteria met, abort ...... ')
                        break
                else:
                    patience = 0
            
            if self.finish:
                print('max oracle hit, abort ...... ')
                break 
