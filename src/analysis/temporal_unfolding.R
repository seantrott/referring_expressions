library(tidyverse)
library(lme4)
library(reshape)


setwd("/Users/seantrott/Dropbox/UCSD/Research/Ambiguity/Corpus_Analysis/ReferringExpressions")

df_switchboard = read_csv("data/processed/switchboard_labeled.csv")

df_switchboard$topic = factor(df_switchboard$topic_description)
df_switchboard$from_caller_sex = factor(df_switchboard$from_caller_sex)
df_switchboard$to_caller_sex = factor(df_switchboard$to_caller_sex)



## Bins turns

df_switchboard$binned_turn = cut(df_switchboard$utterance_index, breaks=seq(0, 100, 1), labels=FALSE)

df_switchboard = na.omit(df_switchboard)


# Group By turn
prop_by_turn = df_switchboard %>%
  group_by(binned_turn) %>%
  summarise(prop_full = sum(full_NP) / sum(total_REs),
            prop_prp_1st = sum(prp_1st) / sum(total_REs),
            prop_prp_2nd = sum(prp_2nd) / sum(total_REs),
            prop_prp_3rd = sum(prp_3rd) / sum(total_REs), 
            prop_bare = sum(bare_NP) / sum(total_REs),
            prop_poss = sum(poss_NP) / sum(total_REs),
            prop_proper_np = sum(proper_NP) / sum(total_REs),
            prop_gerund_np = sum(gerund_NP) / sum(total_REs),
            prop_noun_noun = sum(noun_noun) / sum(total_REs))

prop_by_turn = df_switchboard %>%
  group_by(binned_turn) %>%
  summarise(prop_full = sum(full_NP) / (sum(full_NP) + sum(prp_3rd) + sum(prp_1st)),
            prop_prp_3rd = sum(prp_3rd) / (sum(full_NP) + sum(prp_3rd) + sum(prp_1st)),
            prop_prp_1st = sum(prp_1st) / (sum(full_NP) + sum(prp_3rd) + sum(prp_1st))) 


melted = melt(as.data.frame(prop_by_turn), id=c("binned_turn"))

melted %>%
  ggplot(aes(x = binned_turn,
             y = value,
             color = variable)) +
  geom_point() +
  stat_smooth(method = "loess") +
  # geom_line(stat = "identity") + 
  # geom_smooth(method = "lm") +
  labs(x = "Turn number",
       y = "Proportion of REs",
       title = "Distribution of RE types by turn number",
       color = "RE Type") +
  theme_minimal()


## Analysis

df_switchboard$speaker_recoded = paste(df_switchboard$caller, df_switchboard$conversation_no, sep = "_")

df_switchboard_critical = df_switchboard %>%
  filter(utterance_index <= 100) %>%
  select(utterance_index, speaker_recoded, bare_NP, full_NP, prp_1st, prp_2nd, prp_3rd,
         poss_NP, proper_NP, noun_noun, wh_np, gerund_NP)


sb_melted = melt(as.data.frame(df_switchboard_critical), id=c("utterance_index", "speaker_recoded"))

sb_melted %>%
  ggplot(aes(x = utterance_index,
             y = value,
             color = variable)) +
  geom_point(stat = "summary", fun.y = "mean") +
  geom_smooth(method = "lm") +
  # geom_smooth() +
  theme_minimal()

model_lm = lm(data = sb_melted,
                   value ~ variable * utterance_index)

model_simple = glm(data = sb_melted,
                   value ~ variable * utterance_index,
                   family = poisson())

model_simple_reduced = glm(data = sb_melted,
                   value ~ variable + utterance_index,
                   family = poisson())

anova(model_simple_reduced, model_simple)


model = glmer(data = sb_melted,
              value ~ variable * utterance_index + (1 | speaker),
              family = poisson())

model_reduced = glmer(data = sb_melted,
                      value ~ variable + utterance_index + (1 | speaker),
                      family = poisson())


################ 

#### Callhome

setwd("/Users/seantrott/Dropbox/UCSD/Research/Ambiguity/Corpus_Analysis/ReferringExpressions")

df_callhome = read_csv("data/processed/callhome_labeled.csv")


df_callhome$begin_turn2 = df_callhome$begin_turn / 1000
df_callhome$end_turn2 = df_callhome$end_turn / 1000
df_callhome$turn_length = df_callhome$end_turn2 - df_callhome$begin_turn2
# df_callhome$turn_length = df_callhome$turn_length / 1000

test = df_callhome %>%
  group_by(convo_id) %>%
  summarise(median_turn_length = median(turn_length, na.rm = TRUE))

df_callhome = merge(test, df_callhome)

df_callhome$turn_staggered = round(df_callhome$begin_turn2 / df_callhome$median_turn_length)

df_callhome = na.omit(df_callhome)

df_callhome %>%
  filter(RE_type %in% c("fullNP", "PossNP")) %>%
  ggplot(aes(x = turn_staggered,
             y = length,
             color = RE_type)) +
  geom_point(stat = "summary", fun.y = "mean") +
  geom_smooth(method = "lm")


callhome_counts = df_callhome %>%
  group_by(file_id, convo_id, turn_staggered, RE_type) %>%
  summarise(count = n())


callhome_counts %>%
  # filter(RE_type %in% c("fullNP", "PRP_3rd", "PRP_1st")) %>%
  filter(turn_staggered <= 200) %>%
  ggplot(aes(x = turn_staggered,
             y = count,
             color = RE_type)) +
  # geom_point(stat = "summary", fun.y = "mean") +
  # geom_smooth(method = "lm") +
  geom_smooth() +
  theme_minimal()


### Anslysis

df_callhome$speaker_recoded = paste(df_callhome$speaker, df_callhome$file_id, sep = "_")

df_callhome_critical = df_callhome %>%
  filter(turn_staggered <= 500) %>%
  select(turn_staggered, speaker_recoded, bare_NP, full_NP, prp_1st, prp_2nd, prp_3rd,
         poss_NP, proper_NP, noun_noun, wh_np, gerund_NP)


ch_melted = melt(as.data.frame(df_callhome_critical), id=c("turn_staggered", "speaker_recoded"))


ch_melted %>%
  ggplot(aes(x = turn_staggered,
             y = value,
             color = variable)) +
  # geom_point(stat = "summary", fun.y = "mean") +
  # geom_smooth(method = "lm") +
  geom_smooth() +
  theme_minimal()

model_simple = glm(data = ch_melted,
                   value ~ variable * turn_staggered,
                   family = poisson())

model_simple_reduced = glm(data = ch_melted,
                           value ~ variable + turn_staggered,
                           family = poisson())

anova(model_simple_reduced, model_simple)

model = glmer(data = ch_melted,
              value ~ variable * turn_index + (1 | speaker_recoded),
              family = poisson())

model_reduced = glmer(data = ch_melted,
                      value ~ variable + turn_index + (1 | speaker_recoded),
                      family = poisson())



