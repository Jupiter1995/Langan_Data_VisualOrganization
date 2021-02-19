#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def transferDF(df):
    df['date'] = pd.to_datetime(df['Date/Time'])
    df.columns = df.columns.str.lower()
    df.fillna(0, inplace=True)
    return df

def plotTrends(df, param):
    fig = plt.figure(figsize=(20, 5))
    plt.plot(df.date, df[param])
    plt.ylabel(param, size=10)
    plt.savefig(str(df.date.iloc[0].month) + param + ' vs Time')
    
def findShutdowns(df, param):
    """
    Two pointers to find the beginning of the shutdown, which has pressure lower than 1.
    Then finding the end time of the shutdown, which locates right after the last low pressure date.
    """
    #Define variables for storing the results
    ind1, ind2 = 0, 0
    n = len(df[param])
    sparge = df[param]
    date = df['date']
    starts = []
    ends = []

    #Find the shutdown events by selecting the start time and end time
    while ind1 < n and ind2 < n:
        ind1 = ind2
        while ind1 < n and sparge.iloc[ind1] > 1: ind1 += 1
        if ind1 < n: 
            starts.append(date.iloc[ind1]) #record start times
            ind2 = ind1 + 1
        else:
            break
            
        #Searching the end times 
        while ind2 < n and sparge.iloc[ind2] < 1: ind2 += 1
        if ind2 < n:
            ends.append(date.iloc[ind2 - 1])
        elif ind2 == n and sparge.iloc[ind2 - 1] < 1:
            ends.append(date.iloc[ind2 - 1])

    shutdowns = pd.DataFrame({'Starts': starts, 'Ends': ends})
    shutdowns['days'] = (shutdowns.Ends - shutdowns.Starts).apply(lambda x: x.days)
    res = shutdowns[shutdowns.days >= 7]
    return shutdowns, res


# In[ ]:




