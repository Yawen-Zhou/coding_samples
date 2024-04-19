import streamlit as st
import pydeck as pdk

longitude = st.number_input('Please enter the longitude:', format="%f")
latitude = st.number_input('Please enter the latitude:', format="%f")

# Button to create the map
if st.button('Create Map'):
        # Create a map with a marker at the given longitude and latitude
        map = pdk.Deck(
            map_style = 'mapbox://styles/mapbox/streets-v11',
            initial_view_state = pdk.ViewState(
                latitude = latitude,
                longitude = longitude,
                zoom = 5,
                pitch = 0,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=[{'position': [longitude, latitude], 'size': 30000}],
                    get_position='position',
                    get_color=[180, 0, 200, 140],
                    get_radius='size',
                    pickable=True
                ),
            ],
        )
        st.pydeck_chart(map)