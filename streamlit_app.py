import streamlit

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")


#create dropdown list
my_fruit_list = my_fruit_list.set_index('Fruit')
fruitsSelected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruitsToShow = my_fruit_list.loc[fruitsSelected]

#display table
streamlit.dataframe(fruitsToShow)

streamlit.header('Fruityvice Fruit Advise')

fruitChoice = streamlit.text_input('What fruit would you like info about?','Kiwi')
streamlit.write('The user entered',fruitChoice)

import requests
fruitJuiceResponse = requests.get("https://fruityvice.com/api/fruit/"+fruitChoice)
#streamlit.text(fruitJuiceResponse.json()) #writes to the screen

#normalize - make table 
fruityviceNormalized = pandas.json_normalize(fruitJuiceResponse.json())
#output to screen
streamlit.dataframe(fruityviceNormalized)

import snowflake.connector
import snowflake.connector

myCnx = snowflake.connector(**streamlit.secrets["Snowflake"])

myCur = myCnx.cursor()

myCur.execute("SELECT CURRENT_USER(), current_account(), current_region()")

myDataRow = myCur.fetchone()

streamlit.text("Hi from Snowflake")
streamlit.text(myDataRow)
