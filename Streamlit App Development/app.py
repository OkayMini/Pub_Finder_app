import streamlit as st
import pandas as pd
import folium
from matplotlib import image
from geopy.geocoders import Nominatim
from sklearn.neighbors import DistanceMetric
from streamlit_folium import folium_static
from PIL import Image


# Create a multiselect widget for the user to choose a page
page_options = ['Home Page', 'Pub Locations', 'Find the nearest Pub']
selected_page = st.sidebar.selectbox('Select a page', page_options)

pubs_df = pd.read_csv('pub_df.csv')

# Use if else statements to display the selected page

###################PAGE-1#####################

if selected_page == 'Home Page':
    st.title(':beers: :red[Welcome to the Pub Finder Web Application]:beers:')
    st.write('This application displays information and statistics about pubs in the UK.')
    # Add an image
    image = Image.open('pub2.jpg')
    st.image(image) 
    st.write(f'Total number of pubs: {len(pubs_df)}')
    st.write(f'Number of cities: {pubs_df["city"].nunique()}')
    st.write(f'Number of postal codes: {pubs_df["postcode"].nunique()}')
    city_count = pubs_df['city'].value_counts()
    highest_city = city_count.nlargest(1)
    st.write(f'City with highest number of pubs: {highest_city.index[0]} ({highest_city.values[0]} pubs)')

    st.subheader("About me :point_down:")
    st.write("Nandini Shukla :wave:")
    st.write("Data Science intern @Innomatics research lab :computer:")
    
    st.subheader("Contect me :coffee:")
    st.markdown("Gmail  - nandini0212shukla@gmail.com")
    st.markdown("Github  - https://github.com/OkayMini")
    st.markdown("Linkedin  - https://www.linkedin.com/in/nandinishuklads/")


###################PAGE-2#####################

elif selected_page == 'Pub Locations':
    # Set up the app layout
    st.title(":beer: :blue[Pub Locations] :beer:")


    # Get user inputs for postal code and local authority
    location_pc = st.text_input('Enter your Postal Code:', 'SW1A 2AA')
    location_la = st.text_input('Enter your Local Authority:', 'Westminster')

    # Geocode the user's location
    geolocator = Nominatim(user_agent='my_app')
    location_data = geolocator.geocode(f'{location_pc} {location_la}', exactly_one=False)[0]
    lat, lon = location_data.latitude, location_data.longitude

    # Create a folium map object centered on the user's location
    m = folium.Map(location=[lat, lon], zoom_start=13)

    # Filter the pubs based on the chosen area
    filtered_pubs = pubs_df[(pubs_df['postcode'] == location_data.raw.get('postcode', '')) |
                            (pubs_df['city'] == location_data.raw.get('city', '')) |
                            (pubs_df['local_authority'] == location_la)]

    # Add a marker for each pub in the filtered dataset
    for i, pub in filtered_pubs.iterrows():
        folium.Marker(location=[pub['latitude'], pub['longitude']], 
                    popup=pub['name']).add_to(m)

    # Display the map using Streamlit
    st.markdown('### Pub Locations')
    st.write(f'Number of pubs in {location_pc} {location_la}: {len(filtered_pubs)}')
    folium_static(m) 

    # Display the list of pubs in the filtered dataset
    st.markdown('### List of Pubs')
    for i, pub in filtered_pubs.iterrows():
        st.write(pub['name'])  


###################PAGE-3#####################

elif selected_page == 'Find the nearest Pub':
    # Ask the user to enter their latitude and longitude
    st.title('Find the Nearest Pubs')
    lat = st.number_input('Enter your latitude:')
    lon = st.number_input('Enter your longitude:')

    # Find the nearest 5 pubs using Haversine distance
    dist = DistanceMetric.get_metric('haversine')
    distances = dist.pairwise(pubs_df[['latitude', 'longitude']], [[lat, lon]])
    pubs_df['Distance'] = distances[:, 0]
    nearest_pubs = pubs_df.nsmallest(5, 'Distance')
    
        # Display a map with the nearest pubs
    st.title('Nearest Pubs')
    m = folium.Map(location=[lat, lon], zoom_start=13)
    for i, pub in nearest_pubs.iterrows():
        icon = folium.Icon(icon='beer', prefix='fa')
        folium.Marker(location=[pub['latitude'], pub['longitude']], 
                    popup=pub['name'], icon=icon).add_to(m)
    folium_static(m)

    
    # Display a table with the nearest pubs
    st.title('Nearest Pubs List')
    st.write(nearest_pubs[['name', 'address', 'Distance']])

