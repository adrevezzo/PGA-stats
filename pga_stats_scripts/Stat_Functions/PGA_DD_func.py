import requests
import lxml.html as lh
import pandas as pd
import datetime
from scipy import stats
from bs4 import BeautifulSoup


def pga_dd(url_num,trny_name,year,day_offset,path):
    url = f'https://www.pgatour.com/content/pgatour/stats/stat.101.y{year}.eoff.{url_num}.html'
    page = requests.get(url)
    text = page.text
    soup = BeautifulSoup(text, 'lxml')

    headers = []
    stat_headers = soup.find_all('th')

    for header in stat_headers:
        headers.append(header.get_text())

    players = []

    stat_players = soup.select('td a')[1:]

    for player in stat_players:
        players.append(player.get_text())

    stats = soup.find_all(class_="hidden-small hidden-medium")
    categories = 3

    # Initialize stats list
    stat_list = []

    # Loop through
    for i in range(1, len(stats) - categories + 1, categories):
        temp_list = []
        for j in range(categories):
            temp_list.append(stats[i + j].get_text())
        stat_list.append(temp_list)

    player_dict = {}

    # Loop through player list
    for i, player in enumerate(players):
        # print(player_dict)
        player_dict[player] = stat_list[i]

    #trny = soup.select('option')[46].get_text()
    trny = trny_name


    # Create Dataframe, add headers, replace thousands separator
    dd = pd.DataFrame(player_dict).T
    dd.columns = ['ROUNDS', 'TOTAL DISTANCE', 'TOTAL DRIVES']
    dd.index.name = headers[2]
    dd = dd.replace({',': ''}, regex=True)

    # Insert Column for the Week Of
    today = datetime.date.today()
    #last_monday = today - datetime.timedelta(days=today.weekday() + day_offset+1)
    # coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    #dd['WEEK OF'] = last_monday
    #dd['WEEK OF'] = day_offset.date()

    # Calculate Avg Drive
    dd['TOTAL DISTANCE'] = pd.to_numeric(dd['TOTAL DISTANCE'])
    dd['TOTAL DRIVES'] = pd.to_numeric(dd['TOTAL DRIVES'])
    dd['AVG DISTANCE'] = round(dd['TOTAL DISTANCE'] / dd['TOTAL DRIVES'],4)
    dd.sort_values(by=['AVG DISTANCE'], ascending=False, inplace=True)
    dd['DD RANK'] = dd['AVG DISTANCE'].rank(ascending=0)
    # dd['DD PERCENTILE'] = dd.apply(lambda x: stats.percentileofscore(dd['AVG DISTANCE'], x, kind='rank'))
    dd['DD PERCENTILE'] = round(dd['AVG DISTANCE'].rank(pct=True),4)
    dd['THRU TOURNAMENT'] = trny
    dd['DD VALUE'] = dd['AVG DISTANCE']
    dd['SCHEDULE YEAR'] = year

    dd.to_csv(fr"{path}\DD_{day_offset.date()}.csv")





