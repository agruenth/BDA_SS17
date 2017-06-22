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
df_groupedchat['MessagesPerMinute'] = df_groupedchat['key']/(df_groupedchat['duration']/60)
df_groupedchat_win = df_groupedchat[df_groupedchat['rad_win']==df_groupedchat['radiant_win']]
df_groupedchat_lose = df_groupedchat[df_groupedchat['rad_win']!=df_groupedchat['radiant_win']]
df_groupedchat_win.drop('rad_win',axis=1, inplace=True)
df_groupedchat_lose.drop('rad_win',axis=1, inplace=True)

# df_groupedchat_win['MessagesPerMinute'] = df_groupedchat_win['key']/(df_groupedchat_win['duration']/60)
# Calculate the Winrate depending on Messages per minute
print('Ziel\n----------\n Das Ziel hier ist, den Unterschied zwischen einem gewinnenden Team und einem verlierenden Team in Nachrichten pro Minute aufzuzeigen')
winners = df_groupedchat_win
losers = df_groupedchat_lose

winners['Bereiche'] = pd.cut(winners['MessagesPerMinute'],[x*x/4 for x in range(7)])
losers['Bereiche'] = pd.cut(losers['MessagesPerMinute'],[x*x/4 for x in range(7)])

grouped_data = winners[['Bereiche','MessagesPerMinute']].groupby('Bereiche').sum()
grouped_data['losers'] = losers[['Bereiche','MessagesPerMinute']].groupby('Bereiche').sum()
grouped_data.columns = ['winners_characters', 'losers_characters']

grouped_data['winners_games'] = winners[['Bereiche', 'MessagesPerMinute']].groupby('Bereiche').count()
grouped_data['losers_games'] = losers[['Bereiche', 'MessagesPerMinute']].groupby('Bereiche').count()

grouped_data['winners'] = grouped_data['winners_characters']/grouped_data['winners_games']
grouped_data['losers'] = grouped_data['losers_characters']/grouped_data['losers_games']

grouped_data['results'] = grouped_data['winners_games']-grouped_data['losers_games']
grouped_data['results_%'] = 100*(grouped_data['winners_games']-grouped_data['losers_games'])/(grouped_data['winners_games']+grouped_data['losers_games'])

grouped_data['winrate_difference'] = grouped_data['winners_games']/(grouped_data['winners_games']+grouped_data['losers_games'])

bplot = sns.barplot(
    x = grouped_data.index,
    y = grouped_data.winrate_difference)
bplot.set(xlabel='Nachrichten Pro Minute', ylabel='Winrate')
bplot.get_figure().savefig('NpM_vs_Winrate.png') 

print(grouped_data)
print('\nInterpretation\n----------\nWeniger chatten ist nicht immer positiv. Es ist zwar deutlich sichtbar, dass in den meisten Fällen eine geringere Beteiligung am Chat hilfreich ist, jedoch zeigt sich, dass ein geringer Austausch von Informationen eine bessere Chance auf Sieg gibt. Denn keine Teamarbeit bringt das Spiel auch nicht voran.')
print('\nGraphik\n----------\nDie Daten als Säulendiagramm sind unter NpM_vs_Winrate.png zu finden.')

# Calculate the average messages for each players kda
print('\n\nZiel\n----------\nBerechnung der Durchschnittlichen Nachrichtenlänge und Nachrichtenanzahl abhängig von der Spieler KDA.')
df_player = pd.read_csv('data/players.csv', memory_map=True)
df_player.drop([
    'account_id',
    'gold',
    'gold_spent',
    'gold_per_min',
    'xp_per_min',
    'denies',
    'last_hits',
    'stuns',
    'hero_damage',
    'hero_healing',
    'tower_damage',
    'item_0',
    'item_1',
    'item_2',
    'item_3',
    'item_4',
    'item_5',
    'level',
    'leaver_status',
    'xp_hero',
    'xp_creep',
    'xp_roshan',
    'xp_other',
    'gold_other',
    'gold_death',
    'gold_buyback',
    'gold_abandon',
    'gold_sell',
    'gold_destroying_structure',
    'gold_killing_heros',
    'gold_killing_creeps',
    'gold_killing_roshan',
    'gold_killing_couriers',
    'unit_order_none',
    'unit_order_move_to_position',
    'unit_order_move_to_target',
    'unit_order_attack_move',
    'unit_order_attack_target',
    'unit_order_cast_position',
    'unit_order_cast_target',
    'unit_order_cast_target_tree',
    'unit_order_cast_no_target',
    'unit_order_cast_toggle',
    'unit_order_hold_position',
    'unit_order_train_ability',
    'unit_order_drop_item',
    'unit_order_give_item',
    'unit_order_pickup_item',
    'unit_order_pickup_rune',
    'unit_order_purchase_item',
    'unit_order_sell_item',
    'unit_order_disassemble_item',
    'unit_order_move_item',
    'unit_order_cast_toggle_auto',
    'unit_order_stop',
    'unit_order_taunt',
    'unit_order_buyback',
    'unit_order_glyph',
    'unit_order_eject_item_from_stash',
    'unit_order_cast_rune',
    'unit_order_ping_ability',
    'unit_order_move_to_direction',
    'unit_order_patrol',
    'unit_order_vector_target_position',
    'unit_order_radar',
    'unit_order_set_item_combine_lock',
    'unit_order_continue'], axis=1, inplace=True)
print(df_player.head())
df_player['player_slot_fixed'] = df_player['player_slot'].map(lambda x: x-123 if x>5 else x)
df_chatgrouped = df_chat['match_id','slot','nachlänge'].groupby(['match_id', 'slot'])
print(df_chat.head())
print(df_chatgrouped.head())



import sys
sys.exit()
df_groupedchat_win['Bereiche Duration'] = pd.cut(
    df_groupedchat_win['duration'],
    [x*300 for x in range(21)],
    labels=[x*5 for x in range(1,21)])

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
    .get_figure().savefig('plot.png')


sns.barplot(
    x='Bereiche Duration',
    y='nachlänge',
    data = df_groupedchat_win)\
    .get_figure().savefig('plot.png')

