import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

def ccc(crosstab):
    chi2 = stats.chi2_contingency(crosstab)[0]
    q = min(crosstab.shape)
    if q > 1:
        return np.sqrt(chi2 / (chi2 + crosstab.values.sum())) * np.sqrt(q / (q-1))
    else:
        return 0

pd.set_option('expand_frame_repr', False)
print(pd.get_option('display.max_columns'))

df_player = pd.read_csv('data/players.csv', memory_map=True)
df_match = pd.read_csv('data/match.csv', memory_map=True)
df_chat = pd.read_csv("data/chat.csv", memory_map=True)

df_abbr = pd.read_csv('list.csv', memory_map=True)


df_abbr.applymap(lambda x: str(x).lower())


df_chat.drop([
    'unit',
    'time',],
    axis=1,
    inplace=True)

df_match.drop([
    'start_time',
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

df_player = df_player.merge(df_match, on='match_id')

# KDA with Formular (Kills + 0.5 Assists)/Deaths
df_player['KDA'] = (df_player.kills + 0.5* df_player.assists) / df_player.deaths

df_player.rename(columns={'radiant_win':'GewinnerSeite'}, inplace=True)
# True False ersetzt durch 0 und 1
df_player.GewinnerSeite = df_player.GewinnerSeite.map(lambda x: 0 if x else 1)

# Chat Spalten hinzugefügt
df_chat['NachrichtenLänge'] = df_chat['key'].map(lambda x: len(str(x)))
df_chat['Wörter'] = df_chat['key'].map(lambda x: len(str(x).split(' ')))
df_chat['player_slot'] = df_chat['slot'].map(lambda x: x+123 if x>4 else x)

# Daten Gruppiert
grouped = df_chat[['match_id','player_slot','key']].groupby(['match_id','player_slot']).count()

print(type(grouped))
grouped = grouped.reset_index()
grouped.rename(columns={'key':'Nachrichten'}, inplace=True)
grouped['Gesamtzeichen'] = df_chat[
    ['match_id', 'player_slot', 'NachrichtenLänge']
    ].groupby(['match_id', 'player_slot']).sum().reset_index()['NachrichtenLänge']
 
grouped['Wörter'] = df_chat[
    ['match_id', 'player_slot', 'Wörter']
    ].groupby(['match_id', 'player_slot']).sum().reset_index()['Wörter']
    
print(grouped.head())

# Gruppierte Daten merged mit restlichen Spielern
df_player_merged = df_player.merge(grouped, on=['match_id','player_slot'])

#df_chat_extended = df_chat
#import os
#list_messages = df_chat_extended.key.tolist()
#print("Total Messages: "+str(len(list_messages)))
#fixed_messages = []
#list_abbr = df_abbr['Abbr'].values.tolist()
#list_full = df_abbr['Full'].values.tolist()
#for index, entry in enumerate(list_messages):
#    os.system("clear")
#    print("Progress: "+str(index/len(list_messages)))
#    message = ""
#    lis = str(entry).split(' ')
#    for word in lis:
#        if str(word).lower() in list_abbr:
#            message +=" "+str(list_full[list_abbr.index(str(word).lower())])
#        else:
#            message += " "+str(word).lower()
#
#    fixed_messages.append(message)
#
#print(fixed_messages)

            
print(df_match.head())
print(df_player.head(10))
print(df_chat.head(10))
print(df_player_merged.head(10))
print(ccc(pd.crosstab(df_player_merged.KDA, df_player_merged.Gesamtzeichen)))
print(df_player_merged.corr(min_periods=5).applymap(lambda x: None if x<0.05 or x==1 else x))
#print(df_player_merged.groupby('KDA').shape)
#print(ccc(pd.crosstab(df_player.GewinnerSeite, df_player.KDA)))
#print(df_player[df_player.GewinnerSeite==1].corr().applymap(lambda x: None if x<0.05 or x==1 else x))
#print("\n\n")
#print(df_player[df_player.GewinnerSeite==0].corr().applymap(lambda x: None if x<0.05 or x==1 else x))
