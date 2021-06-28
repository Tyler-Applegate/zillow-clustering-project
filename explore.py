# This is where my Zillow Clustering Project Explore functions will go

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler



def plot_variable_dist(df, figsize = (3,2)):
    '''
    This function is for exploring. Takes in a dataframe with variables you would like to 
    see the distribution of.
    Input the dataframe (either fully, or using .drop) with ONLY the columns you want to see plotted. 
    Optional argument figsize. Default it's small. 
    BTW if you just put list(df) it pulls out only the column names
    '''
    # loop through columns and use seaborn to plot distributions
    for col in list(df):
            plt.figure(figsize=figsize)
            plt.hist(data = df, x = col)
            plt.hist(df[np.isfinite(df[col])].values)
            plt.title(f'Distribution of {col}')
            plt.show()
            print(f'Number of Nulls: {df[col].isnull().sum()}')
            print('--------------------------------------')
            
            
def zillow_dummies(train, validate, test, dummy):
    '''
    This function takes in train, validate, and test dataframes, as well as a target variable,
    (target is a string) and creates dummies on each dataframe. Then returns the updated train,
    validate, and test DataFrames.
    '''

#     Create dummy variables of the target variable for the train DataFrame.
    dummy_train = pd.get_dummies(train[[dummy]], dummy_na=False, drop_first=True)
# let's put it all together...
    train = pd.concat([train, dummy_train], axis=1)
#     Create dummy variables of the target variable for the validate DataFrame.
    dummy_validate = pd.get_dummies(validate[[dummy]], dummy_na=False, drop_first=True)
# let's put it all together...
    validate = pd.concat([validate, dummy_validate], axis=1)
#     Create dummy variables of the target variable for the test DataFrame.
    dummy_test = pd.get_dummies(test[[dummy]], dummy_na=False, drop_first=True)
# let's put it all together...
    test = pd.concat([test, dummy_test], axis=1)
    
    return train, validate, test

def plot_vars_target(df, target, variables, figsize = (6,4), hue = None):
    '''
    Takes in dataframe, target and varialbe list, and plots against target. 
    '''
    for var in variables:
        plt.figure(figsize = (figsize))
        sns.regplot(data = df, x = var, y = target, 
                    line_kws={'color': 'black'})
        plt.show()
        
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

def scale_my_data(df, scalertype):
    '''
    df = dataframe with columns you need scaled
    scalertype = something like StandardScaler(), or MinMaxScaler()
    This function takes a dataframe (an X data), a scaler, and ouputs a new dataframe with those columns scaled. 
    And a scaler to inverse transforming
    '''
    scaler = scalertype.fit(df)

    X_scaled = pd.DataFrame(scaler.transform(df), columns = df.columns).set_index([df.index.values])
    
    return X_scaled, scaler

        
        

        