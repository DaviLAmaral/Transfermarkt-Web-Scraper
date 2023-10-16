import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import filedialog
europa = "https://www.transfermarkt.co.uk/wettbewerbe/europa"
america = "https://www.transfermarkt.co.uk/wettbewerbe/amerika"
asia = "https://www.transfermarkt.co.uk/wettbewerbe/asien"
africa = "https://www.transfermarkt.co.uk/wettbewerbe/afrika"
Regionsl = []
Regionsl.append(europa) 
#for c in range(2,11):
#    Regionsl.append(europa + "?page={}".format(c))
Regionsl.append(america)
#for c in range(2,6):
#    Regionsl.append(america + "?page={}".format(c))
Regionsl.append(asia)
#for c in range(2,5):
#    Regionsl.append(asia + "?page={}".format(c))
Regionsl.append(africa)
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}
websitesL = []
imglinks = []
flaglinks = []
flagnames = []
leaguenames = []

for i in range(len(Regionsl)):
    pageL = Regionsl[i]
    pageTreeL = requests.get(pageL, headers=headers)
    pageSoupL = BeautifulSoup(pageTreeL.content, "html.parser")
    leagues = pageSoupL.find_all("td")
    
    for league in leagues:
        link = league.find("a")
        if link and "startseite" in str(link) and "+" not in str(link):
            websiteL = "https://www.transfermarkt.co.uk" + link["href"]
            if websiteL not in websitesL:
                websitesL.append(websiteL)
        img = league.find("img")
        if "png" in str(img) and "logo" not in str(img) and "discussion" not in str(img):
            flaglink = img["src"]            
            flaglinks.append(flaglink)
            flagname = img["title"]
            flagnames.append(flagname)
        if "png" in str(img) and "flagge" not in str(img) and "discussion" not in str(img):
            imglink = img["src"]
            leaguename = img["title"]
            if imglink not in imglinks:
                leaguenames.append(leaguename)
                imglinks.append(imglink)

