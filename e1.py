# elayne stecher
# programming for public policy
# hw 6 part 1

import requests
# read in webpage
resp = requests.get('http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2016/office_id:1/stage:General')
from bs4 import BeautifulSoup as bs
soup = bs(resp.content, "html.parser")
# find relevant parts of HTML code
S = soup.find_all("tr", "election_item")
# access election year and code

out_file = open("ELECTION_ID", "w")
print("'''", file = out_file)
for i in range(len(S)):
     a = S[i]['id'].split('-')[-1]
     b = S[i].find_all("td","year first")[0].get_text()
     print(b, a, file = out_file)
print("'''", file = out_file)
