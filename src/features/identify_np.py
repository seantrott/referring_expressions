"""Identify all NPs in strings using Spacy.

To do:
- Remove <laughter> tags (and so on)
- Remove disfluencies?
- Maybe don't remove punctuation?
- Doesn't identify bare deictic NPs

"""

import spacy
import pandas as pd 
from tqdm import tqdm

import nltk
import re

from nlp_utilities import TextCleaner

# Load corpus
nlp = spacy.load('en')

## Path
DATA_PATHS = {'switchboard': "data/raw/switchboard_plus_metadata.csv",
			  'callhome': "data/raw/callhome_plus_metadata.csv"}

# Allowable one-letter pronouns
ALLOWABLE_PRONOUNS = ['i', 'I']

# Deictic expressions
DEICTIC = ['that',
		   'this',
		   'those',
		   'these']

# What about: 'here', 'there', 'now' (temporal deixis)


def remove_tags(text):
	"""Remove tags, e.g. <laughter>."""
	text = re.sub(r"&=\S+", "", text)
	text = re.sub(r"\<.*?\>", "", text)
	return text

def identify_bare_deictic(text):
	"""Identify bare deictic expressions, like that[NP]. SpaCy fails to do this.

	Procedure: identify all deictic DTs. If the following item is a kind of verb,
	add it to the list.
	"""
	deictic_nps = []
	tags = nltk.pos_tag(nltk.word_tokenize(text))
	for index, tag in enumerate(tags):
		word, pos = tag
		if word in DEICTIC:
			word_next, pos_next = tags[index+1]
			if pos_next[0] == "V":
				deictic_nps.append([(word, 'DeicticDT')])
	return deictic_nps


def find_noun_phrases(text):
	"""Find NPs."""
	returned = []
	# Remove <laughter> and <throat_clearing>
	stripped_tags = remove_tags(text)
	cleaned_text = TextCleaner.preserve_only_text(stripped_tags)
	doc = nlp(cleaned_text)
	for np in doc.noun_chunks:
		if len(np.text.strip()) <= 1 and np.text.strip() not in ALLOWABLE_PRONOUNS:
			continue
		pos = nltk.pos_tag(np.text.split())
		returned.append(pos)

	bare_deictic = identify_bare_deictic(text)
	# Add to list of NPs
	returned += bare_deictic
	return returned


def main(dataset_name):
	"""Load indicated dataset, then identify all NPs."""
	tqdm.pandas()

	DATA_PATH = DATA_PATHS[dataset_name]
	df = pd.read_csv(DATA_PATH)

	df = df[df['text'].notnull()]

	df['spacy_NPs'] = df['text'].progress_apply(find_noun_phrases)

	df.to_csv("data/processed/{dataset}_with_spacy_np.csv".format(dataset=dataset_name))


if __name__ == "__main__":
	from argparse import ArgumentParser 

	parser = ArgumentParser()

	parser.add_argument("--dataset", type=str, dest="dataset_name",
						default="switchboard")
	
	args = vars(parser.parse_args())
	main(**args)
