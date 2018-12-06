"""Format CallHome data.

TO DO:
Need to write parser for CallHome data.

Problem --> not all has grammar transcriptions?
"""

import os
import re
from os import listdir
import pandas as pd

from tqdm import tqdm

DATA_PATH = "/Users/seantrott/Dropbox/UCSD/Research/Ambiguity/Corpus_Analysis/data/callhome_english"
METADATA_PATH = "/Users/seantrott/Dropbox/UCSD/Research/Ambiguity/Corpus_Analysis/data/callhome_english/metadata_callhome.csv"



def parse_file(filetext, convo_id, file_id):
	"""Return list of turns in file from text.

	Parameters
	----------
	filetext: str
	  string formatted in the CallHome English corpus format.
	convo_id: int
	  id of conversation
	file_id: int
	  id for file

	Returns
	-------
	list
	  list with each row corresponding to information about a dialogue turn:
	  [speaker, text, turn index in conversation, conversation id, file id]
	"""

	def process_timestamp(timestamp):
		"""Kind of hacky, processes timestamp."""
		try:
			# timestamp = re.findall(r"\x15.*?\x15", timestamp)[0]
			timestamp = timestamp.replace("\x15", "")
			return [int(i) for i in timestamp.split("_")]
		except Exception as e:
			print(e)
			return None, None

	turns = []
	record = False 
	current_turn = ""
	turn_index = 1
	for index in range(len(filetext)):
		if record:
			current_turn += filetext[index]
		if filetext[index] in [".", "?", "!"]:
			current_turn = current_turn.replace("A:", "").replace("B:", "")

			new_index = index 
			timestamp = ""
			started = False
			while new_index < len(filetext):
				if started:
					timestamp += filetext[new_index]
				if filetext[new_index] == "\x15":
					if started == False:
						started = True
					else:
						started == False
						break
				new_index += 1

			beginning, end = process_timestamp(timestamp)
			# print(timestamp)
			turns.append([current_speaker, current_turn, turn_index, convo_id, file_id, beginning, end])
			turn_index += 1
			record = False
			current_turn = ""
		if filetext[index] == "*": # Mark of a new turn starting
			current_speaker = filetext[index + 1]
			if current_speaker in ['A', 'B']:
				record = True
	return turns



def main():
	all_filepaths = [os.path.join(DATA_PATH, file)
             	 for file in listdir(DATA_PATH)
             	 if "metadata" not in file and "0doc" not in file]

	### Metadata
	df_metadata = pd.read_csv(METADATA_PATH)
	df_metadata['file_id'] = df_metadata['English']
	valid_ids = list(df_metadata['file_id'])

	valid_files = [f for f in all_filepaths if int(f.split(".cha")[0].split("/")[-1]) in valid_ids]

	all_turns = []
	for f in tqdm(valid_files):
		filetext = open(f, "r").read()
		lines = filetext.split("\n")
		convo_id = int(lines[1].split(":")[-1].split("-")[1])
		file_id = int(f.split("/")[-1].split(".cha")[0])

		turns = parse_file(filetext, convo_id=convo_id, file_id=file_id)

		all_turns += turns

	df_callhome = pd.DataFrame(all_turns, columns = ['speaker', 'text', 'turn_index', 'convo_id', 'file_id', 'begin_turn', 'end_turn'])

	# Add metadata	
	df_merged = df_callhome.merge(df_metadata, on="file_id")
	df_merged.to_csv("data/raw/callhome_plus_metadata.csv")


if __name__ == "__main__":
	main()