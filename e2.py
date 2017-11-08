# elayne stecher
# programming for public policy
# hw 6 part 2

import requests
# use election_id data to download csv files per election
for line in open('ELECTION_ID'):
    s = line.rstrip().split(' ') # rstrip to take out end of line chars
    if len(s) == 2:
        year = s[0]
        ID = s[1]
        URL = 'http://historical.elections.virginia.gov/elections/download/{}/precincts_include:0/'.format(ID)
        name = 'president_general_{}.csv'.format(year) # format name
        resp = requests.get(URL) # call up URL
        with open(name, "w") as out: # write as file
            out.write(resp.text)
        #print(year, ID, URL, name)
