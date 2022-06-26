import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import datetime


def pga_sgt2g(url_num,trny_name,year,day_offset,path):
    url = f'https://www.pgatour.com/content/pgatour/stats/stat.02674.y{year}.eoff.{url_num}.html'
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
    categories = 5

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
        # print(player_dict)
        player_dict[player] = stat_list[i]

    # trny = soup.select('option')[22].get_text()
    trny = trny_name
    #print(trny)

    # Create Dataframe, add headers, replace thousands separator
    sgt2g = pd.DataFrame(player_dict).T
    sgt2g.columns = [headers[3], headers[5], headers[6], headers[7], headers[8]]
    sgt2g.index.name = headers[2]
    sgt2g = sgt2g.replace({',': ''}, regex=True)

    # Insert Column for the Week Of
    today = datetime.date.today()
    #last_monday = today - datetime.timedelta(days=today.weekday() + day_offset+1)
    # coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    #sgt2g['WEEK OF'] = last_monday
    sgt2g['WEEK OF'] = day_offset.date()

    # Calculations
    sgt2g[['ROUNDS', 'SG:OTT', 'SG:APR', 'SG:ARG', 'MEASURED ROUNDS']] = sgt2g[
        ['ROUNDS', 'SG:OTT', 'SG:APR', 'SG:ARG', 'MEASURED ROUNDS']].apply(pd.to_numeric, axis=1)
    sgt2g['SGTTG VALUE'] = round(sgt2g['SG:OTT'] + sgt2g['SG:APR'] + sgt2g['SG:ARG'],4)
    sgt2g.sort_values(by=['SGTTG VALUE'], ascending=False, inplace=True)
    sgt2g['SGTTG RANK'] = sgt2g['SGTTG VALUE'].rank(ascending=0)
    sgt2g['SGTTG PERCENTILE'] = round(sgt2g['SGTTG VALUE'].rank(pct=True),4)
    sgt2g['THRU TOURNAMENT'] = trny
    sgt2g['SCHEDULE YEAR'] = year
    # print(sgt2g.head())

    sgt2g.to_csv(fr"{path}\SGTTG_{day_offset.date()}.csv")


