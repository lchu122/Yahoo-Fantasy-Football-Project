# Fantasy Stats Data Scraper Exclusively for Tracy Bowl, the name of my League
# Wrapper provided by yql
# takes three arguments in command line: year start of week range, end of week range

# league_key and game_keys stored for each year

# stats pulls all data under <results> in a list. See YQL Console for an
# easier view. Unique <tags> are keys of a dictionary
# Multiple <tags> with the same name indicate these elements are all in a list


import yql
from yql.storage import FileTokenStore
import os

import fantasystats
import draftresults
import gspread
from sys import argv
from oauth2client.service_account import ServiceAccountCredentials


y3 = yql.ThreeLegged('insert client ID', 'insert client secret')

_cache_dir = 'C:\\Users\\Luke\\PycharmProjects\\YahooAPI'



if not os.access(_cache_dir, os.R_OK):

    os.mkdir(_cache_dir)

token_store = FileTokenStore(_cache_dir, secret='insert secret here')


stored_token = token_store.get('foo')

if not stored_token:

    # Do the dance

    request_token, auth_url = y3.get_token_and_auth_url()

    print "Visit url %s and get a verifier string" % auth_url

    verifier = raw_input("Enter the code: ")
    token = y3.get_access_token(request_token, verifier)
    token_store.set('foo', token)

else:

    # Check access_token is within 1hour-old and if not refresh it
    # and stash it

    token = y3.check_token(stored_token)

    if token != stored_token:

        token_store.set('foo', token)




'''
# scope = ['https://spreadsheets.google.com/feeds']
# credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_dict('insert file key', scope)
scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('insert file key', scope)



gc = gspread.authorize(credentials)
wks = gc.open("Tracy Bowl 2015").sheet1
# teamid = wks.range('A2:A11')
'''

team_owner =[]
teamid_name = []
teamid_num = range(1,11)  # ten team league


year = int(argv[1])

league_key = {2014: '331.l.89035', 2015: '348.l.145481'}

# oddity: this year there is no team 10 but a team 11, may be because someone got booted and another team added
# a better workaround might be to query teams and grab team names.
if year == 2014:
    teamid_num.pop()
    teamid_num.append(11)

team_key = [league_key[year] + '.t.' + str(k) for k in teamid_num]

# conversion done to fit syntax of query
week_start = argv[2]
week_end = argv[3]

if int(week_start) < int(week_end):
    week_range = range(int(week_start), int(week_end) + 1)
    week_range = [str(i) for i in week_range]
    week_input = ','.join(week_range)
    week_start += '-'  # for filename formatting purposes
else:
    week_input = week_start
    week_end = ''



'''
# loop through team_idname
i= -1

f = open("C:\Users\Luke\PycharmProjects\YahooAPI\\" + str(year) + "_yahoo_roster_week" + week_start + week_end + ".csv", 'w')
f.write("Owner|FirstName|LastName|Team|PlayerId|PlayerKey|Week|PointsScored|Position|SelectedPosition|Year\n")

# loop through each team
for id in teamid_num:
    stats_query = "select * from fantasysports.teams.roster.stats where team_key='" + league_key[year] + ".t." + str(id) + "' and week in (" + week_input + ")"
    stats_yql = y3.execute(stats_query, token=token)
    stats = stats_yql.rows
    # puts each week as an entry in a list

    #careful as name can be changed by manager in between seasons
    teamid_name.append(stats[0]['name'])
    i += 1
    # loop through each week
    for week in stats:

        # loop through each week's roster ( roster element is a player )
        for roster in week['roster']['players']['player']:
            fname = roster['name']['first']
            if not roster['name']['last']:
                lname = "none"
            else:
                lname = roster['name']['last']

            team = roster['editorial_team_abbr']
            weeknum = roster['player_stats']['week']
            totalpoints = roster['player_points']['total']

            f.write(teamid_name[i] + '|' + fname + '|' + lname + '|' + team + '|' + roster['player_id'] + '|' + roster['player_key'] + '|' + str(weeknum) + '|' + str(totalpoints) + '|' + roster['display_position'] + '|' + roster['selected_position']['position'] + "|" + str(year) + '\n')

   # print fantasystats.calculate_points_by_position(week)

f.close()
'''
'''
#get owners

f2 = open("C:\Users\Luke\PycharmProjects\YahooAPI\\" + str(year) + "_yahoo_managers.csv", 'w')
f2.write("Manager|TeamName|Year\n")

for id in teamid_num:
    stats_query = "select * from fantasysports.teams where team_key='" + league_key[year] + ".t." + str(id) + "'"
    stats_yql = y3.execute(stats_query, token=token)
    stats = stats_yql.rows

    f2.write(stats[0]['managers']['manager']['nickname'] + "|" + stats[0]['name'] + "|" + str(year) + "\n")

f2.close()
'''

