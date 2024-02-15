# mol-opt: a Python Toolbox for Molecular Design

## 🚀 Installation 
To install the necessary dependencies, we require python 3.8, and run the following commands:

```
python setup.py install 
```

## 💻 Usage

```python
from molopt import GraphGA
optimizer = GraphGA(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
optimizer.optimize(oracle='qed', config='molopt/graph_ga/hparams_default.yaml', patience=5, seed=0)
```

## 🤝 Contributing
If you wish to contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file. We welcome pull requests for bug fixes, feature requests, and improvements to our code.


## 📜 License
This project is licensed under the terms of the [MIT License](LICENSE).


## 💼 Support
If you need help with the tool, you can raise an issue on our GitHub issue tracker. For other questions, please contact our team. 

*Please note: mol-opt is under active development and certain functionalities are yet to be fully implemented.*

## 📞 Contact 
Please contact gaowh19@gmail.com for help or submit an issue. 


## Cite Us
If you found this package useful, please cite [our paper](https://proceedings.neurips.cc/paper_files/paper/2022/file/8644353f7d307baaf29bc1e56fe8e0ec-Paper-Datasets_and_Benchmarks.pdf) (NeurIPS 2022):

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

