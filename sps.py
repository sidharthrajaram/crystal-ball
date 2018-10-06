import numpy as np
from scraper import getPlayerDataFrame

header = []
starting_stat = 'G'
ending_stat = 'PTS'

def getTwoYearTotals(df):

    last_year = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-2])))

    if len(df['Season']) > 2:
        #not a rookie
        last_last_year = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-3] )))
        return [True, last_year, last_last_year]
    else:
        #rookie
        return [False, last_year]

#stat_tuple and stat (string)
def predictStat(stat_tuple, stat):
    stat_index = header.index(stat)
    min_index = header.index('MP')
    age = float(stat_tuple[1][header.index('Age')])+1

    last_year_totals = stat_tuple[1]
    last_year_stat = float(last_year_totals[stat_index])
    last_year_mins = float(last_year_totals[min_index])

    if stat_tuple[0] == True:

        last_last_year_totals = stat_tuple[2]
        last_last_year_stat = float(last_last_year_totals[stat_index])
        last_last_year_mins = float(last_last_year_totals[min_index])

        mp_weighted_sum = float(6*last_year_mins + 3*last_last_year_mins)
        stat_weighted_sum = float(6*last_year_stat + 3*last_last_year_stat)

        predicted_per36 = (stat_weighted_sum / mp_weighted_sum) * 36

        #this area can be far more advanced
        if age<=28:
            adjustment = (28 - age) * 0.004
        else:
            adjustment = (28 - age) * 0.002

        predicted_stat = (1 + adjustment) * predicted_per36

    else:
        #to be improved
        adjustment = (28-age)*0.004
        predicted_stat = (1+adjustment)* ((last_year_stat/last_year_mins) * 36)

    return round(predicted_stat, 2)


def getStatline(stat_tuple):
    statline = []
    first_stat_index = header.index(starting_stat)
    last_stat_index = header.index(ending_stat)

    for i in range(first_stat_index):
        statline.append(stat_tuple[1][i])

    n = first_stat_index
    while n <= last_stat_index:
        statline.append(predictStat(stat_tuple, header[n]))
        n += 1
    return statline

def predict(name):
    global header
    player_data = getPlayerDataFrame(name)
    df = player_data[0]
    header = player_data[1]
    stat_tuple = getTwoYearTotals(df)
    statline = getStatline(stat_tuple)
    return statline