'''
#matchups
winner = ''
f3 = open("C:\Users\Luke\PycharmProjects\YahooAPI\\" + str(year) + "_yahoo_matchups_week" + week_start + week_end + ".csv", 'w')
f3.write("Week|TeamOne|ProjectedScoreOne|ScoreOne|Winner|ScoreTwo|ProjectedScoreTwo|TeamTwo|Year\n")


stats_query = "select * from fantasysports.leagues.scoreboard where league_key='" + league_key[year] + "' and week in (" + week_input + ")"
stats_yql = y3.execute(stats_query, token=token)
stats = stats_yql.rows

for week in stats:
    weeknum = week['scoreboard']['week']
    # for yql same "keys" actually indicate lists
    # i.e. week['scoreboard']['matchups']['matchup'][0]
    for matchup in week['scoreboard']['matchups']['matchup']:

        #explictly written out for clarity, will always be two teams in a matchup
        team_one = matchup['teams']['team'][0]['name']
        team_two = matchup['teams']['team'][1]['name']

        projected_score_one = matchup['teams']['team'][0]['team_projected_points']['total']
        projected_score_two = matchup['teams']['team'][1]['team_projected_points']['total']

        score_one = matchup['teams']['team'][0]['team_points']['total']
        score_two = matchup['teams']['team'][1]['team_points']['total']

        if float(score_one) > float(score_two):
            winner = '>'
        elif float(score_two) > float(score_one):
            winner = '<'
        else:
            winner = '='

        f3.write(str(weeknum) + "|" + team_one + "|" + projected_score_one + "|" + score_one + "|" + winner + "|" + score_two + "|" + projected_score_two + "|" + team_two + "|" + str(year) + "\n")

f3.close()
'''

f4 = open("C:\Users\Luke\PycharmProjects\YahooAPI\\" + str(year) + "_yahoo_draft_results.csv", 'w')
f4.write('Round|Selection|Owner|Player|Position|SeasonTotal\n')

stats_query = "select * from fantasysports.draftresults where league_key='" + league_key[year] + "'"
stats_yql = y3.execute(stats_query, token=token)
stats = stats_yql.rows

# stats here is a list with one big entry

round_size = int(stats[0]['num_teams'])
draft_count = int(stats[0]['draft_results']['count'])

num_rounds = draft_count / round_size

# draft results are also in a list
draft_results = stats[0]['draft_results']['draft_result']

# sort into a dict with key as round number as value as list of picks for that round
draft_by_round = {}

for i in range(1, num_rounds + 1):
    draft_by_round[i] = [ draft_results[k] for k in range((i-1)*round_size, (i-1)*round_size + round_size)]



team_list ={}

for id in teamid_num:
    teams_query = "select * from fantasysports.teams where team_key='" + league_key[year] + ".t." + str(id) + "'"
    teams_yql = y3.execute(teams_query, token=token)
    teams = teams_yql.rows


    team_list[teams[0]['team_key']] = teams[0]['name']



# have to query each result to see points
# might be a workaround to reduce number of queries if we looked at team, but team rosters change



selection = 0

for round, draft in draft_by_round.items():
    for pick in draft:
        player_key = pick['player_key']
        player_query = "select * from fantasysports.players.stats where league_key='" + league_key[year] +"' and player_key='" + player_key + "'"
        player_yql = y3.execute(player_query, token=token)
        player = player_yql.rows



        team_owner = team_list[pick['team_key']]
        player_name = player[0]['name']['full']
        player_position = player[0]['display_position']
        season_total = player[0]['player_points']['total']

        selection += 1

        f4.write(str(round) + '|' + str(selection) + '|' +  team_owner + '|'  + player_name + '|' + player_position + '|' + season_total +"\n")









