"""Utility functions.


Things to capture:
- [[('more', 'RBR'), ('incriminating', 'JJ'), ('evidence', 'NN')]]
- Noun-noun phrases
- [[('that', 'IN'), ('other', 'JJ'), ('group', 'NN')]]
- [[('one', 'CD'), ('juror', 'NN')]]

Distinguish between "that dog" and "the dog"?

"""

import numpy as np 


# Mappings for 1-word NPs
one_word_np_mappings = {'PRP': 'PRP',
                        'NN': 'undeterminedNP',
                        'NNS': 'undeterminedNP',
                        # 'WP': None,
                        'PRP$': 'PossNP',
                        'NNP': 'ProperNP',
                        'NNPS': 'ProperNP',
                        'VBG': 'GerundNP',
                        'WP': 'WH_NP',
                        # 'VBN': None, # PastTense Verb
                        # 'VB': None,
                        # 'IN': None,
                        # 'JJ': None, # Adjective
                        # 'WDT': 'WDT',
                        'DT': 'BareDT'
                        # 'CD': 'DigitNP',
                        # 'RB': None, # Adverb
                        # 'TO': None,
                        # 'UH': None, # Filler
                        # 'DT': 'BareDT',
                        # 'MD': None, # Modal
                        # 'CC': None, # Coordinating conjunction?
                        } 



# Categories for different PRPs
prp_word_mappings = {'it': 'PRP_3rd',
                 'he': 'PRP_3rd',
                 'she': 'PRP_3rd',
                 'her': 'PRP_3rd',
                 'him': 'PRP_3rd',
                 'they': 'PRP_3rd',
                 'them': 'PRP_3rd',
                 'himself': 'PRP_3rd',
                 'herself': 'PRP_3rd',
                 'themselves': 'PRP_3rd',
                 'itself': 'PRP_3rd',
                 'i': 'PRP_1st',
                 'me': 'PRP_1st',
                 'myself': 'PRP_1st',
                 'us': 'PRP_1st',
                 'you': 'PRP_2nd',
                 'yourself': 'PRP_2nd',
                 'we': 'PRP_1st'}


def categorize_NPs_in_turn(turn_nps):
    """Return a code for which type of NPs are represented."""
    categories = []
    for np in turn_nps:
        cat = categorize_NP(np)
        if cat is not None:
            categories.append(cat)
    return categories


def categorize_NP(np):
    """Return label for POS tags."""
    pos = [token[1] for token in np]
    words = [token[0].lower() for token in np]
    if len(np) == 1:
        if pos[0] == "PRP":
            return prp_word_mappings[words[0]]
        if pos[0] in one_word_np_mappings:
            return one_word_np_mappings[pos[0]]
    else:
        if "DT" in pos:
            return "fullNP"
        elif pos[0] == "RB":
            return 'fullNP'
        elif "PRP$" in pos:
            return "PossNP"
        elif pos[0] == 'NN':
            return 'NounNoun'
        elif pos[-1] == 'NNS':
            return 'undeterminedNP'


def mean_length(turn_nps):
    """Return mean length of NPs in turn."""
    # Change to include ['full_NP', 'PossNP', 'undeterminedNP']
    full_NPs = [np for np in turn_nps if categorize_NP(np) == "fullNP"]
    if len(full_NPs) == 0:
        return 0
    length_NPs = [len(np) for np in full_NPs]
    return np.mean(length_NPs)


