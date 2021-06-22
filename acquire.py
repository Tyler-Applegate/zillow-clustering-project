# This is where my Zillow Clustering Project Acquire functions will go

########################### General Imports ####################################
import pandas as pd
import numpy as np
import os

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
    This function reads data from the Codeup db into a pandas DataFrame.
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
    a breakdown of the statistics on all numerica columns.
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