class ImageApp:
    def __init__(self, root, imglinks, flaglinks, leaguenames, flagnames):
        self.root = root
        self.root.title("Transfermarkt Leagues")

        self.img_links = imglinks
        self.flag_links = flaglinks
        self.league_names = leaguenames
        self.flag_names = flagnames
        self.league_links = websitesL

        self.current_img_index = 0
        self.current_flag_index = 0
        self.current_league_index = 0

        self.image_label_flag = tk.Label(root)
        self.image_label_flag.pack(side=tk.RIGHT)

        self.image_label_img = tk.Label(root)
        self.image_label_img.pack(side=tk.RIGHT)

        self.league_name_label = tk.Label(root, text="")
        self.league_name_label.pack(side=tk.RIGHT)

        self.flag_name_label = tk.Label(root, text="")
        self.flag_name_label.pack(side=tk.RIGHT)

        self.prev_button = tk.Button(root, text="Previous", command=self.show_prev_image)
        self.prev_button.pack()

        self.next_button = tk.Button(root, text="Next", command=self.show_next_image)
        self.next_button.pack()

        botao_salvar = tk.Button(root, text="Save Excel File To...", command=self.salvar_arquivo)
        botao_salvar.pack()
        
        #botao_ano = tk.Button(root, text="Selecionar Ano", command=self.select_year)
        #botao_ano.pack()

        self.show_images()

    def salvar_arquivo(self):
        self.caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel","*.xlsx"), ("Todos os Arquivos", "*.*")])

    def select_year(self):
        year = tk.simpledialog.askinteger("Selecionar Temporada", "Digite o ano:")
        if year is not None:
            print(f"Ano selecionado: {year}")
        self.temporada = "/plus/?saison_id=" + str(year)

    def show_images(self):
        image_url = self.img_links[self.current_img_index]
        flag_url = self.flag_links[self.current_flag_index]
        league_name = self.league_names[self.current_img_index]
        flag_name = self.flag_names[self.current_flag_index]
        league_url = self.league_links[self.current_league_index]

        self.league_button = tk.Button(root,text="Generate " + league_name, command=self.open_link)
        self.league_button.pack()

        self.big5_button = tk.Button(root,text="Generate 'Big Five' Leagues", command=self.big5)
        self.big5_button.pack()

        response_img = requests.get(image_url)
        image_data = BytesIO(response_img.content)
        image = Image.open(image_data)
        photo_img = ImageTk.PhotoImage(image)
        self.image_label_img.config(image=photo_img)
        self.image_label_img.image = photo_img

        response_flag = requests.get(flag_url)
        flag_data = BytesIO(response_flag.content)
        flag = Image.open(flag_data)
        photo_flag = ImageTk.PhotoImage(flag)
        self.image_label_flag.config(image=photo_flag)
        self.image_label_flag.image = photo_flag

        self.league_name_label.config(text=league_name)
        self.flag_name_label.config(text=flag_name)

    def show_prev_image(self):
        self.current_img_index = (self.current_img_index - 1) % len(self.img_links)
        self.current_flag_index = (self.current_flag_index - 1) % len(self.flag_links)
        self.current_league_index = (self.current_league_index - 1) % len(self.league_links)
        self.destroy_league_button()  # Destruir o botão atual
        self.show_images()

    def show_next_image(self):
        self.current_img_index = (self.current_img_index + 1) % len(self.img_links)
        self.current_flag_index = (self.current_flag_index + 1) % len(self.flag_links)
        self.current_league_index = (self.current_league_index + 1) % len(self.league_links)
        self.destroy_league_button()  # Destruir o botão atual
        self.show_images()

    def destroy_league_button(self):
        if hasattr(self, 'league_button'):
            self.league_button.destroy()
            self.big5_button.destroy()
    def big5(self):
        data = []
        big5l = ["https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1","https://www.transfermarkt.co.uk/laliga/startseite/wettbewerb/ES1","https://www.transfermarkt.co.uk/bundesliga/startseite/wettbewerb/L1","https://www.transfermarkt.co.uk/ligue-1/startseite/wettbewerb/FR1","https://www.transfermarkt.co.uk/serie-a/startseite/wettbewerb/IT1"]
        for c in range(len(big5l)):
            pageT = str(big5l[c]) #+ self.temporada)
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
                website = "https://www.transfermarkt.co.uk" + link
                websites.append(website)

            PlayersList = []
            AgeList = []
            PositionsList = []
            NationList = []
            ValuesList = []
            ClubList = []
            cleaned_values = []
            for c in range(len(websites)):
                page = websites[c]
                pageTree = requests.get(page, headers=headers)
                pageSoup = BeautifulSoup(pageTree.content, "html.parser")
                club_name = ClubsList[c]

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
            data += zip_longest(PlayersList, ClubList, AgeList, PositionsList, NationList, ValuesList)
        df = pd.DataFrame(data, columns=['Jogador','Clube', 'Idade', 'Posição', 'Nacionalidade', "Valor"])
        df.to_excel(self.caminho_arquivo, index=False)      

    def open_link(self):
        pageT = str(self.league_links[self.current_league_index]) #+ self.temporada)
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
            website = "https://www.transfermarkt.co.uk" + link
            websites.append(website)

        PlayersList = []
        AgeList = []
        PositionsList = []
        NationList = []
        ValuesList = []
        ClubList = []
        cleaned_values = []
        for c in range(len(websites)):
            page = websites[c]
            pageTree = requests.get(page, headers=headers)
            pageSoup = BeautifulSoup(pageTree.content, "html.parser")
            club_name = ClubsList[c]

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
        df = pd.DataFrame(data, columns=['Player','Club', 'Age', 'Position', 'Nationality', "Value"])
        df.to_excel(self.caminho_arquivo, index=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root, imglinks, flaglinks, leaguenames, flagnames)
    root.mainloop()
