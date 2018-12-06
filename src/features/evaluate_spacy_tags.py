"""Evaluate SPACY tags against Switchboard.

TO DO:
What's the best measure of accuracy?
- % of NPs identified (e.g. power to detect)
- % of correct NPs identified (e.g. how many of NPs it detected were "real")


"""

import pandas as pd 
import re

import numpy as np

from tqdm import tqdm
from ast import literal_eval


## Path
DATA_PATH = "data/processed/switchboard_with_spacy_np.csv"


def find_tagged_NPs(chunked_text):
	"""Find tagged phrases in Switchboard."""
	noun_phrases = re.findall(r"\[.*?\]", chunked_text)
	chunked_nps = []
	for np in noun_phrases:
		new_np = np.replace("[", "").replace("]", "").strip()
		constituents = new_np.split(" ")
		chunked_nps.append([tuple(c.split("/")) for c in constituents])
	return chunked_nps


def evaluate_spacy_recall(spacy_np, tagged_np):
	"""Compare NP chunks."""
	identified = 0
	missed = []
	for known_np in tagged_np:
		if known_np in spacy_np:
			identified += 1
		else:
			missed.append(known_np)
	return [identified / len(tagged_np), missed]

def evaluate_spacy_precision(spacy_np, tagged_np):
	"""Compare NP chunks."""
	identified = 0
	false_pos = []
	for possible_np in spacy_np:
		if possible_np in tagged_np:
			identified += 1
		else:
			false_pos.append(possible_np)
	return [identified / len(spacy_np), false_pos]


df_tagged = pd.read_csv(DATA_PATH)

missed_np, missed_text, false_pos_np, false_pos_text = [], [], [], []
recalls, precisions = [], []
rows = list(df_tagged.iterrows())
for index, row in tqdm(rows):
	tagged_np = find_tagged_NPs(row['pos'])
	spacy_np = literal_eval(row['spacy_NPs'])

	text = row['text']

	if len(tagged_np) > 0 and len(spacy_np) > 0:
		recall, missed = evaluate_spacy_recall(spacy_np, tagged_np)
		missed_np += missed
		missed_text += [text] * len(missed)

		recalls.append(recall)
		precision, false_pos = evaluate_spacy_precision(spacy_np, tagged_np)
		precisions.append(precision)
		false_pos_np += false_pos
		false_pos_text += [text] * len(false_pos)


print("Proportion of NPs recovered: {recall}".format(recall=np.mean(recalls)))
print("Proportion of 'true NPs' identified: {precision}".format(precision=np.mean(precisions)))

df_metrics = pd.DataFrame([{'recall': np.mean(recalls),
						    'precision': np.mean(precisions),
						    'recall_std': np.std(recalls),
						    'precision_std': np.std(precisions),
						    'total_turns': len(recalls)}])
df_metrics.to_csv("data/evaluation/eval_metrics.csv")

df_missed = pd.DataFrame.from_dict({'missed': missed_np, 'text': missed_text})
df_missed.to_csv("data/evaluation/missed.csv")
df_false = pd.DataFrame.from_dict({'false_pos': false_pos_np, 'text': false_pos_text})
df_false.to_csv("data/evaluation/false_positives.csv")


