#created the main python file

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#PANDAS

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#changing the index to the name of the fruit
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])


#selected fruits will be in a new variable called 'fruits selected'
#then, assign the data to the variable called fruits_to_show


streamlit.dataframe(fruits_to_show)

#--------
streamlit.header('Frutyvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
streamlit.write('The user entered', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

#normalizing the json data with Pandas
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#show it in streamlit
streamlit.dataframe(fruityvice_normalized)

#new section to show frutyvice API response

# to stop running anything that it is above
streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("insert into fruit_load_list values ('from streamlit)")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# to add a new fruit (this was a challenge)
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# this will not work correctly!
# my_cur.execute("insert into fruit_load_list values ('from streamlit)")
