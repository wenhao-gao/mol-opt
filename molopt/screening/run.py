from __future__ import print_function

import argparse
import yaml
import os
from copy import deepcopy
import numpy as np
from tdc import Oracle
from ..base import BaseOptimizer

class Screening(BaseOptimizer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = "screening"

    def _optimize(self, oracle, config):

        self.oracle.assign_evaluator(oracle)

        all_mols = deepcopy(self.all_smiles)
        np.random.shuffle(all_mols)

        for i in range(0, len(all_mols), 100):
            scores = self.oracle(all_mols[i: i+100])
            if self.finish:
                break



