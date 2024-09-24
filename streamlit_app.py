import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Set up the Streamlit title and description
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""
    Choose the fruits you want in your custom smoothie:
""")

import streamlit as st

title = st.text_input("Name of Smoothe")
st.write("The name of Your Smoothe will be", title)

# Get the active Snowflake session
cnx=st.connection("Snowflake")
session = cnx.session()

# Query the "fruit_options" table to get the fruit names
my_dataframe = session.table("smoothies.public.fruit_option").select(col('Fruit_name'))

# Display the available fruit options in Streamlit
#st.write("Available fruits for your smoothie:")
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',my_dataframe,
    max_selections=5
)

if ingredients_list:
   # st.write(ingredients_list)
   # st.write(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '

        st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+title+"""')"""

    st.write(my_insert_stmt)
    time_to_insert= st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('your smoothie is ordered', icon="✅")
