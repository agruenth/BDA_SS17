import numpy as np
import pandas as pd
import seaborn as sns

# %matplotlib inline
import matplotlib.pyplot as plt
sns.set(context='paper', font='monospace')

# Get Match data
df_match = pd.read_csv('data/match.csv', memory_map=True)
# Drop unneeded cols
df_match.drop(['start_time',
    'tower_status_radiant',
    'tower_status_dire',
    'barracks_status_radiant',
    'barracks_status_dire',
    'first_blood_time',
    'game_mode',
    'negative_votes',
    'positive_votes',
    'cluster'],
    axis=1)

# Get Chat Data
df_chat = pd.read_csv('data/chat.csv', memory_map=True)
# Drop unneeded cols
df_chat.drop('unit', axis=1)

# Create 
df_chat['team'] = pd.cut(df_chat['slot'],[0,5],labels=[True, False])
df_chat['nachlänge'] = df_chat['key'].str.len()
df_groupedchat = df_chat[['match_id', 'team', 'key']]
    .groupby(['match_id', 'team'])
    .count()
df_groupedchat = df_chat[['match_id', 'team', 'nachlänge']]
    groupby(['match_id', 'team'])
    .sum()

# Adding Total Messages/ match
df_match['Total_Messages'] = df_chat[['match_id','key']]
    .groupby('match_id')
    .count()

