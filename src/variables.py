import streamlit as st
#genuinely hate the existence of this file, but i need to interact with the streamlit secrets feature for deployment purposes
# live_games_api_url = st.secrets["api_football"]["live_games_api_url"]
# team_history_api_url = st.secrets["api_football"]["team_history_api_url"]
# fixture_statistics_api_url = st.secrets["api_football"]["fixture_statistics_api_url"]
# standings_api_url = st.secrets["api_football"]["standings_api_url"]
# headers = {
#      "x-rapidapi-key": st.secrets["api_football"]["x_rapidapi_key"],
#      "x-rapidapi-host": st.secrets["api_football"]["x_rapidapi_host"]
#     }
live_games_api_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
team_history_api_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
fixture_statistics_api_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"
standings_api_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
headers = {
    "x-rapidapi-key": "deff4e03e9mshf7d1508c40a9f06p15f09bjsn57dd631a6a28",
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}




