import pandas as pd
#########
# Uuden kokouksen jälkeen aja CSV2XLSrunner + ExcelCombiner
#########


def preprocess():

    df = pd.read_csv('anonData.csv')
    #Oikeat typet kolumneille
    df['Join Time'] = pd.to_datetime((df['Join Time']), format='%d.%m.%Y klo %H.%M.%S')
    df['Leave Time'] = pd.to_datetime((df['Leave Time']), format='%d.%m.%Y klo %H.%M.%S')
    df['Duration'] = pd.to_numeric(df['Duration'], downcast='float')
    df.sort_values('Join Time', inplace=True,ascending=False)
    return df
def keskiarvo(df):

    df_mean = df.copy()
    df_mean['Join Time'] = pd.to_datetime(df_mean['Join Time']).dt.date
    df_mean = df_mean.groupby(['Full Name','Join Time'], as_index=False).agg({'Duration':'sum'})
    df_mean = df_mean.groupby('Full Name',as_index=False).agg({'Full Name': 'min', 'Duration': 'mean'})
    df_mean = df_mean.rename(columns={'Duration':'Duration(mean)'})
    return df_mean
def maksimi(df):

    df_max = df.copy()
    df_max = df_max.groupby('Full Name',as_index=False).agg({'Full Name': 'min', 'Duration': 'max'})
    df_max = df_max.rename(columns={'Duration':'Duration(max)'})
    return df_max
def osallistumiskerrat(df):

    #Uusi table missä osallistumiskerrat per henkilö (poistettu samaan kokoukseen useampaan kertaan liittymiset)
    df_occurances = df.copy()
    df_occurances['Join Time'] = pd.to_datetime(df['Join Time']).dt.date
    df_occurances['Leave Time'] = pd.to_datetime(df['Leave Time']).dt.date
    df_occurances = df_occurances.groupby(['Full Name', 'Join Time'], as_index=False).agg({'Join Time': 'min', 'Leave Time': 'max', 'Full Name': 'min'})
    
    occ = df_occurances['Join Time'].value_counts()
    #Tehdään taulu: converting to df and assigning new Names to the columns
    df_occ_laika = pd.DataFrame(occ).reset_index()
    df_occ_laika.columns = ['Kokouspäivä', 'count']
    
    #Kokouksissa istutut kerrat per henkilö
    cnimi = df_occurances['Full Name'].value_counts()
    #Tehdään taulu: converting to df and assigning new Names to the columns
    df_value_counts = pd.DataFrame(cnimi).reset_index()
    df_value_counts.columns = ['nimet', 'count']
    return df_value_counts,df_occ_laika

def totaali(df):

    #Uusi table, missä palsussa (yhteensä) istuttu aika per henkilö
    df_total = df.copy()
    df_total = df.groupby('Full Name',as_index=False).agg({'Full Name': 'min', 'Duration': 'sum'})
    df_total = df_total.rename(columns={'Duration':'Duration(total)'})
    df_total.sort_values('Duration(total)', inplace=True,ascending=False)
    return df_total
    
def DurationMerger(df_mean,df_max,df_total):

    #Yhdistetään Duration-taulut
    df_Duration = df_mean.merge(df_max)
    df_Duration = df_Duration.merge(df_total)
    df_Duration.sort_values('Duration(max)', inplace=True,ascending=False)
    return df_Duration

def runner():
    df = preprocess()
    df_mean = keskiarvo(df)
    df_max = maksimi(df)
    df_value_counts, df_occ_laika = osallistumiskerrat(df)
    df_total = totaali(df)
    df_Duration = DurationMerger(df_mean,df_max,df_total)
    return df_value_counts, df_occ_laika, df_total, df_Duration