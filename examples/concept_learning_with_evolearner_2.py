import json
import os
from random import shuffle

from ontolearn.knowledge_base import KnowledgeBase
from ontolearn.concept_learner import EvoLearner
from ontolearn.learning_problem import PosNegLPStandard
from owlapy.model import OWLClass, OWLNamedIndividual, IRI
from ontolearn.utils import setup_logging
from ontolearn.metrics import F1
from sklearn.model_selection import ParameterGrid
from owlapy.render import DLSyntaxObjectRenderer
from ontolearn.value_splitter import BinningValueSplitter, EntropyValueSplitter
import examples.search as es

setup_logging()

space_grid = None

def get_space_grid():
    global space_grid
    if space_grid:
        return space_grid    
    binning_value_splitter = BinningValueSplitter()
    entropy_value_splitter = EntropyValueSplitter()
    space = dict()
    space['max_runtime'] = [10, 500, 900, 1300]
    space['tournament_size'] = [2, 5, 7, 10]
    space['height_limit'] = [3, 5, 17, 25]
    space['use_data_properties'] = [True, False]
    space['value_splitter'] = [binning_value_splitter, entropy_value_splitter]
    space_grid = list(ParameterGrid(space))
    return space_grid

try:
    os.chdir("examples")
except FileNotFoundError:
    pass

with open('carcinogenesis_lp.json') as json_file:
    settings = json.load(json_file)

kb = KnowledgeBase(path=settings['data_path'])

for str_target_concept, examples in settings['problems'].items():
    p = set(examples['positive_examples'])
    n = set(examples['negative_examples'])
    print('Target concept: ', str_target_concept)
    typed_pos = list(set(map(OWLNamedIndividual, map(IRI.create, p))))
    typed_neg = list(set(map(OWLNamedIndividual, map(IRI.create, n))))
    
    #shuffle the Positive and Negative Sample
    shuffle(typed_pos)   
    shuffle(typed_neg)

    #Split the data into Training Set and Test Set
    train_pos = set(typed_pos[:int(len(typed_pos)*0.8)])
    train_neg = set(typed_neg[:int(len(typed_neg)*0.8)])
    test_pos = set(typed_pos[-int(len(typed_pos)*0.2):])
    test_neg = set(typed_neg[-int(len(typed_neg)*0.2):])
    lp = PosNegLPStandard(pos=train_pos, neg=train_neg)

    #Create the grid space for hyper parameter tuning
    space_grid = get_space_grid()
    es.grid_search_with_custom_cv(kb, str_target_concept, list(train_pos), list(train_neg), space_grid, 3)

print(es.df)