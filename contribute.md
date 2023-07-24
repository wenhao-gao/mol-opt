# Contribution Guide

Thanks for your interest in our benchmark! This guide was made to help you develop your model that fits our benchmark quickly. If you have a other suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue.


## 1) Create a directory for new method molopt/MODEL_NAME 

All codes for a model should be in the `molopt/MODEL_NAME` directory, including pretrained model. A `README.md` is prefered to describe the method.

```bash
mkdir molopt/MODEL_NAME
```

- `molopt/__init__.py`: you need to add 
```python
from .MODEL_NAME import MODEL_CLASS     
```
- `molopt/MODEL_NAME/__init__.py`: you need to add 
```python
from .run import MODEL_CLASS 
```


## 2) Make an Optimizer class for your method

One should run the `molopt/MODEL_NAME/run.py` to optimize a property by:

```bash
python run.py MODEL_NAME 
```

Within this `run.py` file, the core code for optimization should be implemented in an optimizer class. One should inherit from BaseOptimizer defined in `molopt/optimizer.py`, in which defined all necessary infrastructures for a molecular optimization run: 

```python
from ..base import BaseOptimizer

class MODEL_NAME(BaseOptimizer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ## Your model name, used for logging your results
        self.model_name = "model_name" 

    def _optimize(self, oracle, config): 
        """
        The code for a function to optimize a oracle function with hyper-parameters defined in config
        """
        
        ## This line is necessary
        self.oracle.assign_evaluator(oracle)

        ############# Your code to optimize an oracle function #############
        ############################## START ###############################

        ## Initialization
        population_size = config["population_size"]
        ...

        ## A typical iterative optimization loop
        for it in range(iterations):

        	## Search for next batch to evaluate
            population = model(old_population)
            ...

	        ## Score the smiles strings with self.oracle, with either a list of SMILES or a SMILES as input
            ## Doing so automatically:
            ##     1) scores the new input molecules and retrieves values for old ones
            ##     2) saves results to self.mol_buffer for logging and analyzing
            ##     3) logs the results to wandb with a predefined frequency
            ##     4) determins if we reached a predefined maximum number of oracle calls
    	    population_scores = self.oracle(population) 

            ## If we reached a predefined maximum number of oracle calls, break
            ## This line could be used in 
            if self.finish:
                break

            ## or one could also use self.oracle.finish to check within a user-defined function with self.oracle
            if self.oracle.finish:
                break

            ## Once you decide to early-stop, you could use self.log_intermediate(finish=True) to fake a converged 
            ## line to maximum number of oracle calls for comparison purposes
            if converge: 
                self.log_intermediate(finish=True)
                break
        ############################### END ################################
```

## 3) Data file

If you need some data file, you need to change `setup.py` and `MANIFEST.in`. For example, in `graph_mcts`, you want to add `molopt/graph_mcts/size_stats.p`. 


- `setup.py`: you need to add the following line in `setup` function
```python
    package_data={'molopt': [..., 'graph_mcts/size_stats.p',
                            ..., ]},
```
- `MANIFEST.in`: you need to add a new line 
```python
include molopt/graph_mcts/size_stats.p
```



## 4) Hyperparameters

We separate hyperparameters for task-level control, defined from `argparse`, and algorithm-level control, defined from `hparam_default.yaml`. There is no clear boundary for them, but we reccomend one keep all hyperparameters in the `self._optimize` function as task-level. 

* **running hyperparameter**: parser argument. 
* **default model hyperparameter**: `hparam_default.yaml`
* **tuning model hyperparameter**: `hparam_tune.yaml` 

For algorithm-level hyperparameters, we adopt the stratforward yaml file format. One should define a default set of hyper-parameters in `molopt/MODEL_NAME/hparam_default.yaml`:

```python
population_size: 50
offspring_size: 100
mutation_rate: 0.02
patience: 5
max_generations: 1000
```

And the search space for hyper-parameter tuning in `molopt/MODEL_NAME/hparam_tune.yaml`:

```python
name: graph_ga
method: random
metric:
  goal: maximize
  name: avg_top100
parameters:
  population_size:
    values: [20, 40, 50, 60, 80, 100, 150, 200]
  offspring_size:
    values: [50, 100, 200, 300]
  mutation_rate:
    distribution: uniform
    min: 0
    max: 0.1
  patience:
    value: 5
  max_generations:
    value: 1000
```



## 5) Run with three-line python code


First you need to install the mol-opt package via

```bash
python setup.py install 
```

Then you can run each method with three-line python code 

```python
from molopt import SmilesVAE
optimizer = SmilesVAE(smi_file=None, n_jobs=-1, max_oracle_calls=10000, freq_log=100, output_dir = 'results', log_results=True) 
optimizer.optimize(oracle='qed', config='molopt/smiles_vae/hparams_default.yaml', patience=5, seed=0)
```

One can use argparse help to check the detail description of the arguments.


## 6) Results 

All the results are saved in the `results` folder. 










