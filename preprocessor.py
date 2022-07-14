import pandas as pd


def preprocess(df,df1):
    df = df[df['Season'] == 'Summer']
    df = df.merge(df1, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

