import glob
import pandas as pd
from functions import *
from datetime import datetime

all_matches = pd.DataFrame()

# All tennis matches for last 10 years into single dataframe
for file in glob.glob("tennis-data/20*.xlsx"):
    current_file = pd.read_excel(file)
    all_matches = all_matches.append(current_file, ignore_index=True, sort=False)

all_matches = all_matches[all_matches.Comment == 'Completed']

all_matches.reset_index(inplace=True)

# Fills the missing values (e.g. in the missing sets)
all_matches = all_matches.fillna(0)

all_matches['Date'] = all_matches.apply(
    lambda row: datetime.strptime(str(row['Date']), "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d"), axis=1)

supervised_matches = all_matches[['Tournament',  'Date', 'Surface']].copy()

supervised_matches.loc[:, 'player_0'] = all_matches.apply(
    lambda row: get_higher_ranked_player(row['Winner'], row['WRank'], row['Loser'], row['LRank']), axis=1)
supervised_matches.loc[:, 'Higher_rank'] = all_matches.apply(
    lambda row: get_higher_rank(row['WRank'], row['LRank']), axis=1)
supervised_matches.loc[:, 'player_1'] = all_matches.apply(
    lambda row: get_lower_ranked_player(row['Winner'], row['WRank'], row['Loser'], row['LRank']), axis=1)
supervised_matches.loc[:, 'Lower_rank'] = all_matches.apply(lambda row: get_lower_rank(row['WRank'], row['LRank']),
                                                            axis=1)

supervised_matches.loc[:, 'result'] = all_matches.apply(lambda row: get_result(row['WRank'], row['LRank']), axis=1)

majors = ['Australian Open', 'French Open', 'US Open', 'Wimbledon', 'Masters Cup']
supervised_matches = supervised_matches[supervised_matches['Tournament'].isin(majors)]

supervised_matches = generate_attributes(supervised_matches, all_matches)

all_matches.to_csv('all_matches.csv', index=False)

supervised_matches.to_csv("supervised_matches.csv", index=False)
