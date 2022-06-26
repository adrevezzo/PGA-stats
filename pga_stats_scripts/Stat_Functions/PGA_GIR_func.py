import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import datetime


def pga_gir(url_num,trny_name,year,day_offset,path):
    url = f'https://www.pgatour.com/content/pgatour/stats/stat.103.y{year}.eoff.{url_num}.html'
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
    categories = 4
    # print(stats)

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
    gir = pd.DataFrame(player_dict).T
    gir.columns = [headers[3], headers[5], headers[6], headers[7]]
    gir.index.name = headers[2]
    gir = gir.replace({',': ''}, regex=True)

    # Insert Column for the Week Of
    today = datetime.date.today()
    #last_monday = today - datetime.timedelta(days=today.weekday() + day_offset+1)
    # coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    #gir['WEEK OF'] = last_monday
    gir['WEEK OF'] = day_offset.date()

    # Calculation
    gir[['ROUNDS', 'GREENS HIT', '# HOLES']] = gir[
        ['ROUNDS', 'GREENS HIT', '# HOLES']].apply(pd.to_numeric, axis=1)
    gir['GIR PCNT'] = round(gir['GREENS HIT'] / gir['# HOLES'],4)
    gir.sort_values(by=['GIR PCNT'], ascending=False, inplace=True)
    gir['GIR RANK'] = gir['GIR PCNT'].rank(ascending=0)
    gir['GIR PERCENTILE'] = round(gir['GIR PCNT'].rank(pct=True),4)
    gir['THRU TOURNAMENT'] = trny
    gir['GIR VALUE'] = gir['GIR PCNT']
    gir['SCHEDULE YEAR'] = year
    # print(gir.head())

    gir.to_csv(fr"{path}\GIR_{day_offset.date()}.csv")
