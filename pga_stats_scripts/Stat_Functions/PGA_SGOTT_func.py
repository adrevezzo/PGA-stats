import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import datetime


def pga_sgott(url_num,trny_name,year,day_offset,path):
    url = f'https://www.pgatour.com/content/pgatour/stats/stat.02567.y{year}.eoff.{url_num}.html'
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
    #print(trny)

    # Create Dataframe, add headers, replace thousands separator
    sgott = pd.DataFrame(player_dict).T
    sgott.columns = [headers[3], headers[5], headers[6]]
    sgott.index.name = headers[2]
    sgott = sgott.replace({',': ''}, regex=True)

    # Insert Column for the Week Of
    today = datetime.date.today()
    #last_monday = today - datetime.timedelta(days=today.weekday() + day_offset+1)
    # coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    #sgott['WEEK OF'] = last_monday
    sgott['WEEK OF'] = day_offset.date()

    # Calculations
    sgott[['ROUNDS', 'TOTAL SG:OTT', 'MEASURED ROUNDS']] = sgott[['ROUNDS', 'TOTAL SG:OTT', 'MEASURED ROUNDS']].apply(
        pd.to_numeric, axis=1)
    sgott['SGOTT VALUE'] = round(sgott['TOTAL SG:OTT'] / sgott['MEASURED ROUNDS'],4)
    sgott.sort_values(by=['SGOTT VALUE'], ascending=False, inplace=True)
    sgott['RANK'] = sgott['SGOTT VALUE'].rank(ascending=0)
    sgott['SGOTT PERCENTILE'] = round(sgott['SGOTT VALUE'].rank(pct=True),4)
    sgott['THRU TOURNAMENT'] = trny
    sgott['SCHEDULE YEAR'] = year
    # print(sgott.head())

    sgott.to_csv(fr"{path}\SGOTT_{day_offset.date()}.csv")




    
         