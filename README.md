# mol-opt: a Python Toolbox for Molecular Design

**Please note: mol-opt is under active development and certain functionalities are yet to be fully implemented.**

## 🚀 Installation 
To get started with our package, please first ensure that PyTorch is installed with a CUDA version compatible with your device. You can find detailed installation instructions on [the official PyTorch website](https://pytorch.org/get-started/locally/).
Once PyTorch is set up, you can install the remaining dependencies for our package by executing:
```
pip install .
```
Please note, our package has been tested and confirmed to work with Python 3.8. We recommend using this version to ensure compatibility and optimal performance.

## 💻 Usage (3 lines of code)

Oracle can be a `string` refering to a [TDC oracle](https://tdcommons.ai/functions/oracles/), e.g., `qed`, `jnk3`, `gsk3b`: 

```python
from molopt.graph_ga import GraphGA
optimizer = GraphGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
optimizer.optimize(oracle='qed', patience=5, seed=0)
```

or a callable function that takes a smiles string as input and return a real value: 

```python
from molopt.graph_ga import GraphGA
from rdkit import Chem
from rdkit.Chem import Descriptors
optimizer = GraphGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 

def mol_wt(smi):
    m = Chem.MolFromSmiles(smi)
    if m is None:
        return 0
    else:
        return Descriptors.MolWt(m)

optimizer.optimize(oracle=mol_wt, patience=5, seed=0)
```

Note that all methods are by default desigend to maximize the oracle function. We support three hyperparameter tune strategies:
- default: e.g., `optimizer.optimize(oracle='qed', patience=5, seed=0)`. 
- configuration file: e.g., for graph GA, `optimizer.optimize(oracle='qed', config='molopt/graph_ga/hparams_default.yaml', patience=5, seed=0)`. 
- keyword update: e.g., for graph GA, `optimizer.optimize(oracle='qed', patience=5, seed=0, population_size=120)`. 


You can follow [the format of yaml file](https://github.com/wenhao-gao/mol_opt/blob/main/main/graph_ga/hparams_default.yaml) to define the hyper-parameters.

## 🤝 Contributing
If you wish to contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file. We welcome pull requests for bug fixes, feature requests, and improvements to our code.


## 📜 License
This project is licensed under the terms of the [Apache 2.0 License](LICENSE).


## 💼 Support
If you need help with the tool, you can raise an issue on our GitHub issue tracker. For other questions, please contact our team. 

## 📞 Contact 
Please contact futianfan@gmail.com and gaowh19@gmail.com for help or submit an issue. 


## Cite Us
This package was developed as a spin-off from [our paper](https://proceedings.neurips.cc/paper_files/paper/2022/file/8644353f7d307baaf29bc1e56fe8e0ec-Paper-Datasets_and_Benchmarks.pdf) (NeurIPS 2022). If you find this package useful, please consider citing:

```
@article{gao2022sample,
  title={Sample efficiency matters: a benchmark for practical molecular optimization},
  author={Gao, Wenhao and Fu, Tianfan and Sun, Jimeng and Coley, Connor},
  journal={Advances in Neural Information Processing Systems},
  volume={35},
  pages={21342--21357},
  year={2022}
}
```

