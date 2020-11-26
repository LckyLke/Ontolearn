"""
====================================================================
Drill -- Deep Reinforcement Learning for Refinement Operators in ALC
====================================================================
Drill with continous training.
Author: Caglar Demir
"""

from ontolearn import KnowledgeBase, LearningProblemGenerator
from ontolearn.rl import DrillSample, DrillAverage
from ontolearn.refinement_operators import LengthBasedRefinement
from ontolearn.util import apply_TSNE_on_df
import json
import pandas as pd

PATH_FAMILY = '../data/family-benchmark_rich_background.owl'
family_embeddings_path = '../embeddings/dismult_family_benchmark/instance_emb.csv'
pretrained_drill_sample_path = '../pre_trained_agents/Family/Drill_Sample/1605797163.5565891_DrillHeuristic_sample.pth'
pretrained_drill_average_path = '../pre_trained_agents/Family/Drill_Average/1605801167.8185513_DrillHeuristic_average.pth'

with open('synthetic_problems.json') as json_file:
    settings = json.load(json_file)
data_path = settings['data_path']

kb = KnowledgeBase(PATH_FAMILY)
rho = LengthBasedRefinement(kb=kb)

balanced_examples = LearningProblemGenerator(knowledge_base=kb, num_problems=1, min_num_ind=15).balanced_examples

instance_emb = pd.read_csv(family_embeddings_path, index_col=0)
# apply_TSNE_on_df(instance_emb)  # if needed.
model_sub = DrillSample(knowledge_base=kb, refinement_operator=rho, num_episode=10, instance_embeddings=instance_emb,
                        pretrained_model_path=pretrained_drill_sample_path).train(balanced_examples, relearn_ratio=2)

model_avg = DrillAverage(knowledge_base=kb, refinement_operator=rho, num_episode=10, instance_embeddings=instance_emb,
                         pretrained_model_path=pretrained_drill_average_path).train(balanced_examples, relearn_ratio=2)

for str_target_concept, examples in settings['problems'].items():
    p = set(examples['positive_examples'])
    n = set(examples['negative_examples'])
    print('Target concept: ', str_target_concept)

    model_avg.fit(pos=p, neg=n)
    print(model_avg.best_hypotheses(n=1)[0])

    model_sub.fit(pos=p, neg=n)
    print(model_sub.best_hypotheses(n=1)[0])
