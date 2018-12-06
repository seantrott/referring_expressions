"""Estimate breakdown of SpaCy mistakes.

Do false positives overrepresent a particular category?
What about misses?
"""

import pandas as pd 

import np_utils

from ast import literal_eval


def wrap_in_try(x):
	"""Wrap in try block."""
	try:
		return np_utils.categorize_NP(literal_eval(x))
	except Exception as e:
		return None


# False positives
df_false = pd.read_csv("data/evaluation/false_positives.csv")
df_false['category'] = df_false['false_pos'].apply(lambda x: wrap_in_try(x))

df_false = df_false.dropna()

print(df_false.category.value_counts() / len(df_false))

false_props = df_false.category.value_counts() / len(df_false)
false_props.to_csv("data/evaluation/eval_false_pos.csv")

## It looks like fullNPs are overrepresented, but I think this is because t
## they're not tagged with brackets in many Switchboard transcriptions.

# Missed


df_missed = pd.read_csv("data/evaluation/missed.csv")
df_missed['category'] = df_missed['missed'].apply(lambda x: wrap_in_try(x))

df_missed = df_missed.dropna()

print(df_missed.category.value_counts() / len(df_missed))

missed_props = df_missed.category.value_counts() / len(df_missed)
missed_props.to_csv("data/evaluation/eval_missed.csv")
