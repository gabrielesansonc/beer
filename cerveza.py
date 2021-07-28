#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 16:54:43 2021

@author: gabriel
"""

import pandas as pd #data manipulation
import streamlit as st #user interface
from PIL import Image #open the images
import statsmodels.api as sm # for the regression and prediction
import altair as alt #for the plots and charts
import plotly.express as px #for the map
import pycountry #for the 3 letter country code needed in the map
import base64

#Upload the title image
image = Image.open ('Screen Shot 2021-07-15 at 8.05.55 PM.png')
st.image (image, use_column_width=True)
st.subheader('This app will predict how much you will like a new beer!')

st.write("#")
st.write("#")


st.image ('beerinstruction.png', use_column_width=True)
st.image ('beerdatahead.png', use_column_width=True)

sample = pd.read_excel('Cervezas.xlsx')
samplecsv = sample.to_csv(index=False)


b64 = base64.b64encode(samplecsv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="samplefile.csv">Download Sample File </a>'

st.write(href, unsafe_allow_html=True)  

st.write("#")
st.write("#")

st.header('Upload the file containing the data of your beers:')

try:
    yourFile = st.file_uploader('Upload excel or csv file here')
    
    yourData=0
    
    if yourFile.name.endswith('.csv'):
        yourData = pd.read_csv(yourFile)
    else:
        yourData = pd.read_excel(yourFile)

    #Ask user for the file of beers
    st.write("#")
    
    #Ask user for variables of new beer
    st.header('Fill in the following variables of your prospective beer')
    PublicRating = st.slider ('Public rating (use untapped)',0.0,5.0,float(yourData['PublicRating'].mean()),0.1) 
    IBU = st.slider ('IBU (may use untapped)',0.0,100.0,float(yourData['IBU'].mean()),1.0)
    ABV = st.slider ('ABV',0.0,50.0,float(yourData['ABV'].mean()),0.1)
    #Ask user for country
    dat = pd.read_excel('countries.xlsx')
    COUNTRIES = dat['Countries'].unique()
    Country = st.selectbox(
         'Choose the country of your beer',
         (COUNTRIES))
    #Ask user for beer type
    beertype = ["Golden Ale","Wheat Beer", "Other"]
    Type = st.radio('Choose the beer type:',beertype) 
    
    
    #Assign regression variables
    independentvar = yourData[['GoldenAle', 'Wheat', 'PublicRating']]
    explanatoryvar = yourData['MyRating']
             
    
    
    # Assign appropiate binary value to the user input of type
    GoldenAle = 0
    Wheat= 0
    if Type == "Golden Ale":
        GoldenAle = 1
    if Type == "Wheat Beer":
        Wheat = 1
            
    
    
    
    # Creates Multiple linear regression
    model = sm.OLS(explanatoryvar, independentvar).fit()
    
    # Stores independent variables in array to add to plots and charts data
    prospectVar = [GoldenAle, Wheat, PublicRating]
    
    st.write("""
             ***
             """)       
    st.write("#")
    
    #Predict the rating of the beer
    st.header('Your personal rating for this beer is:')
    predictions = float(model.predict(prospectVar)) # make the predictions by the model
    st.header (round(predictions,1))
    st.write("#")
    st.write("""
             ***
             """)
    
    #create beer variable arrays and covert them to list in order to anex new candidate
    colu1 = list(yourData['Beer'])
    colu1.append ('Prospective Candidate')
    
    colu16 = list(yourData['PublicRating'])
    colu16.append(PublicRating)
    
    colu17 = list(yourData['ABV'])
    colu17.append(ABV)
    
    colu19 = list(yourData['IBU'])
    colu19.append(IBU)
    
    colu20 = list(yourData['Country'])
    colu20.append(Country)
    
    colu21 = list(yourData['Type'])
    colu21.append(Type)
    
    colu22 = list(explanatoryvar)
    colu22.append (round(predictions,1))
    
    
    #Create colums with anexed beer into a dataframe
    dataForCharts = pd.DataFrame({'Beer' : colu1, 'My Rating' : colu22, 'Public Rating': colu16, 'Alcohol' : colu17, 'IBU' : colu19, 'Country': colu20, 'Type': colu21}) 
    print(dataForCharts)
    
    
    
    
    #Create bar chart
    st.subheader("This is how it compares to your other ratings:")
    st.write("#")
    
    ChartRanking = alt.Chart(dataForCharts).mark_bar().encode(
        x=alt.X('Beer', sort='-y'),
        y=alt.Y('My Rating',scale=alt.Scale(domain=(min(colu22)-0.1, max(colu22)+0.1))),
         # The highlight will be set on the result of a conditional statement
        color=alt.condition(
            alt.datum.Beer == 'Prospective Candidate',  # If the year is 1810 this test returns True,
            alt.value('red'),     # which sets the bar orange.
            alt.value('rebeccapurple')   # And if it's not true it sets the bar steelblue.
            ),
            tooltip=['Beer', 'My Rating', 'Type', 'Country']
        ).interactive()
    
    st.write(ChartRanking)
    
    st.write("""
             ***
             """)
             
             
    #Create scattered plots         
    st.subheader('This is how it compares in the other variables:')
    st.write("#")
    st.write("Public Rating vs My Ratings")
    
    ChartRating= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Public Rating',
        y='My Rating',
        color=alt.condition(
        alt.datum.Beer == 'Prospective Candidate', 
        alt.value('black'),     
        'Type'
            ),
        tooltip=['Beer', 'My Rating', 'Type', 'Country']
    ).interactive()
    
    st.write(ChartRating)
    
    st.write("ABV vs My Ratings")
    
    ChartABV= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='Alcohol',
        y='My Rating',
        color=alt.condition(
        alt.datum.Beer == 'Prospective Candidate', 
        alt.value('black'),     
        'Type'
            ),
        tooltip=['Beer', 'My Rating', 'Type', 'Country']
    ).interactive()
    
    st.write(ChartABV)
    
    
    st.write("IBU vs My Ratings")
    
    ChartIBU= alt.Chart(dataForCharts).mark_circle(size=100).encode(
        x='IBU',
        y='My Rating',
        color=alt.condition(
        alt.datum.Beer== 'Prospective Candidate', 
        alt.value('black'),     
        'Type'
            ),
        tooltip=['Beer', 'My Rating', 'Type', 'Country']
    ).interactive()
    
    st.write(ChartIBU)
    
    #Create map
    
    #Creates an array of the countries and average rating
    AveRat= yourData.groupby('Country')['MyRating'].mean().reset_index()
    
    #Creates array of three letter codes for countries in data
    input_countries = AveRat['Country']
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3
    codes = [countries.get(country, 'Unknown code') for country in input_countries]
    
    #Adds code column to the average rating per country array
    AveRat['codes']=codes
    
    #Shows the map
    st.subheader('Here is a map of your average ratings per countries:')
    fig = px.choropleth(AveRat, locations="codes",
                        color="MyRating", # lifeExp is a column of gapminder
                        hover_name='Country', # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Greens)
    st.write(fig)
    
    
    
    st.subheader('Summary of the multiple linear regression:')
    
    st.write("#")
             
    st.write(model.summary())
    
    st.write("#")
    st.write("#")
    st.write("#")
    st.write("#")
    
    
    st.image ('Screen Shot 2021-07-21 at 10.28.01 AM.png', use_column_width=True)
except:
    st.write('No Excel or CSV file uploaded yet')
