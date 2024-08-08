# Libraries
import streamlit as st
import asyncio

# Local Modules
from data import load_history, remove_old_games_from_history
from utils import filter_first_half_games,filter_second_half_games
from api import get_live_games
from views import display_game


async def main():
    st.set_page_config(layout='wide')
    st.sidebar.title("Jogos ao Vivo")

    live_games = get_live_games()


    second_half_games = filter_second_half_games(live_games)

    if second_half_games:
        selected_second_half_game = None
        # Display Second Half Games
        st.sidebar.subheader("Segundo Tempo")
        for game in second_half_games:
            game_label = f"{game['teams']['home']['name']} x {game['teams']['away']['name']}"
            if st.sidebar.button(game_label, key=f"2nd_{game['fixture']['id']}"):
                selected_second_half_game = game
        if selected_second_half_game:
            await display_game(selected_second_half_game)


    first_half_games = await filter_first_half_games(live_games)
    if first_half_games:
        selected_first_half_game = None
        st.sidebar.subheader("Primeiro Tempo")
        for game in first_half_games:
            game_label = f"{game['teams']['home']['name']} x {game['teams']['away']['name']}"
            if st.sidebar.button(game_label, key=f"1st_{game['fixture']['id']}"):
                selected_first_half_game = game
        if selected_first_half_game:
            await display_game(selected_first_half_game)

    else:
        st.sidebar.write("Nenhum jogo ao vivo no momento")


if __name__ == "__main__":
    asyncio.run(main())