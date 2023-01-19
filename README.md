# pl_debut

A project using Transfermarkt and the ENFA to investigate data on professional league debuts made in the Premier League.
I first scraped data from Transfermarkt using their league debutant information https://www.transfermarkt.us/premier-league/profidebuetanten/wettbewerb/GB1.
I set the parameters on Transfermarkt to show me all players that made their professional debut between 92/92 and 22/23.
For the headers in my code, I used the same ones as this FC Python article https://fcpython.com/blog/introduction-scraping-data-transfermarkt.
You can read my Python code 'prem_debut_data_wrangling.py' to see the nuances in getting every bit of data.
I first retrieved data from the league debutant list like their nationality, position, the team they debuted for, the result in their debut match, their age at debut, number of matches, etc. Basically all the data that comes from the compact view on Transfermarkt's list. I didn't think the data on the detailed view was very enlightening.
I then put all that data into a csv file which I cleaned manually on Excel.

Then, I created another giant chunk of code which scraped data from each individual player's page on Transfermarkt using their unique id which is present on the URLs.
Now, I had two more dictionaries that had club and international data for each player on the Transfermarkt list.
I then created two more csv files with those lists.
Now I had three csv files.
After cleaning the two new csv files I then went on to confirm the data using the English National Football Archive (ENFA).
A lot of the rows on the pro debutant list from Transfermarkt were not accurate. Many of the players had already made their debut in a professional league such as the English Second Division.
I then created a final Excel file with all the players who I had confirmed made their professional league debut in the Premier League.

My final data set for analysis was comprised only of these specific players. Player who made their professional league debut in the Premier League. Even if they played a cup match or continental match before their professional league debut, I included them because those were not league matches.
I then conducted a brief analysis on Python, followed by a more in depth analysis on Tableau.
