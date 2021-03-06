# This is where my Zillow Clustering Project Prepare functions will go

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import os
from env import host, user, password
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer

################# Starting to prepare #######################

def new_index(df):
    '''
    This function takes in the newly acquired zillow dataframe,
    renames the parcelid column as parcel_id,
    and sets this variable as the index.
    '''
    
    df = df.rename(columns={'parcelid': 'parcel_id'})
    df = df.set_index('parcel_id')
    
    return df

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

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    ''' 
        take in a dataframe and a proportion for columns and rows
        return dataframe with columns and rows not meeting proportions dropped
    '''
    col_thresh = int(round(prop_required_column*df.shape[0],0)) # calc column threshold
    
    df.dropna(axis=1, thresh=col_thresh, inplace=True) # drop columns with non-nulls less than threshold
    
    row_thresh = int(round(prop_required_row*df.shape[1],0))  # calc row threshhold
    
    df.dropna(axis=0, thresh=row_thresh, inplace=True) # drop columns with non-nulls less than threshold
    
    return df

def get_counties(df):
    '''
    This function will create dummy variables out of the original fips column. 
    And return a dataframe with all of the original columns except regionidcounty.
    We will keep fips column for data validation after making changes. 
    New columns added will be 'LA', 'Orange', and 'Ventura' which are boolean 
    The fips ids are renamed to be the name of the county each represents. 
    '''
    # create dummy vars of fips id
    county_df = pd.get_dummies(df.fips)
    # rename columns by actual county name
    county_df.columns = ['LA', 'Orange', 'Ventura']
    # concatenate the dataframe with the 3 county columns to the original dataframe
    df = pd.concat([df, county_df], axis = 1)
    # drop regionidcounty and fips columns
    df = df.drop(columns = ['regionidcounty'])
    return df

def create_features(df):
    '''
    This function is specific to my zillow clustering project. 
    It creates new feature columns to use in clustering exploration
    and modeling.
    '''
    # create age column that uses yearbuilt to show how old the property is
    df['age'] = 2017 - df.yearbuilt
    # create taxrate variable
    df['taxrate'] = df.taxamount/df.taxvaluedollarcnt*100
    # create acres variable
    df['acres'] = df.lotsizesquarefeet/43560
    
    return df

def create_bins(df):
    '''
    This function takes in specific variables in the zillow dataframe and bins them so they will be more useful in exploration, statistical testing, and modeling.
    '''
    
    df['bath_bins'] = pd.cut(df['bathroomcnt'], [0, 1, 1.5, 2, 3, 4, 5, 13])
    df['bed_bins'] = pd.cut(df['bedroomcnt'], [0,1,2,3,4,6,8,10])
    df['bb_bins'] = pd.cut(df['calculatedbathnbr'], [0,1,2,3,4,6,10,13])
    df['fb_bins'] = pd.cut(df['fullbathcnt'], [0,1,2,3,4, 13])
    df['room_bins'] = pd.cut(df['roomcnt'], [0,1,3,5,7,9,15])
    
    return df

def discrete_vars(df):
    # get value counts for discrete variables

    disc_cols = [col for col in df.columns if (df[col].dtype == "object")]

    for col in disc_cols:
    
        print(col)
        print(df[col].value_counts())
        print()

def plot_univariate(df):
    # distribution of the data
    con_cols = [col for col in df.columns if (df[col].dtype == 'int64') | (df[col].dtype == 'float64')]

    for col in con_cols:
        plt.hist(df[col])
        plt.title(f"{col} distribution")
        plt.show()

def drop_outliers(df, col_list, k=1.5):
    '''
    This function takes in a dataframe and removes outliers that are k * the IQR
    '''
#     col_list = ['bathroomcnt', 'bedroomcnt', 'calculatedbathnbr',
#        'calculatedfinishedsquarefeet', 'fips', 'fullbathcnt', 'latitude',
#        'longitude', 'lotsizesquarefeet', 'roomcnt', 'taxamount', 'logerror',
#        'LA', 'Orange', 'Ventura', 'age', 'taxrate', 'acres', 'bath_bed_ratio',
#        'abs_logerror']
    for col in col_list:

        q_25, q_75 = df[col].quantile([0.25, 0.75])
        q_iqr = q_75 - q_25
        q_upper = q_75 + (k * q_iqr)
        q_lower = q_25 - (k * q_iqr)
        df = df[df[col] > q_lower]
        df = df[df[col] < q_upper]
        
    return df 

