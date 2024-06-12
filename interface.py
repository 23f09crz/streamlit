import streamlit as st
import requests
from datetime import datetime
import time
from functions import *

# API URLs and headers
live_games_api_url = st.secrets["api_football"]["live_games_api_url"]
team_history_api_url = st.secrets["api_football"]["team_history_api_url"]
headers = {
    "x-rapidapi-key": st.secrets["api_football"]["x_rapidapi_key"],
    "x-rapidapi-host": st.secrets["api_football"]["x_rapidapi_host"]
}

st.set_page_config(layout='wide')

# Inicializar o estado da sessão
if 'auto_refresh' not in st.session_state:
    st.session_state['auto_refresh'] = False

if 'selected_game' not in st.session_state:
    st.session_state['selected_game'] = None

# Botão para ligar/desligar atualizações automáticas
if st.sidebar.button('Ligar/Desligar atualizações de API'):
    st.session_state['auto_refresh'] = not st.session_state['auto_refresh']

# Texto indicando o estado das atualizações automáticas
if st.session_state['auto_refresh']:
    st.sidebar.write("Atualizações automáticas: **LIGADAS**")
else:
    st.sidebar.write("Atualizações automáticas: **DESLIGADAS**")

# Função para buscar jogos ao vivo
def get_live_games():
    response = requests.get(live_games_api_url, headers=headers)
    if response.status_code == 200:
        games = response.json().get('response', [])
        print('os Jogos Ao Vivo Foram coletados')
        return [game for game in games if game['fixture']['status']['elapsed'] is None or game['fixture']['status']['elapsed'] < 50]
    else:
        st.error("Erro ao buscar jogos ao vivo")
        return []

# Função para filtrar jogos com base nos critérios de tempo
def filter_games(games):
    filtered_games = []
    for game in games:
        status = game['fixture']['status']
        time_elapsed = status['elapsed']
        if status['short'] == "HT" or (status['short'] == '2H' and time_elapsed < 71):
            filtered_games.append(game)
    return filtered_games   

# Função para buscar histórico de times
def get_team_history(team_name, team_id, last_n=20):
    history_data = load_history()
    if str(team_id) in history_data:
        print(f'Consultando Localmente {team_name}')
        print(f"dados: {history_data[str(team_id)]['response']}")
        return history_data[str(team_id)]['response']
    else:
        params = {
            "team": team_id,
            "last": last_n
        }
        response = requests.get(team_history_api_url, headers=headers, params=params)
        if response.status_code == 200:
            print(f'Consultando na API {team_name}')
            history_data[str(team_id)] = response.json()
            save_history(history_data)
            return history_data[str(team_id)]['response']
        else:
            st.error(f"Erro ao buscar histórico para o time {team_id}")
            return []

# Função para exibir detalhes do jogo ao vivo
def display_game_details(game):
    fixture = game['fixture']
    teams = game['teams']
    goals = game['goals']
    status = fixture['status']

    home_team = teams['home']['name']
    away_team = teams['away']['name']
    home_score = goals['home']
    away_score = goals['away']
    time_elapsed = status['elapsed']
    status_description = status['short']

    if status_description == 'HT':
        status_text = "INTERVALO"
    elif status_description == '2H':
        status_text = f"{time_elapsed} mins"
    else:
        status_text = status_description

    st.header(f"{home_score} x {away_score}")

