import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


import helper

import preprocessor
df = pd.read_csv('D:/athlete_events.csv')
df1 = pd.read_csv('D:/noc_regions.csv')
st.sidebar.title('Olympics')
st.sidebar.image('https://st2.depositphotos.com/2304119/9181/v/450/depositphotos_91818746-stock-illustration-vector-file-illustration-olympic-games.jpgher')
user_menu=st.sidebar.radio(
    'select an option',
    ('Medal tally','over all analysis','country wise analysis','Athlete wise analysis'))

df=preprocessor.preprocess(df,df1)

if user_menu == 'Medal tally':
    st.sidebar.header('Medal tally')
    year,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('select year',year)
    selected_country = st.sidebar.selectbox('selected country', country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'overall' and selected_country == 'overall':
        st.title('over all tally')
    if selected_year != 'overall' and selected_country == 'overall':
        st.title('medal tally in'+str(selected_year)+'olympics')
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country+'over all perfomance')
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + ' perfomance in ' +str(selected_year))

    st.table(medal_tally)

if user_menu == 'over all analysis':
    st.title('Top statistics')
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athelets = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]



    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('sports')
        st.title(sports)





    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('events')
        st.title(events)
    with col2:
        st.header('athelets')
        st.title(athelets)
    with col3:
        st.header('nations')
        st.title(nations)
    nation = helper.data_over_time(df,'region')
    st.title('participation over the years')
    fig = px.line(nation,x='Edition',y='region')
    st.plotly_chart(fig)

    events = helper.data_over_time(df, 'Event')
    st.title('Events over the years')
    fig = px.line(events, x='Edition', y='Event')
    st.plotly_chart(fig)
    athelets = helper.data_over_time(df, 'Name')
    st.title('Athelet over the years')
    fig = px.line(athelets, x='Edition', y='Name')
    st.plotly_chart(fig)
    st.title('no of events over time')
    fig,ax   = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Sport', 'Event', 'Year'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title('most successful athelete')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')
    selected_sport = st.selectbox('select a sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)
if user_menu == 'country wise analysis':
    st.sidebar.title('Country Wise Analysis')
    country_df = df['region'].dropna().unique().tolist()
    country_df.sort()
    selected_country = st.sidebar.selectbox('select country', country_df)
    country_df = helper.year_wise_medaltally(df,selected_country)
    sns.lineplot(x='year',y='no of medals',data=country_df)
    st.pyplot(plt.gcf())
    t = helper.country_wise_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(t,annot=True)
    st.pyplot(fig)
if user_menu == 'Athlete wise analysis':
    df9 = df.drop_duplicates(subset=['region', 'Name'])
    x1 = df9['Age'].dropna()
    x2 = df9[df9['Medal'] == 'Gold']['Age'].dropna()
    x3 = df9[df9['Medal'] == 'Silver']['Age'].dropna()
    x4 = df9[df9['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Age overall', 'Gold', 'Silver', 'Bronz'], show_hist=False, show_rug=False)
    st.plotly_chart(fig)
    x = []
    name = []

    df12 = df9['Sport'].value_counts().head(38).reset_index()
    df13 = df12['index'].tolist()
    for sport in df13:
        df11 = df9[df9['Sport'] == sport]
        x.append(df11[df11['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    sport_df = df['Sport'].dropna().unique().tolist()
    sport_df.sort()
    sport_df.insert(0,'overall')
    selected_sport = st.selectbox('select sport',sport_df)
    help_df = helper.weight_vs_height(df,selected_sport)
    fig ,ax = plt.subplots()
    ax = sns.scatterplot(x=help_df['Weight'],y=help_df['Height'],hue=help_df['Medal'],style=help_df['Sex'],s=100)
    st.pyplot(fig)
    st.title('mens vs women')
    df15 = helper.men_vs_women(df)
    fig = px.line(df15, x='Year', y=['Men', 'Women'])
    st.plotly_chart(fig)

























