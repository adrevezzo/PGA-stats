import requests
import pandas as pd
from bs4 import BeautifulSoup
import lxml.html as lh
import numpy as np
import datetime

url = 'https://www.pgatour.com/players.html'
page = requests.get(url)
text = page.text
soup = BeautifulSoup(text, 'lxml')

#**********Create Player Name Dictionary
temp_ids = []
temp_names = []

#Find all Player HREF Links
for link in soup.find_all(class_='player-link'):
    plink = link.get('href')

    #Find player ID Number from href link
    temp_id = plink.split('/players/player.')[1].split('.')[0]

    # Find player first name Number from href link
    temp_first = plink.split('.')[2].split('-')[0]

    # Find player last name from href link
    temp_last = plink.split('-')[1].split('.html')[0]

    # Create full player name capitalized
    temp_full = temp_first.capitalize() + " " + temp_last.capitalize()

    #Append names and ids to lists
    temp_ids.append(temp_id)
    temp_names.append(temp_full)

player_dict = dict(zip(temp_ids, temp_names))

#********* Get the Headshot Links
cards = soup.find_all(class_='player-image')

img_url = 'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,dpr_1.5,f_auto,g_face:center,h_230,q_auto,w_174'
#print(photo)

#initialize link and player id lists
imgs = []
p_id =[]

for image in cards:
    #Get Headshot Link
    link = img_url + "/" + image['data-src']

    #Get Player ID
    fname = link.split('/headshots_')[1].split('.png')[0]

    #Create List for Player Link Dataframe
    imgs.append(link)
    p_id.append(fname)

#Create Headshot Link Dataframe
df = pd.DataFrame({'Player ID': p_id, 'Headshot Link': imgs})
df['Player Name'] = df['Player ID'].map(player_dict)
#print(df.head())


#pd = pd.DataFrame({'Player Name Dict': temp_names, 'ID Number': temp_ids}).set_index('Player Name Dict')
#pd.to_csv(fr"---ENTER FILE PATH TO SAVE PLAYER DICTIONARY CSV--------\PGA Player Dictionary.csv")


#Pull All the Headshots
for index, row in df.iterrows():
    fname = row['Player Name']
    link = row['Headshot Link']
    with open(fname + '.png','wb') as f:
        im = requests.get(link)
        f.write(im.content)
