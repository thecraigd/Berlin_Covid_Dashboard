import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title - The title and introductory text and images are all written in Markdown format here, using st.write()

st.write("""
[![craigdoesdata logo][logo]][link]
[logo]: https://www.craigdoesdata.de/img/logo/logo_w_sm.gif
[link]: https://www.craigdoesdata.de/

# Berlin Covid-19 Dashboard

------------

This dashboard provides daily updates of the number of new Covid-19 cases, as well as the rolling 7-day-average number of new cases, in the selected district of Berlin (or in the whole city).

The data are the latest official figures provided by the Berlin government, sourced from [berlin.de](https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-bezirke-gesamtuebersicht/).

If you are viewing this on a mobile device, tap **>** in the top left corner to select district and timescale.
""")
st.write("---")

def get_data():
    historic_district_cases_url = 'https://www.berlin.de/lageso/_assets/gesundheit/publikationen/corona/meldedatum_bezirk.csv'
    historic_district_cases = pd.read_csv(historic_district_cases_url, sep=';', encoding = 'unicode_escape')

    return historic_district_cases

historic_district_cases_df = get_data()

# Adding a Total column for all Berlin
historic_district_cases_df['All Berlin'] = historic_district_cases_df.sum(axis=1)

district = st.sidebar.selectbox(
    'Select District:',
    ('Lichtenberg', 'All Berlin', 'Mitte', 'Friedrichshain-Kreuzberg', 'Neukoelln', 'Tempelhof-Schoeneberg', 'Pankow', 'Reinickendorf', 'Charlottenburg-Wilmersdorf', 'Spandau', 'Steglitz-Zehlendorf', 'Treptow-Koepenick')
)

days_to_show = st.sidebar.slider(
    'Number of days to display:',
    0, 40, 14
)


# Creating a pandas Series object with the rolling 7-day average for the selected district
seven_day_average = historic_district_cases_df.rolling(window=7)[district].mean()

# This is the simple metric of new reported cases on each day
new_reported_cases = historic_district_cases_df[['Datum', district]]


# Adding the new 7-day-average column for the selected district to the existing dataframe
new_col_name = ('7 Day Average for %s' % district)
historic_cases = historic_district_cases_df
historic_cases[new_col_name] = seven_day_average

# Creating a new DataFrame with the date and the 7-day-average
data_to_plot = historic_cases[['Datum', new_col_name]]

###################################


# Creating a pandas DataFrame with the populations of the districts (populations are in units of 100,000 because that's the figure used for 7-day-incidence reporting)
pop_dict = {'Bezirk': ['Lichtenberg', 'Mitte', 'Neukölln', 'Friedrichshain-Kreuzberg', 'Charlottenburg-Wilmersdorf', 'Tempelhof-Schöneberg', 'Pankow', 'Reinickendorf', 'Steglitz-Zehlendorf', 'Spandau', 'Marzahn-Hellersdorf', 'Treptow-Köpenick', 'All Berlin'], 
            'Population': [2.91452, 3.84172, 3.29691, 2.89762, 3.42332, 3.51644, 4.07765, 2.65225, 3.08697, 2.43977, 2.68548, 2.71153, 37.54418]}
pop_df = pd.DataFrame(data=pop_dict)

# Creating a 7 day rolling sum of cases per district
new_reported_cases['Seven Day Sum'] = new_reported_cases.rolling(7).sum()

# Getting the population 
poppo = pop_df.loc[pop_df['Bezirk'] == district]
popn = float(poppo['Population'])

new_reported_cases['Seven Day Incidence'] = new_reported_cases['Seven Day Sum'] / popn

incidence = new_reported_cases[['Datum', 'Seven Day Incidence']]
####################################

# Selecting the style for the plots
plt.style.use('ggplot')

# Font Size Control
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

st.write('# %s' % district)

# Plotting the 7 day incidence

st.write('This chart shows the 7 day incidence (# of cases per 100,000 inhabitants) for %s.' % district)

incidence_data = incidence.iloc[-days_to_show:,:]

fig, ax = plt.subplots()
plt.plot(incidence_data['Datum'], incidence_data['Seven Day Incidence'])
plt.xticks(rotation=45, 
    horizontalalignment='right',
    fontweight='light',
    fontsize='small')
plt.title('Seven Day Incidence for ' + district + ' - Last ' + str(days_to_show) + ' Days', color = '0.5')
st.pyplot(fig)
st.table(incidence.iloc[-3:,:])


st.write('---')

# Plotting the 7 day average



st.write('This chart shows a rolling 7-day-average (e.g. the value shown for 16.9.20 will be the total of all new cases from 9.9.20 - 16.9.20, divided by 7).')
st.write('This smoothes out the spikes and makes it easier to identify the real trend in cases.')

data = data_to_plot.iloc[-days_to_show:,:]

fig, ax = plt.subplots()
plt.plot(data['Datum'], data[new_col_name])
plt.xticks(rotation=45, 
    horizontalalignment='right',
    fontweight='light',
    fontsize='small')
plt.title('Rolling ' + new_col_name + ' - Last ' + str(days_to_show) + ' Days', color = '0.5')
st.pyplot(fig)
st.table(data_to_plot.iloc[-3:,:])


st.write('---')


# Plotting the new cases

st.write('This chart shows the raw number of new reported cases in ' + district +'.')
st.write("This will show larger variance and generally be 'noisier' than the 7-day-average chart.")

new_cases = new_reported_cases.iloc[-days_to_show:,:]

fig, ax = plt.subplots()
plt.plot(new_cases['Datum'], new_cases[district])
plt.xticks(rotation=45, 
    horizontalalignment='right',
    fontweight='light',
    fontsize='small')
plt.title('New Cases in ' + district + ' - Last ' + str(days_to_show) + ' Days', color='0.5')
st.pyplot(fig)
st.table(new_reported_cases.iloc[-3:,:])

st.write('---')

st.write('''
    Dashboard created by [Craig Dickson](https://www.craigdoesdata.de), with [Streamlit](https://www.streamlit.io).
    See the code on [GitHub](https://github.com/thecraigd/Berlin_Covid_Dashboard).

    I have made every effort to ensure the accuracy and reliability of the information on this dashboard. However, the information is provided "as is" without warranty of any kind.
''')