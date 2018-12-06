"""Analyze NPs over the course of a dialog.

For now, I'm just selecting a random NP for ease of data storage.

TO DO:
- Refine code (see below)

Refine code:
- set a list somewhere of all the NP types we want to find, make it consistent across codebases

What about *bare deictic NPs*? Seems not to be finding them? E.g. "That".
"""

import pandas as pd 
from ast import literal_eval

import random

from tqdm import tqdm

import np_utils



DATA_PATHS = {'switchboard': "data/processed/switchboard_with_spacy_np.csv",
              'callhome': "data/processed/callhome_with_spacy_np.csv"}



def main(dataset_name):
    """Load data, then assign categories to the NPs in each turn."""
    print("Analyzing {data} data".format(data=dataset_name))
    df_with_np = pd.read_csv(DATA_PATHS[dataset_name])

    identified = []
  
    for turn in tqdm(list(df_with_np['spacy_NPs'])):
        # Extract actual list from string
        turn = literal_eval(turn)
        # Get NP categories that appear in turn
        categories = np_utils.categorize_NPs_in_turn(turn) 
        
        identified.append({
            'full_NP': len([cat for cat in categories if cat == 'fullNP']),
            'undetermined_NP': len([cat for cat in categories if cat == 'undeterminedNP']),
            'poss_NP': len([cat for cat in categories if cat == 'PossNP']),
            'prp_1st': len([cat for cat in categories if cat == 'PRP_1st']),
            'prp_2nd': len([cat for cat in categories if cat == 'PRP_2nd']),
            'prp_3rd': len([cat for cat in categories if cat == 'PRP_3rd']),
            'proper_NP': len([cat for cat in categories if cat == 'ProperNP']),
            'gerund_NP': len([cat for cat in categories if cat == 'GerundNP']),
            'noun_noun': len([cat for cat in categories if cat == 'NounNoun']),
            'wh_np': len([cat for cat in categories if cat == 'WH_NP']),
            'total_REs': len(categories)
            })


    df_identified = pd.DataFrame(identified)

    df_merged = df_with_np.join(df_identified)
    df_merged.to_csv("data/processed/{dataset_name}_labeled.csv".format(dataset_name=dataset_name))

if __name__ == "__main__":
    from argparse import ArgumentParser 

    parser = ArgumentParser()

    parser.add_argument("--dataset", type=str, dest="dataset_name",
                        default="switchboard")
    
    args = vars(parser.parse_args())
    main(**args)
