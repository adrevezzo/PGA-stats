import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import datetime


def pga_sgapp(url_num, trny_name, year, day_offset, path):
    url = f'https://www.pgatour.com/content/pgatour/stats/stat.02568.y{year}.eoff.{url_num}.html'
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


    # Create Dataframe, add headers, replace thousands separator
    sgapp = pd.DataFrame(player_dict).T
    sgapp.columns = [headers[3], headers[5], headers[6]]
    sgapp.index.name = headers[2]
    sgapp = sgapp.replace({',': ''}, regex=True)

    # Insert Column for the Week Of
    today = datetime.date.today()
    #last_monday = today - datetime.timedelta(days=today.weekday() + day_offset+1)
    # coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    #sgapp['WEEK OF'] = last_monday
    sgapp['WEEK OF'] = day_offset.date()

    # Calculations
    sgapp[['ROUNDS', 'TOTAL SG:APP', 'MEASURED ROUNDS']] = sgapp[['ROUNDS', 'TOTAL SG:APP', 'MEASURED ROUNDS']].apply(
        pd.to_numeric, axis=1)
    sgapp['SGAPP VALUE'] = round(sgapp['TOTAL SG:APP'] / sgapp['MEASURED ROUNDS'],4)
    sgapp.sort_values(by=['SGAPP VALUE'], ascending=False, inplace=True)
    sgapp['SGAPP RANK'] = sgapp['SGAPP VALUE'].rank(ascending=0)
    sgapp['SGAPP PERCENTILE'] = round(sgapp['SGAPP VALUE'].rank(pct=True),4)
    sgapp['THRU TOURNAMENT'] = trny
    sgapp['SCHEDULE YEAR'] = year
    # print(sgapp.head())

    sgapp.to_csv(fr"{path}\SGAPP_{day_offset.date()}.csv")

