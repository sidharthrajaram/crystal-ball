import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib.request
import numpy as np

header = []

def getPlayerDataFrame(name):
    global header

    player_name = name.lower()
    ln_fi = player_name.find(' ') + 1  # index of first initial of last name
    first = player_name[:2]
    last = player_name[ln_fi:ln_fi + 5]

    url = "https://www.basketball-reference.com/players/" + player_name[ln_fi] + "/" + last + first + "01.html"
    if(name=='Anthony Davis'):
        url = "https://www.basketball-reference.com/players/d/davisan02.html"

    with urllib.request.urlopen(url) as response:
        # UTF-8 doesn't support some initial character on the websites for some reason!
        r = response.read().decode('latin-1')

    content = re.sub(r'(?m)^\<!--.*\n?', '', r)
    content = re.sub(r'(?m)^\-->.*\n?', '', content)

    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.findAll('table')
    table = tables[1]

    df = pd.read_html(str(table))[0]
    header = df.columns.values.tolist()
    return df

def getTwoYearTotals(df):

    last_year = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-2])))

    if len(df['Season']) > 2:
        #not a rookie
        last_last_year = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-3] )))
        return [True, last_year, last_last_year]
    else:
        #rookie
        return [False, last_year]

name = input('Player name: ')
df = getPlayerDataFrame(name)
print(getTwoYearTotals(df))
# latest_stats = df.iloc[-2]
# latest_stats = np.array(list(filter(lambda a: str(a) != 'nan', latest_stats)))
# print(latest_stats)