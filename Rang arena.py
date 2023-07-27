import requests
import PySimpleGUI as sg

# API 
API_KEY = 'RGAPI-5f158e5a-1f0d-4de0-91b5-2f06f89e9970'
SUMMONER_NAME = 'PX Frata'  # Nom invocateur
REGION = 'euw1'  # Region (e.g., 'na1', 'euw1', 'eun1', etc.)

# Fonction pour avoir le summoner_id
def get_summoner_id(summoner_name, region, api_key):
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['id']
    return None

# Fonction pour avoir le rang 
def get_summoner_rank(summoner_id, region, api_key):
    url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data)   imprime la reponse de l'api
        for entry in data:
            if entry['queueType'] == 'RANKED_SOLO_5x5': # queue type de l'arena pas dispo atm a changer des que dispo
                return f"{entry['tier']} {entry['rank']} ({entry['leaguePoints']} LP)"
    return 'Astro low pas de rang ICANT'

# Config_Interface
sg.theme('DarkBlue')
layout = [
    [sg.Text("Rang Arena:")],
    [sg.Text("", size=(25, 3), font=('Helvetica', 20), key='-RANK-')],
]
window = sg.Window("Rang Arena Live", layout, finalize=True)

# Boucle
while True:
    event, values = window.read(timeout=10000)  #Maj chaque 10s
    if event == sg.WIN_CLOSED:
        break

    summoner_id = get_summoner_id(SUMMONER_NAME, REGION, API_KEY)
    if summoner_id:
        rank = get_summoner_rank(summoner_id, REGION, API_KEY)
        window['-RANK-'].update(rank)
    else:
        window['-RANK-'].update('Invocateur Introuvable')

window.close()
