# elayne stecher
# programming for public policy
# hw 6 part 3
import requests
import pandas as pd

df_list=[]
for line in open('ELECTION_ID'):
    s = line.rstrip().split(' ') # rstrip to take out end of line chars
    if len(s) == 2:
        year = s[0]
        file = 'president_general_{}.csv'.format(year)
        header = pd.read_csv(file,nrows=1).dropna(axis=1) # read header
        df = pd.read_csv(file,index_col=0,thousands=",",skiprows=[1]) # read data
        df.rename(inplace=True,columns=header.iloc[0].to_dict()) # set header to democratic/republican
        df.dropna(inplace=True,axis=1) # drop empty cols
        df.index = [idx.split(' (CD')[0] for idx in df.index]  # remove congressional district splits
        df = df.loc[['Accomack County','Albemarle County', # only keep rows/cols of interest
                     'Alexandria City','Alleghany County'],
                    ['Democratic','Republican','Total Votes Cast']]
        df = df.groupby(df.index).sum() # group and sum repeated counties
        df['Republican Share'] = df['Republican']/df['Total Votes Cast'] # set republican share
        df["Year"] = year # set year
        df_list.append(df)
df = pd.concat(df_list) # whole list

county = ['Accomack', 'Albemarle', 'Alexandria', 'Alleghany'] # counties we're looking at
years = [i for i in range(2016, 1920, -4)] # years we're looking at

for i in range(len(county)): # graphing the republican share of total votes/county
    graph = df[["Republican Share", "Year"]]
    graph = graph[df.index.str.startswith(county[i])]
    graph.index = graph.Year
    ax = graph.plot(title="{}".format(county[i]), legend=False)
    ax.set(xlabel='Year',ylabel='Republican Share')
    ax.invert_xaxis()
    if county[i] == 'Accomack':
        ax.figure.savefig('accomack_county.pdf')
    if county[i] == 'Albemarle':
        ax.figure.savefig('albemarle_county.pdf')
    if county[i] == 'Alexandria':
        ax.figure.savefig('alexandria_city.pdf')
    if county[i] == 'Alleghany':
        ax.figure.savefig('alleghany_county.pdf')
