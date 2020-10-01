from datetime import datetime
from datetime import timedelta


def get_ranking_diff(winner_rank, loser_rank):
    return winner_rank - loser_rank


def calculate_player_win_ratio(player, matches, surface='All', tournament='All', last_year_only=False,
                               data_collected='Matches'):
    if surface != 'All':
        matches = matches[matches['Surface'] == surface]

    if tournament != 'All':
        matches = matches[matches['Tournament'] == tournament]

    if last_year_only:
        matches = matches[matches['Date'] >= '2019/01/01']

    if data_collected == 'Matches':
        wins = (matches['Winner'] == player).sum()
        losses = (matches['Loser'] == player).sum()
        if wins + losses <= 5:
            return 0.5


    elif data_collected == 'Sets':
        wins = matches[matches['Winner'] == player]['Wsets'].sum() + matches[matches['Loser'] == player][
            'Lsets'].sum()
        losses = matches[matches['Winner'] == player]['Lsets'].sum() + matches[matches['Loser'] == player][
            'Wsets'].sum()

        if wins + losses <= 15:
            return 0.5

    return wins / (wins + losses)


def calculate_player_win_ratio_h2h(player1, player2, matches, surface='All', tournament='All', last_year_only=False,
                                   data_collected='Matches'):
    if surface != 'All':
        matches = matches[matches['Surface'] == surface]

    if tournament != 'All':
        matches = matches[matches['Tournament'] == tournament]

    if last_year_only:
        matches = matches[matches['Date'] >= '2019/01/01']

    if data_collected == 'Matches':
        wins = ((matches['Winner'] == player1) & (matches['Loser'] == player2)).sum()
        losses = ((matches['Winner'] == player2) & (matches['Loser'] == player1)).sum()

    elif data_collected == 'Sets':

        wins = matches[(matches['Winner'] == player1) & (matches['Loser'] == player2)]['Wsets'].sum() + \
               matches[(matches['Winner'] == player2) & (matches['Loser'] == player1)]['Lsets'].sum()

        losses = matches[(matches['Winner'] == player1) & (matches['Loser'] == player2)]['Lsets'].sum() + \
                 matches[(matches['Winner'] == player2) & (matches['Loser'] == player1)]['Wsets'].sum()

    # if never played each other
    if wins + losses == 0:
        return 0.6

    return wins / (wins + losses)


def get_higher_ranked_player(player1, rank1, player2, rank2):
    if rank1 < rank2:
        return player1
    return player2


def get_higher_rank(rank1, rank2):
    return min(rank1, rank2)


def get_lower_ranked_player(player1, rank1, player2, rank2):
    if rank1 < rank2:
        return player2
    return player1


def get_lower_rank(rank1, rank2):
    return max(rank1, rank2)


def get_result(winner_rank, loser_rank):
    # 1 if the favourite (higher ranked player) won the game, 0 otherwise
    if winner_rank < loser_rank:
        return 1
    return 0


def get_favourite_odds(odd1, rank1, odd2, rank2):
    if rank1 < rank2:
        return odd1
    return odd2


def get_underdog_odds(odd1, rank1, odd2, rank2):
    if rank1 < rank2:
        return odd2
    return odd1


