import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
leagueurl = str(input("Insira o URL da liga correspondente:"))
path = str(input("Insira o nome e o caminho para o arquivo .xlsx:"))

pageT = leagueurl
pageTreeT = requests.get(pageT, headers=headers)
pageSoupT = BeautifulSoup(pageTreeT.content, "html.parser")
clubs = pageSoupT.find_all("td", {"class": "hauptlink no-border-links"})
ClubsList = []
for club in clubs:
    club_name = club.text.strip()
    ClubsList.append(club_name)
websites = []
for club in clubs:
    link = club.find("a")["href"]
    #link = link.replace("startseite","kadernaechstesaison")
    website = "https://www.transfermarkt.co.uk" + link
    websites.append(website)

PlayersList = []
AgeList = []
PositionsList = []
NationList = []
ValuesList = []
ClubList = []
#PlinksList = []
Playerlinks = []
#chegoulist = []
#atelist = []
#Playerlist = []
#chegou = []
#ate = []
for c in range(len(websites)):
    page = websites[c]
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, "html.parser")
    #cleaned_values = []
    club_name = ClubsList[c]

    #Plinks = pageSoup.find_all("span", {"class": "hide-for-small"})
    Players = pageSoup.find_all("img", {"class": "bilderrahmen-fixed"})
    Age = pageSoup.find_all("td", {"class": "zentriert"})
    Positions = pageSoup.find_all("td", {"class": ["zentriert rueckennummer bg_Torwart", "zentriert rueckennummer bg_Abwehr", "zentriert rueckennummer bg_Mittelfeld", "zentriert rueckennummer bg_Sturm"]})
    Nationality = pageSoup.find_all("td", {"class": "zentriert"})
    Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
    for i in range(0, len(Players)):
        PlayersList.append(str(Players[i]).split('" class', 1)[0].split('<img alt="', 1)[1])
        ClubList.append(club_name)

    for i in range(1, (len(Players) * 3), 3):
        AgeList.append((str(Age[i]).split("(", 1)[1].split(")", 1)[0]))

    for i in range(0, len(Positions)):
        PositionsList.append((str(Positions[i]).split('title="', 1)[1].split('"><')[0]).title())

    for i in range(2, (len(Players) * 3), 3):
        NationList.append(str(Nationality[i]).split('title="', 1)[1].split('"/', 1)[0])

    for i in range(0, len(Values)):
        ValuesList.append(Values[i].text)
    #for value in ValuesList:
        #if 'm' in value:
            #cleaned_values.append(float(value.split('m\xa0')[0].split('€')[1]) * 1000000)
        #elif 'k' in value:
            #cleaned_values.append(float(value.split('k\xa0')[0].split('€')[1]) * 1000)
        #else:
            #cleaned_values.append(0.0)
    
data = zip_longest(PlayersList, ClubList, AgeList, PositionsList, NationList, ValuesList)
df = pd.DataFrame(data, columns=['Jogador','Clube', 'Idade', 'Posição', 'Nacionalidade', "Valor"])
df.to_excel(path, index=False)
print(df)
