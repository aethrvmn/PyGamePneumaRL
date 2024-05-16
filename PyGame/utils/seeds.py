import random
import torch as T
import numpy as np


def set_seeds(value):

    random.seed(value)
    np.random.seed(value)
    T.manual_seed(value)
    T.cuda.manual_seed_all(value)
