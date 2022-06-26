import requests
import lxml.html as lh
import pandas as pd
import datetime
from bs4 import BeautifulSoup

def pga_sgputt(url_num,trny_name,year,day_offset,path):
    url = f'https://www.pgatour.com/content/pgatour/stats/stat.02564.y{year}.eoff.{url_num}.html'
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

    #trny = soup.select('option')[22].get_text()
    trny = trny_name
    #print(trny)

    # Create Dataframe, add headers, replace thousands separator
    sgputt = pd.DataFrame(player_dict).T
    sgputt.columns = [headers[3], headers[5], headers[6]]
    sgputt.index.name = headers[2]
    sgputt = sgputt.replace({',': ''}, regex=True)
    # print(sgputt.head())

    # Insert Column for the Week Of
    today = datetime.date.today()
    # last_monday = today - datetime.timedelta(days=today.weekday() + day_offset+1)
    # coming_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    # sgputt['WEEK OF'] = last_monday
    sgputt['WEEK OF'] = day_offset.date()

    # Calculate SG Putting Avg
    sgputt[['ROUNDS', 'TOTAL SG:PUTTING', 'MEASURED ROUNDS']] = sgputt[
        ['ROUNDS', 'TOTAL SG:PUTTING', 'MEASURED ROUNDS']].apply(pd.to_numeric, axis=1)
    sgputt['SGPUTT VALUE'] = round(sgputt['TOTAL SG:PUTTING'] / sgputt['MEASURED ROUNDS'],4)
    sgputt.sort_values(by=['SGPUTT VALUE'], ascending=False, inplace=True)
    sgputt['SGPUTT RANK'] = sgputt['SGPUTT VALUE'].rank(ascending=0)
    sgputt['SGPUTT PERCENTILE'] = round(sgputt['SGPUTT VALUE'].rank(pct=True),4)
    sgputt['THRU TOURNAMENT'] = trny
    sgputt['SCHEDULE YEAR'] = year

    sgputt.to_csv(fr"{path}\SGPUTT_{day_offset.date()}.csv")






