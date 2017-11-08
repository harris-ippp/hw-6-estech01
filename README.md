# Homework 6: Making and Scraping Websites

You can accept this assignment [here](https://classroom.github.com/assignment-invitations/66526f93dac8e6a95ed82fff64faad2b).  It is due Wednesday November 8 at 1:30am.

## Make A Simple Website [DONE]

* Using and adapting the example from class, make a small, professional website.  It can be about you, a topic, or balderdash.  But it should include:
  * A picture [x]
  * A table [x]
  * At least three sections [x]
  * A list (could be the nav bar) [x]
  * A navigation bar, with links to sections [x]
* You can host your website either on GitHub or on the university servers.[x]
* Whichever site you use for hosting, your main work should be in an index.html file.  You can upload additional resources -- pictures etc.  -- or "hotlink" to other resources on the net.  (Generally this is bad practice, but we aren't expecting these sites to get enormous traffic.) [x]
* Wherever you end up putting your site, you should put a link in the "WEBSITE" file in this repo, so we know where to look. [x]

## Elections in the Old Dominion

### The Data Source

Navigate to the [Virginia Historical Elections Database](http://historical.elections.virginia.gov/).  Click around.  What you will find is a "fairly common" mix of "standard" html with a slightly-hidden API.  The web address for Presidential elections is highly suggestive: [x]

http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2015/office_id:1/stage:General [x]

If you expand "Candidates »" for a single election and follow along to "[See Details for this Election »](http://historical.elections.virginia.gov/elections/view/44930/)", you'll end up at the results for that contest, with a URL that again suggests an API: [x]

http://historical.elections.virginia.gov/elections/view/44930/ [x]

Under "Actions" on the left hand side, click on "Download this election."  Right-click on the [Municipality Results](http://historical.elections.virginia.gov/elections/download/44930/precincts_include:0/) to get the link [x]

http://historical.elections.virginia.gov/elections/download/44930/precincts_include:0/ [x]

Again, it's pretty darn suggestive.  80871 is the election ID for the General Presiential Election in 2016.  Download the file.  It's a CSV!  [x]

So for any election, we can grab the low-level voting records really easily if we know its ID!  Unfortunately, the IDs are not (as far as I can tell) neatly exposed.  But they _are_ contained in the search results.  You'll have to scrape them out.

### Your Tasks

1. Using BeautifulSoup ([docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)), print, then save as ELECTION_ID, a list containing the years and election IDs in exactly this format.  [x]
   ```
   2016 80871
   2012 44930
   2008 39050
   2004 41055
   2000 39517
   ...  ...
   ```
   Save (and commit) your work in `e1.py`. &nbsp;<details><summary>Hints, step by step.</summary>
   If you are reading this, make sure you understand the big picture, before you try to implement the steps.
   Otherwise the steps will be meaningless and confusing.
     * Search within the the source for the first election id, 80871.  It appears twice, once in a row ID and once in a link.  I think the row will be easier to use. [x]
     * Set up your `soup` as we did in class: make the `requests.get()`, save it, and parse it. [x]
     * Grab all of the instances where the class is `election_item`, like `soup.find_all(tag_type, class_name)`, i.e., `soup.find_all("tr", "election_item")`. [x]
     * Extract the IDs; split them on dashes to extract the numbers. [x]
     * Now, _within that same row_ `row.find()` the cell containing the year, using the same syntax as above.  Recall that `find()` yields the first instance, instead of the list.  What are the tag and the class, now?  
     * Grab the year using `.string` (or `.contents[0]`). [x]

   Why is it that pandas is not well-suited to this task??
   </details>
2. Loop over your list from Part 1, and use requests to download the CSV files from.
   You will format them like so:
   ```
   http://historical.elections.virginia.gov/elections/download/{}/precincts_include:0/
   ```

   Save your work in `e2.py` and commit your csv file for the 2016 election, naming it `president_general_2016.csv`.

   Don't run parts 1 and 2 every time you do this part -- once it's downloaded leave it be!
   We don't want to bother the Virginia Election site too much! &nbsp;<details><summary>Hints</summary>
   * Loop over a file using: `for line in open("ELECTION_ID"):`.
   * You can print the contents of the response using `resp.text`.
     Instead, write them to files (see slide 8 of [lecture 3B](https://github.com/harris-ippp/lectures/raw/master/03/files.pdf)) with a meaningful name structure: [x]

     ```
     file_name = year +".csv"
     with open(file_name, "w") as out:
       out.write(resp.text)
     ```
   </details> [x]
3. Import your CSV files into a single `pandas.DataFrame()` and plot the Republican vote share in Accomack County, Albermarle County, Alexandria City, and Alleghany County as a fraction of Total Votes Cast.  Save your work as `e3.py` and commit your plots as: [x]
   `accomack_county.pdf`, `albemarle_county.pdf`, `alexandria_city.pdf`, and `alleghany_county.pdf`. &nbsp;<details><summary>Hints</summary>
   * The challenge is in the `read_csv()`: there are empty columns, and the 'relevant' column names (party names) are in the second row.  So you need to import that single row as a dictionary, to change the column names.  You can do the setup, like so
     ```
     header = pd.read_csv("president_general_2004.csv", nrows = 1).dropna(axis = 1)
     d = header.iloc[0].to_dict()

     df = pd.read_csv("president_general_2004.csv", index_col = 0,
                    thousands = ",", skiprows = [1])

     df.rename(inplace = True, columns = d) # rename to democrat/republican
     df.dropna(inplace = True, axis = 1)    # drop empty columns
     df["Year"] = 2004
     ```
   * Write a for loop, placing up all of your dataframes (elections) in a list.  Then `concat` them together.  You'll probably want just these columns:
     ```
     ["Democratic", "Republican", "Total Votes Cast", "Year"]
     ```
   * Then you just need to define a new column, Republican Share. [x]
   * You can either "select off" the column and plot the year, or you can [pivot](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pivot.html) all of the city/county names up as columns, keeping the
     * If you do this, you may want to deal with the counties that were occasionally split between congressional districts, "(CD X)".  You could do this by fixing the labels with a regular expression.  Then group by County/City, take the sum, and reset the index.
   </details>
