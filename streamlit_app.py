# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothe will be:", name_on_order)

cnx = st.connectio("snowflake")
session =cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
indredients_list = st.multiselect(
    'Choose up 5 ingredeitns',
    my_dataframe,
    max_selections=5
    ) 
if indredients_list:

    ingredients_string = ''

    for fruit_chosen in indredients_list:
        ingredients_string +=fruit_chosen + ' '

    #st.write(indredients_list)

    my_insert_stmt = """ INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('""" + ingredients_string.replace("'", "''") + """', '""" + name_on_order.replace("'", "''") + """')"""
                            
    
    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


    
    
