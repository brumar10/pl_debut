# i want to analyze
# age at debut date
# number of appearances (minutes as well) in big 5 leagues v debut date
# number of appearances (minutes as well) in premier league v debut date
# position (do this for all positions) v debut date
# club debut date v ntl debut date
# nationality v debut date over time
# oldest debutants and youngest debutants
# write up on the ten youngest debutants
# write up on the ten oldest debutants
# what percentage of people on that list played for their national team
# do those that win their first game have better careers?
# do those who make their debut at a younger age play more international games?
# which team has most debutants
# usually do bad teams or good teams give debuts (get final league position)
# which month has most debuts
# oldest debutant in every year
# debutants by year, age
# number of premier league players ever: https://www.transfermarkt.us/premier-league/profidebuetanten/wettbewerb/GB1/plus/0/galerie/0?saisonIdVon=1992&saison_id=2022&option=liga
# compare the debut information of most expensive prem transfers, highest appearance makers
# this study is primarily concerned with how many premier league apps will be made by a player vs their age at pro debut?

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load data
main_df = pd.read_excel('premier-league-debut/final_dataset.xlsx', sheet_name=0)
goalie_df = pd.read_excel('premier-league-debut/final_dataset.xlsx', sheet_name=1)
apps_df = pd.read_excel('premier-league-debut/final_dataset.xlsx', sheet_name=2)

# exploratory data analysis
main_df.info()
print("The data set has ", main_df.shape[0], "rows and ", main_df.shape[1], "columns.")
num_desc = pd.DataFrame(main_df.describe())
# Average player will make 4-5 appearances in their debut season
# Average player will make 60 appearances in the Premier League
# Average debut age is 19.13 years
# Note these variables had high standard deviations

# the debut_dates column also has time, going to clean it
# I dont really care for the international debut date column so not going to clean it
main_df['debut_dates'] = pd.to_datetime(main_df['debut_dates']).dt.date
main_df['debut_date'] = pd.to_datetime(main_df['debut_dates'])
main_df = main_df.set_index('debut_date')
main_df["year"] = main_df.index.year
main_df["month"] = main_df.index.month
main_df.reset_index(drop=True)
print(main_df.month.value_counts())
# May is overwhelmingly the most common month for a premier league debut
main_df.month.value_counts().plot(kind="bar")
# Data Visualization for debut by year
main_df.year.value_counts().sort_index().plot(kind="bar")
# Debut by year and average age of debutant
import matplotlib.pyplot as plt
plt.scatter(main_df.month, main_df.club_debut_age)
plt.scatter(main_df.year, main_df.club_debut_age)
# Are these players who make a debut in May less successful?
plt.scatter(main_df.month, main_df.prem_apps)
plt.scatter(main_df.club_debut_age, main_df.prem_apps)
main_df.positions.value_counts()
plt.scatter(main_df.positions,main_df.club_debut_age)
# Lets see which months you are most likely to make your debut in

# new dataframe
main_df.head()