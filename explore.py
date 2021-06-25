# This is where my Zillow Clustering Project Explore functions will go

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns



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