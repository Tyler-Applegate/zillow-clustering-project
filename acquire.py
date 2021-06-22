# This is where my Zillow Clustering Project Acquire functions will go

########################### General Imports ####################################
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

############### Connection #####################################################

# Enables access to my env.py file in order to use sensitive info to access Codeup DB
from env import host, user, password

# sets up a secure connection to the Codeup db using my login infor
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my env file to create a connection url to access
    the Codeup database.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
################### Data Acquisition ##########################################

def new_zillow_cluster():
    '''
    This function uses my credentials to connect to the zillow dataset in the Codeup database,
    performs a SQL query and returns a pandas DataFrame.
    '''
    sql_query = '''
                SELECT *
                FROM properties_2017 AS prop
                LEFT JOIN (SELECT DISTINCT parcelid, logerror, max(transactiondate) AS transactiondate
                FROM predictions_2017 
                        GROUP BY parcelid, logerror) AS pred
                        USING (parcelid)
                LEFT JOIN propertylandusetype AS land USING (propertylandusetypeid)
                LEFT JOIN storytype AS story USING (storytypeid)
                LEFT JOIN typeconstructiontype AS construct USING (typeconstructiontypeid)
                LEFT JOIN unique_properties AS special USING (parcelid)
                LEFT JOIN airconditioningtype AS air USING (airconditioningtypeid)
                LEFT JOIN architecturalstyletype AS architect USING (architecturalstyletypeid)
                LEFT JOIN buildingclasstype  AS class USING (buildingclasstypeid)
                LEFT JOIN heatingorsystemtype AS heat USING (heatingorsystemtypeid)
                WHERE transactiondate LIKE '2017%'
                AND latitude IS NOT null
                AND longitude IS NOT null
                '''
    return pd.read_sql(sql_query, get_connection('zillow'))

def get_zillow_cluster():
    '''
    This function reads in zillow data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('zillow_cluster.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('zillow_cluster.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_zillow_cluster()
        
        # Cache data
        df.to_csv('zillow_cluster.csv')

    return df

def overview(df):
    '''
    This function returns the shape and info of the df. It also includes a breakdown of the number of unique values
    in each column to determine which are categorical/discrete, and which are numerical/continuous. Finally, it returns
    a breakdown of the statistics on all numeric columns.
    '''
    print(f'This dataframe has {df.shape[0]} rows and {df.shape[1]} columns.')
    print('----------------------------------')
    print('')
    print(df.info())
    print('----------------------------------')
    print('')
    print('Unique value counts of each column')
    print('')
    print(df.nunique())
    print('----------------------------------')
    print('')
    print('Stats on Numeric Columns')
    print('')
    print(df.describe())
    
def nulls_by_col(df):
    '''
    This function determines how many null values there are in each column, and returns a pandas DataFrame
    with 3 columns, index=column name, 
    num_missing=number of missing values per columnm, 
    prcnt_miss=what percent of each column is null.
    '''
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    prcnt_miss = num_missing / rows * 100
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'percent_rows_missing': prcnt_miss})
    return cols_missing

def nulls_by_row(df):
    '''
    This function determines how many null values there are in each row, and returns a pandas DataFrame
    with 4 columns, index=index, 
    num_missing=number of missing values per row, 
    prcnt_miss=what percent of each row is null,
    num_rows=how many rows are missing this many values.
    '''
    num_missing = df.isnull().sum(axis=1)
    prcnt_miss = num_missing / df.shape[1] * 100
    rows_missing = pd.DataFrame({'num_cols_missing': num_missing, 'percent_cols_missing': prcnt_miss})\
    .reset_index()\
    .groupby(['num_cols_missing', 'percent_cols_missing']).count()\
    .rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing
    
    
def summarize(df):
    '''
    This function will take in a single argument (pandas DF)
    and output to console various statistics on said DF, including:
    # .head()
    # .info()
    # .describe()
    # value_counts()
    # observe null values
    '''
    print('----------------------------------------------------')
    print('DataFrame Head')
    print(df.head(3))
    print('----------------------------------------------------')
    print('DataFrame Info')
    print(df.info())
    print('----------------------------------------------------')
    print('DataFrame Description')
    print(df.describe())
    num_cols = [col for col in df.columns if df[col].dtype != 'O']
    cat_cols = [col for col in df.columns if col not in num_cols]
    print('----------------------------------------------------')
    print('DataFrame Value Counts: ')
    for col in df.columns:
        if col in cat_cols:
            print(df[col].value_counts())
            print('--------------------------------------------')
            print('')
        else:
            print(df[col].value_counts(bins=10, sort=False))
            print('--------------------------------------------')
            print('')
    print('----------------------------------------------------')
    print('Nulls in DataFrame by Column: ')
    print(nulls_by_col(df))
    print('----------------------------------------------------')
    print('Nulls in DataFrame by Rows: ')
    print(nulls_by_row(df))
    print('----------------------------------------------------')
    
