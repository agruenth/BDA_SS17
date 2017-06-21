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
    axis=1,
    inplace=True)
# Get Chat Data
df_chat = pd.read_csv('data/chat.csv', memory_map=True)
# Drop unneeded cols
df_chat.drop('unit', axis=1, inplace=True)

# Create 
df_chat['team'] = pd.cut(df_chat['slot'],[0, 5, 10],labels=[True, False])
df_chat['nachlänge'] = df_chat['key'].str.len()
df_groupedchat = df_chat[['match_id', 'team', 'key']]\
    .groupby(['match_id', 'team'])\
    .count()
df_groupedchat['nachlänge'] = df_chat[['match_id', 'team', 'nachlänge']]\
    .groupby(['match_id', 'team'])\
    .sum()
df_groupedchat['avglength'] = df_groupedchat['nachlänge']/df_groupedchat['key']
df_groupedchat['match_id'] = [x[0] for x in list(df_groupedchat.index.values)]
df_groupedchat['rad_win'] = [x[1] for x in list(df_groupedchat.index.values)]
df_groupedchat = df_groupedchat.merge(df_match, on='match_id')
df_groupedchat_win = df_groupedchat[df_groupedchat['rad_win']==df_groupedchat['radiant_win']]
df_groupedchat_lose = df_groupedchat[df_groupedchat['rad_win']!=df_groupedchat['radiant_win']]
df_groupedchat_win.drop('rad_win',axis=1, inplace=True)
df_groupedchat_lose.drop('rad_win',axis=1, inplace=True)

df_groupedchat_win['MessagesPerMinute'] = df_groupedchat_win['key']/(df_groupedchat_win['duration']/60)
df_groupedchat_win['Bereiche Duration'] = pd.cut(df_groupedchat_win['duration'],[x*300 for x in range(21)], labels=[x*5 for x in range(1,21)])
print("Groupedchat")
print(df_groupedchat.head())
print("WIN only")
print(df_groupedchat_win.head())
print("LOSE only")
print(df_groupedchat_lose.head())
print(df_groupedchat_win.groupby('Bereiche Duration').count())

sns.stripplot(
    x='Bereiche Duration',
    y='nachlänge',
    data = df_groupedchat_win)\
    .get_figure().savefig('plot-png')


sns.barplot(
    x='Bereiche Duration',
    y='nachlänge',
    data = df_groupedchat_win)\
    .get_figure().savefig('plot-png')

