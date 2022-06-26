import requests
import lxml.html as lh
import pandas as pd
import datetime
from bs4 import BeautifulSoup


def pga_da(url_num,trny_name,year,day_offset,path):
    url = f'https://www.pgatour.com/content/pgatour/stats/stat.102.y{year}.eoff.{url_num}.html'
    page = requests.get(url)
    text = page.text
    soup = BeautifulSoup(text, 'lxml')

    headers = []
    stat_headers = soup.find_all('th')
    # print(stat_headers)

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
    for i in range(0, len(stats) - categories, categories):
        temp_list = []
        for j in range(categories):
            temp_list.append(stats[(i + 1) + j].get_text())
            # print(temp_list)
        stat_list.append(temp_list)

    player_dict = {}

    # Loop through player list
    for i, player in enumerate(players):
        player_dict[player] = stat_list[i]

    trny = trny_name
    #print(trny)

    # Create Dataframe, add headers, replace thousands separator
    da = pd.DataFrame(player_dict).T
    da.columns = [headers[3], headers[5], headers[6]]
    da.index.name = headers[2]
    da = da.replace({',': ''}, regex=True)

    # Insert Column for the Week Of
    today = datetime.date.today()
    #last_monday = today - datetime.timedelta(days=today.weekday() + day_offset+1)
    # coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    #da['WEEK OF'] = last_monday
    da['WEEK OF'] = day_offset.date()

    # Calculate %
    da['FAIRWAYS HIT'] = pd.to_numeric(da['FAIRWAYS HIT'])
    da['POSSIBLE FAIRWAYS'] = pd.to_numeric(da['POSSIBLE FAIRWAYS'])
    da['DA VALUE'] = round(da['FAIRWAYS HIT'] / da['POSSIBLE FAIRWAYS'],4)
    da.sort_values(by=['DA VALUE'], ascending=False, inplace=True)
    da['DA RANK'] = da['DA VALUE'].rank(ascending=0)
    da['DA PERCENTILE'] = round(da['DA VALUE'].rank(pct=True),4)
    da['THRU TOURNAMENT'] = trny
    da['SCHEDULE YEAR'] = year

    da.to_csv(fr"{path}\DA_{day_offset.date()}.csv")










