Code to pre-process dialogue corpora, identify referring expressions (REs), and categorize the REs that occur.

# Preprocessing

Note that these preprocessing steps assume that you have another directory, `data`, in the same directory as `ReferringExpressions`.

Specifically, you should have downloaded callhome and switchboard into the following paths:

```
../data/callhome_english
../data/swda
```

[Link to download CallHome](https://ca.talkbank.org/data/CallHome/eng.zip)  
[Link to download Switchboard](http://compprag.christopherpotts.net/code-data/swda.zip)

## Switchboard

Switchboard has already been separated into .csv files with tags for NPs and dialogue acts, so the preprocessing just involves concatenating these files and incorporating metadata.

```
python src/data/preprocess_switchboard.py
```

## CallHome

The CallHome corpus is in a raw text format, so preprocessing includes parsing into separate turns, and putting into a .csv format.

```
python src/data/preprocess_callhome.py
```


# Identify NPs

Now you can use spaCy to identify **noun chunks** in each turn. Substitute either `switchboard` or `callhome` for `{DATASET_NAME}`. 

```
python src/features/identify_np.py --dataset={DATASET_NAME}
```

## Evaluating identification

You might also want to know how well spaCy performs. We can use the Switchboard data as a baseline. Run:

```
python src/features/evaluate_spacy_tags.py
```



# Categorize NPs

Once you've identified each NP, you can further categorize them into the pre-specified bins (e.g. *full NP*, *PRP_3rd*, etc.).

```
python src/features/analyze_nps.py --dataset={DATASET_NAME}
```

You can also run a separate script to identify the *length* of each NP.

```
python src/features/analyze_lengths.py --dataset={DATASET_NAME}
```

# Analysis of RE distributions by turn and dataset

Finally, you can produce a report by *knitting* the .Rmd file at `src/reports/analysis_report.Rmd`. 

