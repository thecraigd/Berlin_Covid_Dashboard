[![CraigDoesData][logo]][link]

[logo]: https://www.craigdoesdata.de/img/logo/logo.png
[link]: https://www.craigdoesdata.de/


# [Covid-19 Dashboard for Berlin](https://berlin-covid.herokuapp.com/)


![App Screenshot](https://www.craigdoesdata.de/img/berlindashboard.jpg)

#### Project status - Complete


## Introduction

As we approach autumn and winter of 2020, and the number of Covid-19 cases begin to rise again across Europe, I wanted to find a way to keep track of my local situation. This is for my own interest and because some of the companies I work with are restricting who can enter the office based on the incidence of Covid-19 cases in their respective districts.

I became frustrated trying to get to the up-to-date figures for my area, so I decided to build a dashboard (around 6 months after all the cool kids started doing it) using [Streamlit](https://www.streamlit.io). I extract the data directly from the official figures posted on [berlin.de](https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-bezirke-gesamtuebersicht/), and then manipulate the data with [pandas](https://pandas.pydata.org/) to make it show the information I want.

I have the default set to Lichtenberg (my home district) so that I just have to refresh the page to see the information I want, but I used Streamlit's [selectbox](https://docs.streamlit.io/en/stable/api.html#streamlit.selectbox) function to allow the user to choose their own district, or a calculated 'All Berlin' field. The period can be adjusted using a [slider](https://docs.streamlit.io/en/stable/api.html#streamlit.slider).

I deployed the application using [Heroku](https://www.heroku.com), the Procfile, setup.sh and requirements.txt are all included in this repository.


### Technologies used
* [Streamlit](https://www.streamlit.io)
* [pandas](https://pandas.pydata.org/)
* [Heroku](https://www.heroku.com)


## Contact
All feedback is warmly received. Craig Dickson can be contacted at [craigdoesdata.de](https://www.craigdoesdata.de/contact.html).