def drop_columns(df):
    '''
    This function takes in a pandas DataFrame, and a list of columns to drop,
    and returns a DataFrame after dropping the columns
    '''
    # This list needs to be updated for each DataFrame
    col_list = ['propertylandusetypeid', 'id', 'finishedsquarefeet12', 'propertycountylandusecode', 'propertyzoningdesc', 'transactiondate', 'heatingorsystemdesc', 'propertylandusedesc', 'heatingorsystemtypeid', 'buildingqualitytypeid', 'unitcnt', 'censustractandblock', 'regionidcity', 'regionidzip', 'yearbuilt', 'structuretaxvaluedollarcnt', 'taxvaluedollarcnt', 'assessmentyear',
 'landtaxvaluedollarcnt', 'rawcensustractandblock']
    
    df = df.drop(columns=col_list)
    
    return df


def zillow_prep(df):
    '''
    This functions combines multiple functions to prepare my zillow data to be split.
    '''

    # Runs my new index functions to rest the index to parcel_id
    df = new_index(df)
    
    # This functions drops columns and rows that exceed a specified limit of null values
    df = handle_missing_values(df)
    
    # This function creates dummy columns to give names to the FIPS values
    df = get_counties(df)
    
    # This fuiction is used to create specific features like age, acres, etc. to help with exploration and modeling
    df = create_features(df)
    
    # This function drops unneccessary columns
    df = drop_columns(df)
    
    # Drop all remaining missing values
    df = df.dropna()
    
    # returns a cleaned and prepped df ready to be split/imputed
    return df

def train_validate_test(df, target):
    """
    this function takes in a dataframe and splits it into 3 samples,
    a test, which is 20% of the entire dataframe,
    a validate, which is 24% of the entire dataframe,
    and a train, which is 56% of the entire dataframe.
    It then splits each of the 3 samples into a dataframe with independent variables
    and a series with the dependent, or target variable.
    The function returns 3 dataframes and 3 series:
    X_train (df) & y_train (series), X_validate & y_validate, X_test & y_test.
    """
    # split df into test (20%) and train_validate (80%)
    train_validate, test = train_test_split(df, test_size=0.2, random_state=1221)

    # split train_validate off into train (70% of 80% = 56%) and validate (30% of 80% = 24%)
    train, validate = train_test_split(train_validate, test_size=0.3, random_state=1221)

    # split train into X (dataframe, drop target) & y (series, keep target only)
    X_train = train.drop(columns=[target])
    y_train = train[target]

    # split validate into X (dataframe, drop target) & y (series, keep target only)
    X_validate = validate.drop(columns=[target])
    y_validate = validate[target]

    # split test into X (dataframe, drop target) & y (series, keep target only)
    X_test = test.drop(columns=[target])
    y_test = test[target]

    return train, validate, test, X_train, y_train, X_validate, y_validate, X_test, y_test


# impute columns *do this after you split*

def impute_zillow(df, my_strategy, column_list):
    ''' take in a df, strategy, and cloumn list
        return df with listed columns imputed using input stratagy
    '''
        
    imputer = SimpleImputer(strategy=my_strategy)  # build imputer

    df[column_list] = imputer.fit_transform(df[column_list]) # fit/transform selected columns

    return df
    
    
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
            print('----------------------------------------------------')
            print('')
        else:
            print(df[col].value_counts(bins=10, sort=False))
            print('----------------------------------------------------')
            print('')
    print('----------------------------------------------------')
    print('Nulls in DataFrame by Column: ')
    print(nulls_by_col(df))
    print('----------------------------------------------------')
    print('Nulls in DataFrame by Rows: ')
    print(nulls_by_row(df))
    print('----------------------------------------------------')
    
    