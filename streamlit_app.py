import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")


#create dropdown list
my_fruit_list = my_fruit_list.set_index('Fruit')
fruitsSelected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruitsToShow = my_fruit_list.loc[fruitsSelected]

#display table
streamlit.dataframe(fruitsToShow)

streamlit.header('Fruityvice Fruit Advise')

try:

  fruitChoice = streamlit.text_input('What fruit would you like info about?')
  if not fruitChoice:
    streamlit.error('Please select a fruit')
  else:
    streamlit.write('The user entered',fruitChoice)
    #streamlit.text(fruitJuiceResponse.json()) #writes to the screen
    fruitJuiceResponse = requests.get("https://fruityvice.com/api/fruit/"+fruitChoice)

    #normalize - make table 
    fruityviceNormalized = pandas.json_normalize(fruitJuiceResponse.json())
    #output to screen
    streamlit.dataframe(fruityviceNormalized)
    
except URLError as e:
  streamlit.error()
  
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_row)

addFruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding',addFruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
