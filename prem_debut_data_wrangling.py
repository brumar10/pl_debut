import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from collections import defaultdict

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

url_list = []
base_url = "https://www.transfermarkt.us/premier-league/profidebuetanten/wettbewerb/GB1/saisonIdVon/1992/saison_id/2022/option/profi/plus/0/galerie/0/page/"
for page_number in range(1,56):
    url_with_page = urljoin(base_url,str(page_number))
    url_list.append(url_with_page)

#use these to restart lists
player_names = []
positions = []
nations = []
debut_teams = []
apps = []
team1s = []
scores = []
team2s = []
debut_dates = []
ages = []
player_urls = []


tally = 0



for url in url_list:
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    oplayer_dict = soup.find_all('tr', class_='odd')
    for player in oplayer_dict:
        tally += 1
        # section 1 (inline table: contains player name and position)
        player_name = player.find('td', class_='hauptlink').get_text()
        player_names.append([[player_name]])
        player_position = player.select('td')[3].get_text()
        positions.append([[player_position]])
        # section 2 (first "zentriert": contains player nation)
        player_nation = player.find('td', class_ = 'zentriert').img.get('alt')
        nations.append([[player_nation]])
        # section 3 (second "zentriert": contains team player debuted for)
        player_debut_team = player.find('td', class_ = 'zentriert').next_sibling.a.get('title')
        debut_teams.append([[player_debut_team]])
        # section 4 (zentriert hauplink: contains number of appearances in premier league in debut season)
        player_apps = player.find('td', class_ = 'zentriert hauptlink').get_text()
        apps.append([[player_apps]])
        # section 5 (zentriert match: contains information on debut)
        team1 = player.find('td', class_ = 'wappen_zelle rechts').a.get('title')
        team1s.append([[team1]])
        score = player.find('td', class_ = 'zentriert ergebnis').find('span').get_text()
        scores.append([[score]])
        team2 = player.find('td', class_ = 'wappen_zelle links').a.get('title')
        team2s.append([[team2]])
        debut_date = player.find('span', class_ = 'spielDatum').get_text()
        debut_dates.append([[debut_date]])
        # section 6 (rechts hauptlink: age at debut)
        age_at_debut = player.find('td', class_ = 'rechts hauptlink').get_text()
        ages.append([[age_at_debut]])
        # player url
        player_url = player.find('td', class_='hauptlink').a.get('href')
        player_urls.append([[player_url]])
    eplayer_dict = soup.find_all('tr', class_='even')
    for player in eplayer_dict:
        tally += 1
        print(tally)
        # section 1 (inline table: contains player name and position)
        player_name = player.find('td', class_='hauptlink').get_text()
        player_names.extend([[player_name]])
        player_position = player.select('td')[3].get_text()
        positions.append([[player_position]])
        # section 2 (first "zentriert": contains player nation)
        player_nation = player.find('td', class_='zentriert').img.get('alt')
        nations.append([[player_nation]])
        # section 3 (second "zentriert": contains team player debuted for)
        player_debut_team = player.find('td', class_='zentriert').next_sibling.a.get('title')
        debut_teams.append([[player_debut_team]])
        # section 4 (zentriert hauplink: contains number of appearances in premier league in debut season)
        player_apps = player.find('td', class_='zentriert hauptlink').get_text()
        apps.append([[player_apps]])
        # section 5 (zentriert match: contains information on debut)
        team1 = player.find('td', class_='wappen_zelle rechts').a.get('title')
        team1s.append([[team1]])
        score = player.find('td', class_='zentriert ergebnis').find('span').get_text()
        scores.append([[score]])
        team2 = player.find('td', class_='wappen_zelle links').a.get('title')
        team2s.append([[team2]])
        debut_date = player.find('span', class_='spielDatum').get_text()
        debut_dates.append([[debut_date]])
        # section 6 (rechts hauptlink: age at debut)
        age_at_debut = player.find('td', class_='rechts hauptlink').get_text()
        ages.append([[age_at_debut]])
        # player url
        player_url = player.find('td', class_='hauptlink').a.get('href')
        player_urls.append([[player_url]])

dict_data = {'player_names': player_names,
        'positions': positions,
        'nations': nations,
        'debut_teams' : debut_teams,
        'apps' : apps,
        'team1s' : team1s,
        'scores' : scores,
        'team2s' : team2s,
        'debut_dates' : debut_dates,
        'ages' : ages,
        'player_urls' : player_urls
}

bf = pd.DataFrame(dict_data)

