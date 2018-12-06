"""Identify all unique constructions from SpaCy parser.

E.g. DT_NN, DT_NNS, PRP, etc.
"""

import pandas as pd 

import pprint

from collections import Counter
from ast import literal_eval

from tqdm import tqdm


DATA_PATHS = {'switchboard': "data/processed/switchboard_with_spacy_np.csv",
              'callhome': "data/processed/callhome_with_spacy_np.csv"}


df = pd.read_csv(DATA_PATHS['callhome'])

cxns = []
for turn_s in tqdm(list(df['spacy_NPs'])):
	turn = literal_eval(turn_s)
	for np in turn:
		pos = [i[1] for i in np]
		if len(pos) > 2:
			pos = [pos[0], pos[-1]]
		cxns.append("_".join(pos))
		# cxns.append

counts = Counter(cxns)
pprint.pprint(counts)