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

    rows = list(df_with_np.iterrows())
    for index, row in tqdm(rows):
        # Extract actual list from string
        turn = row['spacy_NPs']
        turn = literal_eval(turn)
        # Get NP categories that appear in turn
        for np in turn:
            category = np_utils.categorize_NP(np)
            length = len(np)
            new_observation = {'RE_type': category,
                               'np_length': length}
            turn_data = {**dict(row), **new_observation}

            identified.append(turn_data)

    df_turns = pd.DataFrame(identified)
    df_turns.to_csv("data/processed/{dataset_name}_np_lengths.csv".format(dataset_name=dataset_name))
   

if __name__ == "__main__":
    from argparse import ArgumentParser 

    parser = ArgumentParser()

    parser.add_argument("--dataset", type=str, dest="dataset_name",
                        default="switchboard")
    
    args = vars(parser.parse_args())
    main(**args)