# Função para exibir histórico de times
def display_team_history(team_id, team_name, limit=10):
    team_history = get_team_history(team_name, team_id)
    valid_games = [game for game in team_history if game['goals']['home'] is not None and game['goals']['away'] is not None]
    st.write(f"Últimos {limit} jogos de {team_name}:")
    for game in valid_games[1:limit+1]:
        fixture = game['fixture']
        date = datetime.strptime(fixture['date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d/%m')
        home_team = game['teams']['home']['name']
        away_team = game['teams']['away']['name']
        home_score = game['goals']['home']
        away_score = game['goals']['away']
        
        if home_team == team_name:
            if home_score > 0:
                st.markdown(f"{date}: <span style='color:green'><b>{home_team} {home_score}</b></span> - {away_team} {away_score}", unsafe_allow_html=True)
            else:
                st.markdown(f"{date}: <span style='color:red'><b>{home_team} {home_score}</b></span> - {away_team} {away_score}", unsafe_allow_html=True)
        else:
            if away_score > 0:
                st.markdown(f"{date}: {home_team} {home_score} - <span style='color:green'><b>{away_team} {away_score}</b></span>", unsafe_allow_html=True)
            else:
                st.markdown(f"{date}: {home_team} {home_score} - <span style='color:red'><b>{away_team} {away_score}</b></span>", unsafe_allow_html=True)

# Função para calcular média de gols
def calculate_average_goals(team_history, team_name, limit=10):
    try:
        valid_games = [game for game in team_history if game['goals']['home'] is not None and game['goals']['away'] is not None]
        total_goals = sum(game['goals']['home'] if game['teams']['home']['name'] == team_name else game['goals']['away'] for game in valid_games[:limit])
        return total_goals / limit
    except Exception as e:
        st.error(f"Erro ao calcular média de gols: {e}")
        return "Não foi possível calcular a média"

# Interface do Streamlit
st.sidebar.title("Jogos ao Vivo")

# Carregar histórico de times do arquivo JSON
history_data = load_history()

# Buscar e filtrar jogos ao vivo
live_games = filter_games(get_live_games())

# Remover jogos antigos do histórico
remove_old_games_from_history(history_data)


# Exibir botões para selecionar jogos
if live_games:
    selected_game = None
    for game in live_games:
        game_label = f"{game['teams']['home']['name']} x {game['teams']['away']['name']}"
        if st.sidebar.button(game_label):
            selected_game = game_label

    # Exibir detalhes do jogo selecionado
    for game in live_games:
        if f"{game['teams']['home']['name']} x {game['teams']['away']['name']}" == selected_game:
            print(selected_game)
            fixture = game['fixture']
            home_team = game['teams']['home']
            away_team = game['teams']['away']

            home_team_id = home_team['id']
            away_team_id = away_team['id']
            home_team_name = home_team['name']
            away_team_name = away_team['name']

            status = game['fixture']['status']
            time_elapsed = status['elapsed']
            status_description = status['short']

            if status_description == 'HT':
                status_text = "INTERVALO"
            elif status_description == '2H':
                status_text = f"{time_elapsed} mins"
            else:
                status_text = status_description

            st.title(f"{home_team_name} x {away_team_name} - {status_text}")
            
            # Exibir detalhes do jogo ao vivo
            display_game_details(game)

            # Buscar e exibir histórico do time da siapl
            home_team_history = get_team_history(home_team_name,home_team_id)
            
            # Buscar e exibir histórico do time visitante
            away_team_history = get_team_history(away_team_name,away_team_id)
            
            # Calcular e exibir média de gols
            home_team_avg_goals = calculate_average_goals(home_team_history, home_team_name)
            away_team_avg_goals = calculate_average_goals(away_team_history, away_team_name)
            st.subheader(f"Soma Total das Médias: {round(home_team_avg_goals + away_team_avg_goals,1)}")
            st.write(f"Média de Gols {home_team_name}: {home_team_avg_goals}")
            st.write(f"Média de Gols {away_team_name}: {away_team_avg_goals}")

            # Criar duas colunas para os históricos
            col1, col2 = st.columns(2)
            
            # Exibir históricos nas colunas
            with col1:
                st.subheader(f"Histórico {home_team_name}:")
                display_team_history(home_team_id, home_team_name)
                
            with col2:
                st.subheader(f"Histórico {away_team_name}:")
                display_team_history(away_team_id,away_team_name)

    # Lógica de atualização automática
    if st.session_state['auto_refresh']:
        time.sleep(30)  # 30 min
        st.rerun()
else:
    st.sidebar.write("Nenhum jogo ao vivo no momento")