# to open it in excel nd clean it a bit.. i removed "[[' .. /n .. ']]"
from pathlib import Path
filepath = Path("C:/Users/mfar4/PycharmProjects/11/bf.csv")
bf.to_csv(filepath)

bf_back = pd.read_csv('bf_edit.csv')
# now its back pretty :)
bf_back_pretty = bf_back.copy()
bf_back_pretty = bf_back_pretty.loc[:, ~bf_back_pretty.columns.str.contains('^Unnamed')]
bfbs = bf_back_pretty


pos_bfbs = bfbs['positions'].tolist()
name_bfbs = bfbs['name'].tolist()
dtl_club_url_bfbs = bfbs['detail_club_url'].tolist()
ntl_team_url_bfbs = bfbs['ntl_team_url'].tolist()
ids_bfbs = bfbs['ids'].tolist()
u_id_bfbs = bfbs['u_id'].tolist()

tal = 0

# create dictionary for club_data and ntl_data
club=defaultdict(list)
ntl=defaultdict(list)

# get career statistics for players
# here
for plr in range(1100,1312):
    u_id = u_id_bfbs[plr]
    dtl_club_u = dtl_club_url_bfbs[plr]
    pos = pos_bfbs[plr]
    transfer_og = "https://www.transfermarkt.us"
    clb_stats_url = urljoin(transfer_og,dtl_club_u)
    html_player_text = requests.get(clb_stats_url, headers=headers).text
    soup_player = BeautifulSoup(html_player_text, 'lxml')
    clb_player_tbody = soup_player.find('div', class_='responsive-table').tbody
    leagues = ['leagues']
    apps = ['apps']
    goals = ['goals']
    assists = ['assists']
    own_goals = ['own_goals']
    sub_on = ['sub_on']
    sub_off = ['sub_off']
    yellow = ['yellow']
    snd_yellow = ['snd_yellow']
    red = ['red']
    penalty_goals = ['penalty_goals']
    minutes_goal = ['minutes_goal']
    minutes = ['minutes']
    goals_conceded = ['goals_conceded']
    clean_sheets = ['clean_sheets']
    if pos == "Goalkeeper":
        for i in clb_player_tbody.find_all('tr', class_='odd'):
            # get league name
            leagues.append(i.find('td', class_='hauptlink no-border-links').text)
            apps.append(i.select('td')[2].text)
            goals.append(i.select('td')[3].text)
            own_goals.append(i.select('td')[4].text)
            sub_on.append(i.select('td')[5].text)
            sub_off.append(i.select('td')[6].text)
            yellow.append(i.select('td')[7].text)
            snd_yellow.append(i.select('td')[8].text)
            red.append(i.select('td')[9].text)
            goals_conceded.append(i.select('td')[10].text)
            clean_sheets.append(i.select('td')[11].text)
            minutes.append(i.select('td')[12].text)
        for e in clb_player_tbody.find_all('tr', class_='even'):
            # get league name
            leagues.append(e.find('td', class_='hauptlink no-border-links').text)
            apps.append(e.select('td')[2].text)
            goals.append(e.select('td')[3].text)
            own_goals.append(e.select('td')[4].text)
            sub_on.append(e.select('td')[5].text)
            sub_off.append(e.select('td')[6].text)
            yellow.append(e.select('td')[7].text)
            snd_yellow.append(e.select('td')[8].text)
            red.append(e.select('td')[9].text)
            goals_conceded.append(e.select('td')[10].text)
            clean_sheets.append(e.select('td')[11].text)
            minutes.append(e.select('td')[12].text)
        club[u_id].append(leagues)
        club[u_id].append(apps)
        club[u_id].append(goals)
        club[u_id].append(own_goals)
        club[u_id].append(sub_on)
        club[u_id].append(sub_off)
        club[u_id].append(yellow)
        club[u_id].append(snd_yellow)
        club[u_id].append(red)
        club[u_id].append(goals_conceded)
        club[u_id].append(clean_sheets)
        club[u_id].append(minutes)
        # national team data too
        ntl_team_u = ntl_team_url_bfbs[plr]
        ntl_stats_url = urljoin(transfer_og, ntl_team_u)
        n_html_player_text = requests.get(ntl_stats_url, headers=headers).text
        n_soup_player = BeautifulSoup(n_html_player_text, 'lxml')
        if n_soup_player.find('div', class_='box') == None:
            ntl[u_id].append('n/a')
        else:
            ntl_player_tbody = n_soup_player.find('div', class_='box').tbody
            national_team = ['national_team']
            intl_debut = ['intl_debut']
            intl_apps = ['intl_apps']
            intl_goals = ['intl_goals']
            intl_coach_at_debut = ['intl_coach_at_debut']
            intl_age_at_debut = ['intl_age_at_debut']
            if ntl_player_tbody.find('td', class_='zentriert bg_gruen_20') == None:
                ntl_team = ntl_player_tbody.select('tr')[1]
                national_team.append(
                    ntl_team.find('td', class_="hauptlink no-border-links hide-for-small").a.get_text())
                if ntl_team.select('td')[3].get_text() == None or ntl_team.select('td')[3].get_text().find('-') >= 0:
                    ntl[u_id].append('n/a')
                else:
                    intl_debut.append(ntl_team.select('td')[3].get_text())
                    intl_apps.append(ntl_team.select('td')[4].get_text())
                    intl_goals.append(ntl_team.select('td')[5].get_text())
                    try:
                        ntl_team.select('a')[3].get_text()
                    except IndexError:
                        intl_coach_at_debut.append('n/a')
                        intl_age_at_debut.append(ntl_team.find('td', class_='rechts').get_text())
                    else:
                        intl_coach_at_debut.append(ntl_team.select('a')[3].get_text())
                        intl_age_at_debut.append(ntl_team.find('td', class_='rechts').get_text())
                    ntl[u_id].append(national_team)
                    ntl[u_id].append(intl_debut)
                    ntl[u_id].append(intl_apps)
                    ntl[u_id].append(intl_goals)
                    ntl[u_id].append(intl_coach_at_debut)
                    ntl[u_id].append(intl_age_at_debut)
            else:
                ntl_team = ntl_player_tbody.select('tr')[1]
                national_team.append(
                    ntl_team.find('td', class_="hauptlink no-border-links hide-for-small").a.get_text())
                if ntl_team.select('a')[1].get_text() == None or ntl_team.select('a')[1].get_text().find('-') >= 0:
                    ntl[u_id].append('n/a')
                else:
                    intl_debut.append(ntl_team.select('a')[1].get_text())
                    intl_apps.append(ntl_team.select('a')[2].get_text())
                    intl_goals.append(ntl_team.select('a')[3].get_text())
                    try:
                        ntl_team.select('a')[4].get_text()
                    except IndexError:
                        intl_coach_at_debut.append('n/a')
                        intl_age_at_debut.append(ntl_team.find('td', class_='rechts').get_text())
                    else:
                        intl_coach_at_debut.append(ntl_team.select('a')[4].get_text())
                        intl_age_at_debut.append(ntl_team.find('td', class_='rechts').get_text())
                    ntl[u_id].append(national_team)
                    ntl[u_id].append(intl_debut)
                    ntl[u_id].append(intl_apps)
                    ntl[u_id].append(intl_goals)
                    ntl[u_id].append(intl_coach_at_debut)
                    ntl[u_id].append(intl_age_at_debut)
    else: #for non goalies
        for i in clb_player_tbody.find_all('tr', class_ = 'odd'):
            # get league name
            leagues.append(i.find('td', class_='hauptlink no-border-links').text)
            apps.append(i.select('td')[2].text)
            goals.append(i.select('td')[3].text)
            assists.append(i.select('td')[4].text)
            own_goals.append(i.select('td')[5].text)
            sub_on.append(i.select('td')[6].text)
            sub_off.append(i.select('td')[7].text)
            yellow.append(i.select('td')[8].text)
            snd_yellow.append(i.select('td')[9].text)
            red.append(i.select('td')[10].text)
            penalty_goals.append(i.select('td')[11].text)
            minutes_goal.append(i.select('td')[12].text)
            minutes.append(i.select('td')[13].text)
        for e in clb_player_tbody.find_all('tr', class_ = 'even'):
            # get league name
            leagues.append(e.find('td', class_='hauptlink no-border-links').text)
            apps.append(e.select('td')[2].text)
            goals.append(e.select('td')[3].text)
            assists.append(e.select('td')[4].text)
            own_goals.append(e.select('td')[5].text)
            sub_on.append(e.select('td')[6].text)
            sub_off.append(e.select('td')[7].text)
            yellow.append(e.select('td')[8].text)
            snd_yellow.append(e.select('td')[9].text)
            red.append(e.select('td')[10].text)
            penalty_goals.append(e.select('td')[11].text)
            minutes_goal.append(e.select('td')[12].text)
            minutes.append(e.select('td')[13].text)
        club[u_id].append(leagues)
        club[u_id].append(apps)
        club[u_id].append(goals)
        club[u_id].append(assists)
        club[u_id].append(own_goals)
        club[u_id].append(sub_on)
        club[u_id].append(sub_off)
        club[u_id].append(yellow)
        club[u_id].append(snd_yellow)
        club[u_id].append(red)
        club[u_id].append(penalty_goals)
        club[u_id].append(minutes_goal)
        club[u_id].append(minutes)
        #national team data too
        ntl_team_u = ntl_team_url_bfbs[plr]
        ntl_stats_url = urljoin(transfer_og,ntl_team_u)
        n_html_player_text = requests.get(ntl_stats_url, headers=headers).text
        n_soup_player = BeautifulSoup(n_html_player_text, 'lxml')
        if n_soup_player.find('div', class_='box') == None:
            ntl[u_id].append('n/a')
        else:
            ntl_player_tbody = n_soup_player.find('div', class_='box').tbody
            national_team = ['national_team']
            intl_debut = ['intl_debut']
            intl_apps = ['intl_apps']
            intl_goals = ['intl_goals']
            intl_coach_at_debut = ['intl_coach_at_debut']
            intl_age_at_debut = ['intl_age_at_debut']
            if ntl_player_tbody.find('td', class_='zentriert bg_gruen_20') == None:
                ntl_team = ntl_player_tbody.select('tr')[1]
                national_team.append(ntl_team.find('td', class_="hauptlink no-border-links hide-for-small").a.get_text())
                if ntl_team.select('td')[3].get_text() == None or ntl_team.select('td')[3].get_text().find('-') >= 0:
                    ntl[u_id].append('n/a')
                else:
                    intl_debut.append(ntl_team.select('td')[3].get_text())
                    intl_apps.append(ntl_team.select('td')[4].get_text())
                    intl_goals.append(ntl_team.select('td')[5].get_text())
                    try:
                        ntl_team.select('a')[3].get_text()
                    except IndexError:
                        intl_coach_at_debut.append('n/a')
                        intl_age_at_debut.append(ntl_team.find('td', class_='rechts').get_text())
                    else:
                        intl_coach_at_debut.append(ntl_team.select('a')[3].get_text())
                        intl_age_at_debut.append(ntl_team.find('td', class_='rechts').get_text())
                    ntl[u_id].append(national_team)
                    ntl[u_id].append(intl_debut)
                    ntl[u_id].append(intl_apps)
                    ntl[u_id].append(intl_goals)
                    ntl[u_id].append(intl_coach_at_debut)
                    ntl[u_id].append(intl_age_at_debut)
            else:
                ntl_team = ntl_player_tbody.select('tr')[1]
                national_team.append(ntl_team.find('td',class_ = "hauptlink no-border-links hide-for-small").a.get_text())
                if ntl_team.select('a')[1].get_text() == None or ntl_team.select('a')[1].get_text().find('-')>=0:
                    ntl[u_id].append('n/a')
                else:
                    intl_debut.append(ntl_team.select('a')[1].get_text())
                    intl_apps.append(ntl_team.select('a')[2].get_text())
                    intl_goals.append(ntl_team.select('a')[3].get_text())
                    try:
                        ntl_team.select('a')[4].get_text()
                    except IndexError:
                        intl_coach_at_debut.append('n/a')
                        intl_age_at_debut.append(ntl_team.find('td',class_='rechts').get_text())
                    else:
                        intl_coach_at_debut.append(ntl_team.select('a')[4].get_text())
                        intl_age_at_debut.append(ntl_team.find('td',class_='rechts').get_text())
                    ntl[u_id].append(national_team)
                    ntl[u_id].append(intl_debut)
                    ntl[u_id].append(intl_apps)
                    ntl[u_id].append(intl_goals)
                    ntl[u_id].append(intl_coach_at_debut)
                    ntl[u_id].append(intl_age_at_debut)



#got it :)
from pathlib import Path
bf = pd.DataFrame(club)
filepath_club = Path("C:/Users/mfar4/PycharmProjects/11/club_data.csv")
bf.to_csv(filepath_club)

bf = pd.DataFrame(ntl)
filepath_ntl = Path("C:/Users/mfar4/PycharmProjects/11/ntl_data.csv")
bf.to_csv(filepath_ntl)

# club_copy = club.copy()
# ntl_copy = ntl.copy()
#
# club_data= {
# 'assists' : assists,
# 'own_goals' : own_goals,
# 'sub_on' : sub_on,
# 'sub_off' : sub_off,
# 'yellow' : yellow,
# 'snd_yellow' : snd_yellow,
# 'red' : red,
# 'penalty_goals' : penalty_goals,
# 'minutes_goal' : minutes_goal,
# 'minutes' : minutes
# }
