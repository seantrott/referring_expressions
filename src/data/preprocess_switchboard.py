"""Concatenate Switchboard data"""

import os
import pandas as pd

from tqdm import tqdm


# PATHS
DATA_PATH = "/Users/seantrott/Dropbox/UCSD/Research/Ambiguity/Corpus_Analysis/data/swda"
METADATA_PATH = "/Users/seantrott/Dropbox/UCSD/Research/Ambiguity/Corpus_Analysis/data/swda/swda-metadata.csv"


def main(DATA_PATH, METADATA_PATH):
	"""Read in all switchboard files, concatenate to a single dataframe, then combine with metadata.

	Parameters
	----------
	DATA_PATH: str
	  path to directory containing all relevant transcripts
	METADATA_PATH: str
	  path to file with all metadata about conversations
	"""
	all_filepaths = [os.path.join(root, name)
	             	 for root, dirs, files in os.walk(DATA_PATH)
	             	 for name in files if ".csv" in name and "metadata" not in name]

	all_files = []
	for file in tqdm(all_filepaths):
		df = pd.read_csv(file)
		all_files.append(df)

	df_concat = pd.concat(all_files).reset_index()

	## Get metadata
	df_metadata = pd.read_csv(METADATA_PATH).reset_index()

	# Combine together
	df_combined = df_concat.merge(df_metadata, on="conversation_no")

	# Write to file
	print("Saving data...")
	df_combined.to_csv("data/raw/switchboard_plus_metadata.csv")


if __name__ == "__main__":
	main(DATA_PATH=DATA_PATH, METADATA_PATH = METADATA_PATH)

