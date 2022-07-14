import numpy as np
import pandas as pd
def fetch_medal_tally(df,year, country):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = medal_tally
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_tally[medal_tally['region'] == country]
    if year != 'overall' and country == 'overall':
        temp_df = medal_tally[medal_tally['Year'] == int(year)]
    if year != 'overall' and country != 'overall':
        temp_df = medal_tally[(medal_tally['Year'] == year) & (medal_tally['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year')['Gold', 'Bronze', 'Silver'].sum().sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region')['Gold', 'Bronze', 'Silver'].sum().sort_values('Gold',
                                                                                    ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Bronze'] + x['Silver']
    x['Gold'] = x['Gold'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    return x



def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport',
                                             'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region')['Gold', 'Bronze', 'Silver'].sum().sort_values('Gold',
    ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Bronze'] + medal_tally['Silver']
    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)

    return medal_tally

def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'overall')
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'overall')
    return year, country
def data_over_time(df,col ):

    nation_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
    nation_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nation_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset = ['Medal'])
    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'Name_x':'Medals','index':'Name'})
    return x
def year_wise_medaltally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    df5 = new_df['Year'].value_counts().reset_index()
    df5.rename(columns={'index': 'year', 'Year': 'no of medals'}, inplace=True)
    df5.sort_values('year', inplace=True)
    df6 = df5.reset_index(drop=True)
    df6
    return df6
def country_wise_heatmap(df,country):
    df7 = df.dropna(subset=['Medal'])
    df7.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    df8 = df7[df7['region'] == country]
    pt = df8.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt
def weight_vs_height(df,sport):
    df9 = df.drop_duplicates(subset=['region','Name'])
    df9['Medal'].fillna('no medal',inplace=True)
    if sport != 'overall':
        df14 = df9[df9['Sport'] == sport]
        return df14
    else:
        return df9
def men_vs_women(df):
    df9 = df.drop_duplicates(subset=['region', 'Name'])
    mens = df9[df9['Sex'] == "M"].groupby('Year')['Name'].count().reset_index()
    womens = df9[df9['Sex'] == "F"].groupby('Year')['Name'].count().reset_index()
    df15 = pd.merge(mens, womens, on='Year', how='left').fillna(0)
    df15.rename(columns={'Name_x': 'Men', 'Name_y': 'Women'}, inplace=True)
    return df15












