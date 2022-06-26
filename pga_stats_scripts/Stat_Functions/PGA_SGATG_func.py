import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import datetime

def pga_sgatg(url_num,trny_name,year,day_offset,path):
    url = f'https://www.pgatour.com/content/pgatour/stats/stat.02569.y{year}.eoff.{url_num}.html'
    page = requests.get(url)
    text = page.text
    soup = BeautifulSoup(text, 'lxml')

    headers = []
    stat_headers = soup.find_all('th')

    for header in stat_headers:
        headers.append(header.get_text())

    players = []

    stat_players = soup.select('td a')[1:]
    # print(stat_players)

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
        # print(player_dict)
        player_dict[player] = stat_list[i]

    trny = trny_name
    #print(trny)

    # Create Dataframe, add headers, replace thousands separator
    atg = pd.DataFrame(player_dict).T
    atg.columns = [headers[3], headers[5], headers[6]]
    atg.index.name = headers[2]
    atg = atg.replace({',': ''}, regex=True)
    # print(atg.head())

    # Insert Column for the Week Of
    today = datetime.date.today()
    #last_monday = today - datetime.timedelta(days=today.weekday() + day_offset+1)
    # coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    #atg['WEEK OF'] = last_monday
    atg['WEEK OF'] = day_offset.date()

    # Calculations
    atg[['ROUNDS', 'TOTAL SG:ARG', 'MEASURED ROUNDS']] = atg[['ROUNDS', 'TOTAL SG:ARG', 'MEASURED ROUNDS']].apply(
        pd.to_numeric, axis=1)
    atg['SGATG VALUE'] = round(atg['TOTAL SG:ARG'] / atg['MEASURED ROUNDS'],4)
    atg.sort_values(by=['SGATG VALUE'], ascending=False, inplace=True)
    atg['SGATG RANK'] = atg['SGATG VALUE'].rank(ascending=0)
    atg['SGATG PERCENTILE'] = round(atg['SGATG VALUE'].rank(pct=True),4)
    atg['THRU TOURNAMENT'] = trny
    atg['SCHEDULE YEAR'] = year

    atg.to_csv(fr"{path}\SGATG_{day_offset.date()}.csv")
