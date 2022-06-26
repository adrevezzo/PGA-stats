import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import Comment
import lxml.html as lh
import numpy as np
import datetime


#Read in Player Dict
player_dict = pd.read_csv(fr'---ENTER LOCATION OF PLAYER DICTIONARY CREATED WITH THE IMAGE SCRAPE.PY FILE OR USER CREATED LIST OF PLAYER & PLAYER IDS----' )
years = ['2022']#,'2021','2020','2019','2018','2017','2016','2015','2014','2013','2012']


for year in years:
    tot_results = []
    for index, row in player_dict.iterrows():
        p_name = row['Player Name Dict']
        p_id = row['ID Number']
        # WARNING: The API may now be closed to public access
        j_son = f'https://statdata-api-prod.pgatour.com/api/clientfile/YtdResultsArchive?P_ID={p_id}&YEAR={year}&format=json'
        page = requests.get(j_son)
        page.raise_for_status()
        text = json.loads(page.text)

        # Check if player in player_dict has results for given year.
        try:
            details = (text['plrs'][0]['tours'][0]['trnDetails'])

        except:
            continue

        for i, trn in enumerate(details):
            temp_list = []
            end_Date = details[i]['endDate']
            trn_name = details[i]['trn']['trnName']
            trn_num = details[i]['trn']['trnNum']
            perm_num = details[i]['trn']['permNum']
            fin_pos = details[i]['finPos']['value']
            mny_earn = details[i]['offMoney']
            fedex_earn = details[i]['fedexEvtPts']
            fedex_rnk = details[i]['fedexRnkReg']
            score = details[i]['scr']['relToPar']

            temp_list = [p_name, end_Date, trn_name, trn_num, perm_num, fin_pos, mny_earn, fedex_earn, fedex_rnk, score]
            tot_results.append(temp_list)

    res = pd.DataFrame(tot_results,
                       columns=['Player Name', 'Tourny End Date', 'Tourny Name', 'Tourny Number', 'Perm Number',
                                'Result', 'Tourny Money Earned', 'Tourny FedEx Pts Earned',
                                'Tourny Fedex Ranking', 'Tourny Score'])


    res.set_index('Player Name', inplace=True)

    res.to_csv(fr"---ETNER FILE PATH TO SAVE ALL PLAYER RESULTS CSV----\Player Results_{year}_temp.csv")