def generate_attributes(supervised_matches, all_matches):
    supervised_matches.loc[:, 'player_0_match_win_ratio_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_0'], all_matches, surface='Hard'),
        axis=1)

    supervised_matches.loc[:, 'player_1_match_win_ratio_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_1'], all_matches, surface='Hard'),
        axis=1)

    print("Overall Stat On Hard Done")

    supervised_matches.loc[:, 'player_0_match_win_ratio_ao'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_0'], all_matches, tournament='Australian Open'),
        axis=1)

    supervised_matches.loc[:, 'player_1_match_win_ratio_ao'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_1'], all_matches, tournament='Australian Open'),
        axis=1)

    print("Overall Stat Australian Open Done")

    supervised_matches.loc[:, 'player_0_match_win_ratio_last_year'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_0'], all_matches, last_year_only=True),
        axis=1)

    supervised_matches.loc[:, 'player_1_match_win_ratio_last_year'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_1'], all_matches, last_year_only=True),
        axis=1)

    print("Last Year Stats Done")

    supervised_matches.loc[:, 'player_0_match_win_ratio_last_year_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_0'], all_matches, surface='Hard', last_year_only=True),
        axis=1)

    supervised_matches.loc[:, 'player_1_match_win_ratio_last_year_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_1'], all_matches, surface='Hard', last_year_only=True),
        axis=1)

    supervised_matches.loc[:, 'player_0_set_win_ratio_last_year_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_0'], all_matches, surface='Hard', last_year_only=True,
                                               data_collected='Sets'),
        axis=1)

    supervised_matches.loc[:, 'player_1_set_win_ratio_last_year_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio(row['player_1'], all_matches, surface='Hard', last_year_only=True,
                                               data_collected='Sets'),
        axis=1)

    print("Last Year Stats on Hard Done")

    supervised_matches.loc[:, 'player_0_match_win_ratio_hh'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio_h2h(row['player_0'], row['player_1'], all_matches), axis=1)

    print("Overall H2H Done")

    supervised_matches.loc[:, 'player_0_match_win_ratio_hh_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio_h2h(row['player_0'], row['player_1'], all_matches, surface='Hard'),
        axis=1)

    supervised_matches.loc[:, 'player_0_set_win_ratio_hh_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio_h2h(row['player_0'], row['player_1'], all_matches, surface='Hard',
                                                   data_collected='Sets'), axis=1)

    print("Overall H2H on Hard Done")

    supervised_matches.loc[:, 'player_0_match_win_ratio_hh_ao'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio_h2h(row['player_0'], row['player_1'], all_matches,
                                                   tournament='Australian Open'),
        axis=1)

    supervised_matches.loc[:, 'player_0_match_win_ratio_hh_last_year'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio_h2h(row['player_0'], row['player_1'], all_matches,
                                                   last_year_only=True),
        axis=1)

    supervised_matches.loc[:, 'player_0_set_win_ratio_hh_last_year'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio_h2h(row['player_0'], row['player_1'], all_matches,
                                                   last_year_only=True,
                                                   data_collected='Sets'),
        axis=1)

    print("Overall H2H on Australian Open Done")

    supervised_matches.loc[:, 'player_0_match_win_ratio_hh_last_year_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio_h2h(row['player_0'], row['player_1'], all_matches,
                                                   surface='Hard',
                                                   last_year_only=True),
        axis=1)

    supervised_matches.loc[:, 'player_0_set_win_ratio_hh_last_year_hard'] = supervised_matches.apply(
        lambda row: calculate_player_win_ratio_h2h(row['player_0'], row['player_1'], all_matches,
                                                   surface='Hard',
                                                   last_year_only=True, data_collected='Sets'),
        axis=1)

    supervised_matches.loc[:, 'diff_match_win_ratio_hard'] = 0.5 + (
            (supervised_matches['player_0_match_win_ratio_hard'] - \
             supervised_matches[
                 'player_1_match_win_ratio_hard']) / 2)

    supervised_matches.loc[:, 'diff_match_win_ratio_ao'] = 0.5 + ((supervised_matches['player_0_match_win_ratio_ao'] - \
                                                                   supervised_matches[
                                                                       'player_1_match_win_ratio_ao']) / 2)

    supervised_matches.loc[:, 'diff_match_win_ratio_last_year'] = 0.5 + ((supervised_matches[
                                                                              'player_0_match_win_ratio_last_year'] - \
                                                                          supervised_matches[
                                                                              'player_1_match_win_ratio_last_year']) / 2)

    supervised_matches.loc[:, 'diff_match_win_ratio_last_year_hard'] = 0.5 + ((supervised_matches[
                                                                                   'player_0_match_win_ratio_last_year_hard'] - \
                                                                               supervised_matches[
                                                                                   'player_1_match_win_ratio_last_year_hard']) / 2)
    supervised_matches.loc[:, 'diff_set_win_ratio_last_year_hard'] = 0.5 + ((supervised_matches[
                                                                                 'player_0_set_win_ratio_last_year_hard'] - \
                                                                             supervised_matches[
                                                                                 'player_1_set_win_ratio_last_year_hard']) / 2)

    print("Done with calculating final attributes")
    return supervised_matches
