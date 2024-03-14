import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
import requests

st.title("Pokemon Explorer!")


def get_details(poke_number):
	url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
	response = requests.get(url)
	pokemon = response.json()
	details = {}
	details['name'] = pokemon['name'].title()
	details['height'] =  pokemon['height'] * 10
	details['weight'] = pokemon['weight']
	details['move_count'] = len(pokemon['moves'])
	details['cry'] = pokemon['cries']['latest']
	details['sprite'] = pokemon['sprites']['front_default']
	details['moves'] = [x['move']['name'] for x in pokemon['moves']]
	return details

	
pokemon_number = st.slider("Pick a pokemon",
						   min_value=1,
						   max_value=150
						   )

details = get_details(pokemon_number)
height_data = pd.DataFrame({'Pokemon': ['Weedle', details['name'], 'Victreebel'],
							'Heights': [30, details['height'], 170]})
weight_data = pd.DataFrame({'Pokemon': ['Weedle', details['name'], 'Victreebel'],
               'Weights': [32, details['weight'], 155]})
         
color_lookup = {'fire': '#FF6C4C'}

colors = ['grey', '#FF6C4C', 'grey']
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5)) 

h_graph = sns.barplot(data = height_data, 
                    x = 'Pokemon',
					  y = 'Heights',
					  palette = colors,
					  ax=ax1)

w_graph = sns.barplot(data = weight_data, 
					  x = 'Pokemon',
					  y = 'Weights',
					  palette = colors,
					  ax=ax2)

ax1.set_title('Height')
ax2.set_title('Weight')
h_graph.set_xlabel('')
w_graph.set_xlabel('')

cola, colb = st.columns(2)
with cola:
	st.title(f'{details["name"]}')
with colb:
	picture = st.empty()
	
col1, col2 = st.columns(2)

with col1:
	tile = col1.container(height=120)
	tile.subheader('Height 	:arrow_up:')
	tile.subheader(f'{details["height"]}cm')
	
with col2:
	tile = col2.container(height=120)
	tile.subheader("Weight 	:weight_lifter:")
	tile.subheader(f"{details['weight']}kg")

picture.image(details['sprite'])

st.audio(details['cry'], format="audio/wav", start_time=0, sample_rate=None)

moves_markdown = '\n'.join("* **{}**".format(move) for move in details['moves'])

st.write(f'Move Count: {details["move_count"]}')
with st.expander("View Moves"):
	st.write(moves_markdown)

st.pyplot(fig)
