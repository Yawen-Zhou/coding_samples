import streamlit as st
import pandas as pd
from datetime import datetime
import pydeck as pdk


# read in data
dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
datdeath = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
datreco = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
st.write("# Daily Cases, Deaths, and Recoveries")
# get daily cases for Italy
dat_ita = dat[dat['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
diff_dat_ita = dat_ita.diff(axis=1)
diff_dat_ita.iloc[:, 0] = diff_dat_ita.iloc[:, 0].fillna(0)
diff_dat_ita = diff_dat_ita.astype(int)

# get daily deaths for Italy
datdeath_ita = datdeath[datdeath['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
datdeath_ita.head()
diff_datdeath_ita = datdeath_ita.diff(axis=1)
diff_datdeath_ita.iloc[:, 0] = diff_datdeath_ita.iloc[:, 0].fillna(0)
diff_datdeath_ita = diff_datdeath_ita.astype(int)

# daily recoveries for Italy
datreco_ita = datreco[datreco['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)

# concatenate these three data frames
concatenated_dat = pd.concat([diff_dat_ita, diff_datdeath_ita, datreco_ita], axis=0)
labels = (['Daily Cases'] * len(diff_dat_ita)) + \
         (['Daily Deaths'] * len(diff_datdeath_ita)) + \
         (['Daily Recoveries'] * len(datreco_ita))
concatenated_dat.insert(0, 'Label', labels)

# Provide some space
st.markdown('---')

# Use columns to organize the selectors
col1, col2 = st.columns([1, 1])

with col1:
    # User input for date
    st.markdown("""
    <style>
    .big-font {
        font-size:25px;
        font-weight:bold;
        margin-bottom:0px;
        padding-bottom:0px;
    }
    </style>
    <div class="big-font">Select a date</div>
    """, unsafe_allow_html=True)
    user_input_date = st.date_input("", datetime.today())

with col2:
    # Options for user to select from
    options = ["Daily Cases", "Daily Deaths", "Daily Recoveries"]

# Format the date as a string to match the DataFrame's columns format
formatted_date = user_input_date.strftime('%-m/%-d/%y')
formatted_date_change = user_input_date.strftime('%B %-d, %Y')

if formatted_date:
    # Check if the user input date is in the DataFrame columns
    if formatted_date in concatenated_dat.columns[1:]:
        # User selects an option
        st.markdown("""
    <style>
    .big-font {
        font-size:25px;
        font-weight:bold;
        margin-bottom:0px;
        padding-bottom:0px;
    }
    </style>
    <div class="big-font">Choose an option</div>
    """, unsafe_allow_html=True)
        selected_option = st.selectbox('', options)
        # Find the value for the entered date and selected option
        value = concatenated_dat.loc[concatenated_dat['Label'] == selected_option, formatted_date].values[0]
        # show the value
        st.markdown(f'#### {selected_option} of Italy on {formatted_date_change}')
        st.markdown(f'### {value}')

        # Extract the data for the selected date
        cases = concatenated_dat.loc[concatenated_dat['Label'] == 'Daily Cases', formatted_date].values[0]
        deaths = concatenated_dat.loc[concatenated_dat['Label'] == 'Daily Deaths', formatted_date].values[0]
        recoveries = concatenated_dat.loc[concatenated_dat['Label'] == 'Daily Recoveries', formatted_date].values[0]

        # Create a DataFrame for mapping
        data_for_map = pd.DataFrame({
            'country': ['Italy'],
            'latitude': [40.8719],  # Latitude for Italy's centroid
            'longitude': [15.0674], # Longitude for Italy's centroid
            'Daily Cases': [cases],
            'Daily Deaths': [deaths],
            'Daily Recoveries': [recoveries]
        })
        # Set up the pydeck view state centered on Italy
        view_state = pdk.ViewState(
            latitude=41.8719,
            longitude=12.5674,
            zoom=4,
            pitch=0,
        )
        # Select which data to display on the map
        selected_data_type = st.selectbox("Select data to display on the map", ["Daily Cases", "Daily Deaths", "Daily Recoveries"])

        # Define tooltip text based on selected data type
        tooltip_text = f"<b>{selected_data_type.replace('_', ' ').title()}:</b> " + \
                        f"{data_for_map[selected_data_type].values[0]}"
        
        # Define color based on the selected data type
        if selected_data_type == "Daily Cases":
            color = [255, 255, 0, 130]  # Yellow with some transparency
        elif selected_data_type == "Daily Deaths":
            color = [255, 0, 0, 130]  # Red with some transparency
        else:  # Assuming the only other option is "Daily Recoveries"
            color = [0, 0, 255, 130]  # Blue with some transparency

        # Set up the pydeck layer
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=data_for_map,
            get_position='[longitude, latitude]',
            get_radius=250000, # Radius is in meters
            get_color=color,
            pickable=True
        )
        map_style = 'mapbox://styles/mapbox/streets-v11'
        # Set up the pydeck deck
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style=map_style,
            tooltip={
                "html": tooltip_text,
                "style": {
                    "color": "white"
                }
            }
        )

        # Display the map in the Streamlit app
        st.pydeck_chart(deck)
    else:
        st.error('The selected date is invalid or not in the dataset. Please select again.')
