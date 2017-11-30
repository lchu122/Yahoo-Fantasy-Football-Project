
# Tracy Bowl 2017 Stats
<script>
  function code_toggle() {
    if (code_shown){
      $('div.input').hide('500');
      $('#toggleButton').val('Show Code')
    } else {
      $('div.input').show('500');
      $('#toggleButton').val('Hide Code')
    }
    code_shown = !code_shown
  }

  $( document ).ready(function(){
    code_shown=false;
    $('div.input').hide()
  });
</script>
<form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Show Code"></form>

```python
# refactor with pandas
import pandas as pd
import numpy as np
import math
from collections import Counter

from IPython.display import display, HTML


```


```python
# manually update to reflect most up-to-date week
matchups = pd.read_csv("2017_yahoo_matchups_week1-12.csv",delimiter='|')
weeks_elapsed = 12


```

## All Matchups


```python
matchups.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Week</th>
      <th>TeamOne</th>
      <th>Proj.ScoreOne</th>
      <th>ScoreOne</th>
      <th>Winner</th>
      <th>ScoreTwo</th>
      <th>Proj.ScoreTwo</th>
      <th>TeamTwo</th>
      <th>Year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>The Golden Yogis</td>
      <td>116.14</td>
      <td>84.22</td>
      <td>&lt;</td>
      <td>114.70</td>
      <td>114.64</td>
      <td>Sean McBae</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Clippernation</td>
      <td>113.36</td>
      <td>93.12</td>
      <td>&gt;</td>
      <td>91.72</td>
      <td>120.17</td>
      <td>TeamGooseEggs</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>Butkicker&amp;Tygod</td>
      <td>120.96</td>
      <td>69.84</td>
      <td>&lt;</td>
      <td>81.12</td>
      <td>100.64</td>
      <td>LordN’Savior Josh G</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>Sit4Anthems</td>
      <td>118.75</td>
      <td>114.94</td>
      <td>&gt;</td>
      <td>91.58</td>
      <td>118.03</td>
      <td>BigBradyBrand</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>Team 8</td>
      <td>122.70</td>
      <td>121.84</td>
      <td>&gt;</td>
      <td>98.98</td>
      <td>109.05</td>
      <td>Healthyplayersplz</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2</td>
      <td>The Golden Yogis</td>
      <td>120.19</td>
      <td>109.52</td>
      <td>&lt;</td>
      <td>110.62</td>
      <td>120.81</td>
      <td>Team 8</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2</td>
      <td>Clippernation</td>
      <td>112.58</td>
      <td>125.82</td>
      <td>&gt;</td>
      <td>100.42</td>
      <td>119.05</td>
      <td>Butkicker&amp;Tygod</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2</td>
      <td>Sean McBae</td>
      <td>115.00</td>
      <td>103.96</td>
      <td>&lt;</td>
      <td>128.18</td>
      <td>122.92</td>
      <td>LordN’Savior Josh G</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2</td>
      <td>TeamGooseEggs</td>
      <td>125.30</td>
      <td>90.26</td>
      <td>&gt;</td>
      <td>65.40</td>
      <td>109.84</td>
      <td>Sit4Anthems</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2</td>
      <td>BigBradyBrand</td>
      <td>118.63</td>
      <td>87.88</td>
      <td>&lt;</td>
      <td>95.58</td>
      <td>117.55</td>
      <td>Healthyplayersplz</td>
      <td>2017</td>
    </tr>
  </tbody>
</table>
</div>




```python
# sort by score per week
matchups_stacked = pd.DataFrame()

for i in range(1, weeks_elapsed+1): 
    # alternatively matchups[["Week"], ...].filter_by(1, "Week")
    matchup_week_score = matchups[matchups["Week"]==i][["Week", "TeamOne", "Proj.ScoreOne", "ScoreOne" ]] 
    matchup_week_score.rename(columns = {"TeamOne":"Team", "Proj.ScoreOne":"Proj.Score", "ScoreOne":"Score"}, 
                              inplace = True)
    
    matchup_week_score_two = matchups[matchups["Week"]==i][["Week", "TeamTwo", "Proj.ScoreTwo", "ScoreTwo" ]] 
    matchup_week_score_two.rename(columns = {"TeamTwo":"Team", "Proj.ScoreTwo":"Proj.Score", "ScoreTwo":"Score"}, 
                                  inplace = True)

    matchup_week_score = matchup_week_score.append(matchup_week_score_two)
    matchup_week_score = matchup_week_score.sort_values(["Score"], ascending = False) \
    .assign(WeeklyBeaten = range(matchup_week_score.shape[0] - 1, -1, -1))
    
    matchups_stacked = matchups_stacked.append(matchup_week_score)

matchups_stacked = matchups_stacked.reset_index(drop=True)

n_teams = matchups_stacked[matchups_stacked["Week"] == 1].shape[0]

```

## Sorted Scores Per Week


```python
matchups_stacked.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Week</th>
      <th>Team</th>
      <th>Proj.Score</th>
      <th>Score</th>
      <th>WeeklyBeaten</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Team 8</td>
      <td>122.70</td>
      <td>121.84</td>
      <td>9</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Sit4Anthems</td>
      <td>118.75</td>
      <td>114.94</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>Sean McBae</td>
      <td>114.64</td>
      <td>114.70</td>
      <td>7</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>Healthyplayersplz</td>
      <td>109.05</td>
      <td>98.98</td>
      <td>6</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>Clippernation</td>
      <td>113.36</td>
      <td>93.12</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1</td>
      <td>TeamGooseEggs</td>
      <td>120.17</td>
      <td>91.72</td>
      <td>4</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1</td>
      <td>BigBradyBrand</td>
      <td>118.03</td>
      <td>91.58</td>
      <td>3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1</td>
      <td>The Golden Yogis</td>
      <td>116.14</td>
      <td>84.22</td>
      <td>2</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1</td>
      <td>LordN’Savior Josh G</td>
      <td>100.64</td>
      <td>81.12</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1</td>
      <td>Butkicker&amp;Tygod</td>
      <td>120.96</td>
      <td>69.84</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Expected Wins = TotalNumBeaten / Num_Opponents
# AvgBeatenPerWeek = TotalNumBeaten / Weeks

# next steps: include actual wins from API

matchup_wins_list = [matchups['TeamOne'][k] if matchups['Winner'][k] == '>' else matchups['TeamTwo'][k] \
                   for k in range(matchups.shape[0])]

matchup_wins_count = dict(Counter(matchup_wins_list))
keys, values = matchup_wins_count.keys(), matchup_wins_count.values()


matchup_wins_count_df = pd.DataFrame.from_items([('Team', list(keys)), ('Wins', list(values))])


num_opponents = matchups.shape[0] / weeks_elapsed * 2 - 1
 
expected_wins = matchups_stacked.groupby(["Team"], as_index = False).agg({"WeeklyBeaten": "sum"}) \
.rename(columns = {"WeeklyBeaten": "TotalBeaten"})

expected_wins = expected_wins.assign(ExpectedWins = expected_wins["TotalBeaten"] / num_opponents) \
.assign(AvgBeatPerWeek = expected_wins["TotalBeaten"] / weeks_elapsed) \
.sort_values("ExpectedWins", ascending = False)

expected_wins = expected_wins[["Team", "ExpectedWins", "AvgBeatPerWeek"]].round(2).reset_index(drop=True)

expected_wins = expected_wins.merge(matchup_wins_count_df, on ="Team", how = "outer")

expected_wins = expected_wins[["Team", "Wins", "ExpectedWins", "AvgBeatPerWeek"]]



```

## Expected Wins


```python
expected_wins
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>Wins</th>
      <th>ExpectedWins</th>
      <th>AvgBeatPerWeek</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sean McBae</td>
      <td>8</td>
      <td>7.89</td>
      <td>5.92</td>
    </tr>
    <tr>
      <th>1</th>
      <td>LordN’Savior Josh G</td>
      <td>9</td>
      <td>7.22</td>
      <td>5.42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BigBradyBrand</td>
      <td>5</td>
      <td>7.11</td>
      <td>5.33</td>
    </tr>
    <tr>
      <th>3</th>
      <td>TeamGooseEggs</td>
      <td>8</td>
      <td>7.11</td>
      <td>5.33</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Team 8</td>
      <td>5</td>
      <td>6.00</td>
      <td>4.50</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Healthyplayersplz</td>
      <td>5</td>
      <td>5.67</td>
      <td>4.25</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Clippernation</td>
      <td>7</td>
      <td>5.56</td>
      <td>4.17</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Butkicker&amp;Tygod</td>
      <td>7</td>
      <td>4.78</td>
      <td>3.58</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Sit4Anthems</td>
      <td>3</td>
      <td>4.33</td>
      <td>3.25</td>
    </tr>
    <tr>
      <th>9</th>
      <td>The Golden Yogis</td>
      <td>3</td>
      <td>4.33</td>
      <td>3.25</td>
    </tr>
  </tbody>
</table>
</div>



## Point Differentials


```python
# Calculate Point Diff
# Point Diff is the score difference per matchup
matchups['Diff'] = abs(matchups['ScoreOne'] - matchups['ScoreTwo'])
matchups.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Week</th>
      <th>TeamOne</th>
      <th>Proj.ScoreOne</th>
      <th>ScoreOne</th>
      <th>Winner</th>
      <th>ScoreTwo</th>
      <th>Proj.ScoreTwo</th>
      <th>TeamTwo</th>
      <th>Year</th>
      <th>Diff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>The Golden Yogis</td>
      <td>116.14</td>
      <td>84.22</td>
      <td>&lt;</td>
      <td>114.70</td>
      <td>114.64</td>
      <td>Sean McBae</td>
      <td>2017</td>
      <td>30.48</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Clippernation</td>
      <td>113.36</td>
      <td>93.12</td>
      <td>&gt;</td>
      <td>91.72</td>
      <td>120.17</td>
      <td>TeamGooseEggs</td>
      <td>2017</td>
      <td>1.40</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>Butkicker&amp;Tygod</td>
      <td>120.96</td>
      <td>69.84</td>
      <td>&lt;</td>
      <td>81.12</td>
      <td>100.64</td>
      <td>LordN’Savior Josh G</td>
      <td>2017</td>
      <td>11.28</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>Sit4Anthems</td>
      <td>118.75</td>
      <td>114.94</td>
      <td>&gt;</td>
      <td>91.58</td>
      <td>118.03</td>
      <td>BigBradyBrand</td>
      <td>2017</td>
      <td>23.36</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>Team 8</td>
      <td>122.70</td>
      <td>121.84</td>
      <td>&gt;</td>
      <td>98.98</td>
      <td>109.05</td>
      <td>Healthyplayersplz</td>
      <td>2017</td>
      <td>22.86</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2</td>
      <td>The Golden Yogis</td>
      <td>120.19</td>
      <td>109.52</td>
      <td>&lt;</td>
      <td>110.62</td>
      <td>120.81</td>
      <td>Team 8</td>
      <td>2017</td>
      <td>1.10</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2</td>
      <td>Clippernation</td>
      <td>112.58</td>
      <td>125.82</td>
      <td>&gt;</td>
      <td>100.42</td>
      <td>119.05</td>
      <td>Butkicker&amp;Tygod</td>
      <td>2017</td>
      <td>25.40</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2</td>
      <td>Sean McBae</td>
      <td>115.00</td>
      <td>103.96</td>
      <td>&lt;</td>
      <td>128.18</td>
      <td>122.92</td>
      <td>LordN’Savior Josh G</td>
      <td>2017</td>
      <td>24.22</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2</td>
      <td>TeamGooseEggs</td>
      <td>125.30</td>
      <td>90.26</td>
      <td>&gt;</td>
      <td>65.40</td>
      <td>109.84</td>
      <td>Sit4Anthems</td>
      <td>2017</td>
      <td>24.86</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2</td>
      <td>BigBradyBrand</td>
      <td>118.63</td>
      <td>87.88</td>
      <td>&lt;</td>
      <td>95.58</td>
      <td>117.55</td>
      <td>Healthyplayersplz</td>
      <td>2017</td>
      <td>7.70</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Biggest Blowouts: top 10 point largest differentials in season
biggest_blowouts = matchups.nlargest(10, 'Diff')

# quick and dirty way to restack winners on one side: use lists
winner = list(biggest_blowouts["Winner"])
index = [x for x in range(0, len(winner)) if winner[x] == '<']
team_one = list(biggest_blowouts["TeamOne"])
team_two = list(biggest_blowouts["TeamTwo"])
score_one = list(biggest_blowouts["ScoreOne"])
score_two = list(biggest_blowouts["ScoreTwo"])

temp_team = list(team_one)
temp_score = list(score_one)

# swap team one and two and sign if winner is on right side, so winner is on left side
for i in index:
    team_one[i] = team_two[i]
    score_one[i] = score_two[i]
    team_two[i] = temp_team[i]
    score_two[i] = temp_score[i]
    winner[i] = '>'

biggest_blowouts["TeamOne"] = team_one
biggest_blowouts["TeamTwo"] = team_two
biggest_blowouts["ScoreOne"] = score_one
biggest_blowouts["ScoreTwo"] = score_two
biggest_blowouts["Winner"] = winner


```

### Biggest Blowouts


```python
biggest_blowouts.reset_index(drop=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Week</th>
      <th>TeamOne</th>
      <th>Proj.ScoreOne</th>
      <th>ScoreOne</th>
      <th>Winner</th>
      <th>ScoreTwo</th>
      <th>Proj.ScoreTwo</th>
      <th>TeamTwo</th>
      <th>Year</th>
      <th>Diff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12</td>
      <td>Sean McBae</td>
      <td>103.02</td>
      <td>182.44</td>
      <td>&gt;</td>
      <td>92.38</td>
      <td>134.84</td>
      <td>Clippernation</td>
      <td>2017</td>
      <td>90.06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>BigBradyBrand</td>
      <td>122.59</td>
      <td>151.28</td>
      <td>&gt;</td>
      <td>83.70</td>
      <td>129.99</td>
      <td>LordN’Savior Josh G</td>
      <td>2017</td>
      <td>67.58</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6</td>
      <td>TeamGooseEggs</td>
      <td>102.25</td>
      <td>136.44</td>
      <td>&gt;</td>
      <td>74.46</td>
      <td>125.67</td>
      <td>The Golden Yogis</td>
      <td>2017</td>
      <td>61.98</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5</td>
      <td>TeamGooseEggs</td>
      <td>112.95</td>
      <td>157.16</td>
      <td>&gt;</td>
      <td>96.26</td>
      <td>118.86</td>
      <td>Sean McBae</td>
      <td>2017</td>
      <td>60.90</td>
    </tr>
    <tr>
      <th>4</th>
      <td>8</td>
      <td>LordN’Savior Josh G</td>
      <td>109.88</td>
      <td>135.50</td>
      <td>&gt;</td>
      <td>78.26</td>
      <td>107.83</td>
      <td>TeamGooseEggs</td>
      <td>2017</td>
      <td>57.24</td>
    </tr>
    <tr>
      <th>5</th>
      <td>3</td>
      <td>BigBradyBrand</td>
      <td>117.36</td>
      <td>130.32</td>
      <td>&gt;</td>
      <td>76.66</td>
      <td>117.79</td>
      <td>The Golden Yogis</td>
      <td>2017</td>
      <td>53.66</td>
    </tr>
    <tr>
      <th>6</th>
      <td>4</td>
      <td>TeamGooseEggs</td>
      <td>124.77</td>
      <td>132.82</td>
      <td>&gt;</td>
      <td>80.62</td>
      <td>122.35</td>
      <td>Healthyplayersplz</td>
      <td>2017</td>
      <td>52.20</td>
    </tr>
    <tr>
      <th>7</th>
      <td>4</td>
      <td>Sean McBae</td>
      <td>121.31</td>
      <td>114.68</td>
      <td>&gt;</td>
      <td>62.86</td>
      <td>112.87</td>
      <td>Butkicker&amp;Tygod</td>
      <td>2017</td>
      <td>51.82</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>Butkicker&amp;Tygod</td>
      <td>97.26</td>
      <td>118.60</td>
      <td>&gt;</td>
      <td>68.32</td>
      <td>102.36</td>
      <td>The Golden Yogis</td>
      <td>2017</td>
      <td>50.28</td>
    </tr>
    <tr>
      <th>9</th>
      <td>8</td>
      <td>BigBradyBrand</td>
      <td>122.21</td>
      <td>135.62</td>
      <td>&gt;</td>
      <td>89.28</td>
      <td>101.15</td>
      <td>Team 8</td>
      <td>2017</td>
      <td>46.34</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Smallest Squeakers: top 10 smallest point differentials in season
smallest_squeakers = matchups.nsmallest(10, 'Diff')

# quick and dirty way to restack winners on one side: use lists
winner = list(smallest_squeakers["Winner"])
index = [x for x in range(0, len(winner)) if winner[x] == '<']
team_one = list(smallest_squeakers["TeamOne"])
team_two = list(smallest_squeakers["TeamTwo"])
score_one = list(smallest_squeakers["ScoreOne"])
score_two = list(smallest_squeakers["ScoreTwo"])

temp_team = list(team_one)
temp_score = list(score_one)

# swap team one and two and sign if winner is on right side, so winner is on left side
for i in index:
    team_one[i] = team_two[i]
    score_one[i] = score_two[i]
    team_two[i] = temp_team[i]
    score_two[i] = temp_score[i]
    winner[i] = '>'

smallest_squeakers["TeamOne"] = team_one
smallest_squeakers["TeamTwo"] = team_two
smallest_squeakers["ScoreOne"] = score_one
smallest_squeakers["ScoreTwo"] = score_two
smallest_squeakers["Winner"] = winner

```

### Smallest Squeakers


```python
smallest_squeakers.reset_index(drop=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Week</th>
      <th>TeamOne</th>
      <th>Proj.ScoreOne</th>
      <th>ScoreOne</th>
      <th>Winner</th>
      <th>ScoreTwo</th>
      <th>Proj.ScoreTwo</th>
      <th>TeamTwo</th>
      <th>Year</th>
      <th>Diff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>Team 8</td>
      <td>120.19</td>
      <td>110.62</td>
      <td>&gt;</td>
      <td>109.52</td>
      <td>120.81</td>
      <td>The Golden Yogis</td>
      <td>2017</td>
      <td>1.10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Clippernation</td>
      <td>113.36</td>
      <td>93.12</td>
      <td>&gt;</td>
      <td>91.72</td>
      <td>120.17</td>
      <td>TeamGooseEggs</td>
      <td>2017</td>
      <td>1.40</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7</td>
      <td>LordN’Savior Josh G</td>
      <td>116.21</td>
      <td>93.62</td>
      <td>&gt;</td>
      <td>90.74</td>
      <td>110.73</td>
      <td>The Golden Yogis</td>
      <td>2017</td>
      <td>2.88</td>
    </tr>
    <tr>
      <th>3</th>
      <td>7</td>
      <td>Butkicker&amp;Tygod</td>
      <td>108.48</td>
      <td>106.52</td>
      <td>&gt;</td>
      <td>103.08</td>
      <td>99.62</td>
      <td>Sit4Anthems</td>
      <td>2017</td>
      <td>3.44</td>
    </tr>
    <tr>
      <th>4</th>
      <td>11</td>
      <td>Healthyplayersplz</td>
      <td>114.64</td>
      <td>115.46</td>
      <td>&gt;</td>
      <td>111.80</td>
      <td>103.95</td>
      <td>BigBradyBrand</td>
      <td>2017</td>
      <td>3.66</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>LordN’Savior Josh G</td>
      <td>115.44</td>
      <td>151.26</td>
      <td>&gt;</td>
      <td>146.98</td>
      <td>114.73</td>
      <td>Healthyplayersplz</td>
      <td>2017</td>
      <td>4.28</td>
    </tr>
    <tr>
      <th>6</th>
      <td>10</td>
      <td>The Golden Yogis</td>
      <td>98.73</td>
      <td>91.88</td>
      <td>&gt;</td>
      <td>87.44</td>
      <td>96.16</td>
      <td>Clippernation</td>
      <td>2017</td>
      <td>4.44</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>Clippernation</td>
      <td>122.94</td>
      <td>93.52</td>
      <td>&gt;</td>
      <td>87.96</td>
      <td>99.51</td>
      <td>The Golden Yogis</td>
      <td>2017</td>
      <td>5.56</td>
    </tr>
    <tr>
      <th>8</th>
      <td>10</td>
      <td>LordN’Savior Josh G</td>
      <td>102.75</td>
      <td>97.58</td>
      <td>&gt;</td>
      <td>90.60</td>
      <td>101.97</td>
      <td>Sit4Anthems</td>
      <td>2017</td>
      <td>6.98</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2</td>
      <td>Healthyplayersplz</td>
      <td>118.63</td>
      <td>95.58</td>
      <td>&gt;</td>
      <td>87.88</td>
      <td>117.55</td>
      <td>BigBradyBrand</td>
      <td>2017</td>
      <td>7.70</td>
    </tr>
  </tbody>
</table>
</div>



## Avg Win/Loss Differential


```python
# matchups.groupby(["TeamOne", "Winner"], ).agg({'Winner': "count"}).rename(columns = {"Winner": "Wins"}).reset_index()
matchups_flipped = matchups.assign(Winner_Flipped = ['>' if i == '<' else '<' for i in list(matchups['Winner'])])
m1 = matchups.groupby(["TeamOne", "Winner"], ).Diff.agg(['count', 'sum'])
m2 = matchups_flipped.groupby(["TeamTwo", "Winner_Flipped"], ).Diff.agg(['count', 'sum'])

midx1 = pd.MultiIndex.from_product([m1.index.levels[0], ['>', '<']])
midx2 = pd.MultiIndex.from_product([m2.index.levels[0], ['>', '<']])

matchup_wins_one = m1.reindex(midx1, fill_value = 0).reset_index() \
.rename(columns = {"level_0": "Team", "level_1": "W/L", "count": "Count", "sum": "Diff"})
matchup_wins_two = m2.reindex(midx2, fill_value = 0).reset_index() \
.rename(columns = {"level_0": "Team", "level_1": "W/L", "count": "Count", "sum": "Diff"})

#matchup_wins_two

```


```python
# outer join in case a team is not in either side of the matchups

matchup_wins_stacked = matchup_wins_one.merge(matchup_wins_two, on=["Team", "W/L"], how="outer")
matchup_wins_stacked['Count_x'] = matchup_wins_stacked['Count_x'].fillna(0)
matchup_wins_stacked['Count_y'] = matchup_wins_stacked['Count_y'].fillna(0)
matchup_wins_stacked['Diff_x'] = matchup_wins_stacked['Diff_x'].fillna(0)
matchup_wins_stacked['Diff_y'] = matchup_wins_stacked['Diff_y'].fillna(0)

matchup_wins_stacked

matchup_wins_final = matchup_wins_stacked[['Team', 'W/L']] \
.assign(Count = matchup_wins_stacked['Count_x'] + matchup_wins_stacked['Count_y']) \
.assign(Diff = matchup_wins_stacked['Diff_x'] + matchup_wins_stacked['Diff_y'])

matchup_wins_final = matchup_wins_final.assign(AvgDiff = matchup_wins_final['Diff'] / matchup_wins_final['Count']).round(2)

matchup_wins_final['Count'] = matchup_wins_final['Count'].astype('int')
matchup_wins_final['W/L'] = ["Wins" if k == ">" else "Losses" for k in matchup_wins_final['W/L']]


```

### Avg Differential by Team


```python
matchup_wins_final
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>W/L</th>
      <th>Count</th>
      <th>Diff</th>
      <th>AvgDiff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BigBradyBrand</td>
      <td>Wins</td>
      <td>5</td>
      <td>208.76</td>
      <td>41.75</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BigBradyBrand</td>
      <td>Losses</td>
      <td>7</td>
      <td>112.78</td>
      <td>16.11</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Butkicker&amp;Tygod</td>
      <td>Wins</td>
      <td>7</td>
      <td>176.88</td>
      <td>25.27</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Butkicker&amp;Tygod</td>
      <td>Losses</td>
      <td>5</td>
      <td>139.02</td>
      <td>27.80</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Clippernation</td>
      <td>Wins</td>
      <td>7</td>
      <td>121.22</td>
      <td>17.32</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Clippernation</td>
      <td>Losses</td>
      <td>5</td>
      <td>134.68</td>
      <td>26.94</td>
    </tr>
    <tr>
      <th>6</th>
      <td>LordN’Savior Josh G</td>
      <td>Wins</td>
      <td>9</td>
      <td>173.36</td>
      <td>19.26</td>
    </tr>
    <tr>
      <th>7</th>
      <td>LordN’Savior Josh G</td>
      <td>Losses</td>
      <td>3</td>
      <td>108.66</td>
      <td>36.22</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Sean McBae</td>
      <td>Wins</td>
      <td>8</td>
      <td>294.34</td>
      <td>36.79</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Sean McBae</td>
      <td>Losses</td>
      <td>4</td>
      <td>120.96</td>
      <td>30.24</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Sit4Anthems</td>
      <td>Wins</td>
      <td>3</td>
      <td>55.38</td>
      <td>18.46</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Sit4Anthems</td>
      <td>Losses</td>
      <td>9</td>
      <td>178.14</td>
      <td>19.79</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Team 8</td>
      <td>Wins</td>
      <td>5</td>
      <td>77.28</td>
      <td>15.46</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Team 8</td>
      <td>Losses</td>
      <td>7</td>
      <td>192.90</td>
      <td>27.56</td>
    </tr>
    <tr>
      <th>14</th>
      <td>TeamGooseEggs</td>
      <td>Wins</td>
      <td>8</td>
      <td>315.64</td>
      <td>39.46</td>
    </tr>
    <tr>
      <th>15</th>
      <td>TeamGooseEggs</td>
      <td>Losses</td>
      <td>4</td>
      <td>122.64</td>
      <td>30.66</td>
    </tr>
    <tr>
      <th>16</th>
      <td>The Golden Yogis</td>
      <td>Wins</td>
      <td>3</td>
      <td>37.58</td>
      <td>12.53</td>
    </tr>
    <tr>
      <th>17</th>
      <td>The Golden Yogis</td>
      <td>Losses</td>
      <td>9</td>
      <td>247.60</td>
      <td>27.51</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Healthyplayersplz</td>
      <td>Wins</td>
      <td>5</td>
      <td>64.20</td>
      <td>12.84</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Healthyplayersplz</td>
      <td>Losses</td>
      <td>7</td>
      <td>167.26</td>
      <td>23.89</td>
    </tr>
  </tbody>
</table>
</div>



### Avg Differential by Wins and Losses


```python
matchup_wins_final.sort_values(["W/L", "AvgDiff"], ascending = False).reset_index(drop=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>W/L</th>
      <th>Count</th>
      <th>Diff</th>
      <th>AvgDiff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BigBradyBrand</td>
      <td>Wins</td>
      <td>5</td>
      <td>208.76</td>
      <td>41.75</td>
    </tr>
    <tr>
      <th>1</th>
      <td>TeamGooseEggs</td>
      <td>Wins</td>
      <td>8</td>
      <td>315.64</td>
      <td>39.46</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Sean McBae</td>
      <td>Wins</td>
      <td>8</td>
      <td>294.34</td>
      <td>36.79</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Butkicker&amp;Tygod</td>
      <td>Wins</td>
      <td>7</td>
      <td>176.88</td>
      <td>25.27</td>
    </tr>
    <tr>
      <th>4</th>
      <td>LordN’Savior Josh G</td>
      <td>Wins</td>
      <td>9</td>
      <td>173.36</td>
      <td>19.26</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Sit4Anthems</td>
      <td>Wins</td>
      <td>3</td>
      <td>55.38</td>
      <td>18.46</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Clippernation</td>
      <td>Wins</td>
      <td>7</td>
      <td>121.22</td>
      <td>17.32</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Team 8</td>
      <td>Wins</td>
      <td>5</td>
      <td>77.28</td>
      <td>15.46</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Healthyplayersplz</td>
      <td>Wins</td>
      <td>5</td>
      <td>64.20</td>
      <td>12.84</td>
    </tr>
    <tr>
      <th>9</th>
      <td>The Golden Yogis</td>
      <td>Wins</td>
      <td>3</td>
      <td>37.58</td>
      <td>12.53</td>
    </tr>
    <tr>
      <th>10</th>
      <td>LordN’Savior Josh G</td>
      <td>Losses</td>
      <td>3</td>
      <td>108.66</td>
      <td>36.22</td>
    </tr>
    <tr>
      <th>11</th>
      <td>TeamGooseEggs</td>
      <td>Losses</td>
      <td>4</td>
      <td>122.64</td>
      <td>30.66</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Sean McBae</td>
      <td>Losses</td>
      <td>4</td>
      <td>120.96</td>
      <td>30.24</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Butkicker&amp;Tygod</td>
      <td>Losses</td>
      <td>5</td>
      <td>139.02</td>
      <td>27.80</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Team 8</td>
      <td>Losses</td>
      <td>7</td>
      <td>192.90</td>
      <td>27.56</td>
    </tr>
    <tr>
      <th>15</th>
      <td>The Golden Yogis</td>
      <td>Losses</td>
      <td>9</td>
      <td>247.60</td>
      <td>27.51</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Clippernation</td>
      <td>Losses</td>
      <td>5</td>
      <td>134.68</td>
      <td>26.94</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Healthyplayersplz</td>
      <td>Losses</td>
      <td>7</td>
      <td>167.26</td>
      <td>23.89</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Sit4Anthems</td>
      <td>Losses</td>
      <td>9</td>
      <td>178.14</td>
      <td>19.79</td>
    </tr>
    <tr>
      <th>19</th>
      <td>BigBradyBrand</td>
      <td>Losses</td>
      <td>7</td>
      <td>112.78</td>
      <td>16.11</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Last 3 games W/L and Points
last_n = 3

last_three_scores = matchups_stacked[matchups_stacked["Week"] > weeks_elapsed - last_n].groupby(["Team"]) \
.agg({"Proj.Score" : "sum", "Score": "sum"}).reset_index() \

last_three_scores = last_three_scores.assign(Avg = last_three_scores["Score"] / last_n).round(2) \
.sort_values("Avg", ascending = False).reset_index(drop = True)


```


```python
last_three_matchups = matchups[matchups["Week"] > weeks_elapsed - last_n]
ltm1 = last_three_matchups[["TeamOne", "Winner"]]
ltm2 = last_three_matchups[["TeamTwo", "Winner"]]

ltm1 = ltm1.assign(Convert= [1 if x == ">" else 0 for x in list(ltm1["Winner"]) ])
ltm2 = ltm2.assign(Convert= [1 if x == "<" else 0 for x in list(ltm1["Winner"]) ])


```


```python
last_three_record_dict = {}

for k in range(ltm1.shape[0]):
    team1 = ltm1["TeamOne"].iloc[k]
    count1 = ltm1["Convert"].iloc[k]
    team2 = ltm2["TeamTwo"].iloc[k]
    count2 = ltm2["Convert"].iloc[k]  
    if team1 in last_three_record_dict:
        last_three_record_dict[team1] += count1
    else:
        last_three_record_dict[team1] = count1
        
    if team2 in last_three_record_dict:
        last_three_record_dict[team2] += count2
    else:
        last_three_record_dict[team2] = count2



keys2, values2 = last_three_record_dict.keys(), last_three_record_dict.values()


last_three_record = pd.DataFrame.from_items([('Team', list(keys2)), ('Wins', list(values2))])

last_three_record["Losses"] = 3 - last_three_record["Wins"]
last_three_record["W\L"] = last_three_record["Wins"].astype("str") + "-" + last_three_record["Losses"].astype("str")

```

## Scores for Last Three Weeks


```python
last_three_scores.merge(last_three_record[["Team", "W\L"]], on="Team")
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>Proj.Score</th>
      <th>Score</th>
      <th>Avg</th>
      <th>W\L</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sean McBae</td>
      <td>381.76</td>
      <td>467.48</td>
      <td>155.83</td>
      <td>3-0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Butkicker&amp;Tygod</td>
      <td>321.97</td>
      <td>343.12</td>
      <td>114.37</td>
      <td>2-1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>LordN’Savior Josh G</td>
      <td>326.50</td>
      <td>337.84</td>
      <td>112.61</td>
      <td>2-1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Healthyplayersplz</td>
      <td>315.70</td>
      <td>330.64</td>
      <td>110.21</td>
      <td>3-0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Team 8</td>
      <td>316.10</td>
      <td>328.80</td>
      <td>109.60</td>
      <td>1-2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>BigBradyBrand</td>
      <td>335.63</td>
      <td>322.64</td>
      <td>107.55</td>
      <td>0-3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>TeamGooseEggs</td>
      <td>382.59</td>
      <td>318.56</td>
      <td>106.19</td>
      <td>2-1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>The Golden Yogis</td>
      <td>310.91</td>
      <td>316.58</td>
      <td>105.53</td>
      <td>2-1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Clippernation</td>
      <td>306.72</td>
      <td>272.22</td>
      <td>90.74</td>
      <td>0-3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Sit4Anthems</td>
      <td>309.66</td>
      <td>245.16</td>
      <td>81.72</td>
      <td>0-3</td>
    </tr>
  </tbody>
</table>
</div>



## Top 10 Scores in the Season


```python
# top 10 scores in season
matchups_stacked[["Team", "Score", "Proj.Score", "Week"]].sort_values("Score", ascending = False).head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>Score</th>
      <th>Proj.Score</th>
      <th>Week</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>110</th>
      <td>Sean McBae</td>
      <td>182.44</td>
      <td>134.84</td>
      <td>12</td>
    </tr>
    <tr>
      <th>100</th>
      <td>Sean McBae</td>
      <td>159.64</td>
      <td>126.12</td>
      <td>11</td>
    </tr>
    <tr>
      <th>40</th>
      <td>TeamGooseEggs</td>
      <td>157.16</td>
      <td>118.86</td>
      <td>5</td>
    </tr>
    <tr>
      <th>30</th>
      <td>BigBradyBrand</td>
      <td>151.28</td>
      <td>122.59</td>
      <td>4</td>
    </tr>
    <tr>
      <th>50</th>
      <td>LordN’Savior Josh G</td>
      <td>151.26</td>
      <td>115.44</td>
      <td>6</td>
    </tr>
    <tr>
      <th>51</th>
      <td>Healthyplayersplz</td>
      <td>146.98</td>
      <td>114.73</td>
      <td>6</td>
    </tr>
    <tr>
      <th>80</th>
      <td>BigBradyBrand</td>
      <td>146.24</td>
      <td>111.80</td>
      <td>9</td>
    </tr>
    <tr>
      <th>81</th>
      <td>Sean McBae</td>
      <td>139.80</td>
      <td>105.48</td>
      <td>9</td>
    </tr>
    <tr>
      <th>101</th>
      <td>Team 8</td>
      <td>136.84</td>
      <td>104.01</td>
      <td>11</td>
    </tr>
    <tr>
      <th>52</th>
      <td>TeamGooseEggs</td>
      <td>136.44</td>
      <td>125.67</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



## Bottom 10 Scores in the Season


```python
# bottom 10 scores in season
matchups_stacked[["Team", "Score", "Proj.Score", "Week"]].sort_values("Score").head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>Score</th>
      <th>Proj.Score</th>
      <th>Week</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <td>Butkicker&amp;Tygod</td>
      <td>62.86</td>
      <td>112.87</td>
      <td>4</td>
    </tr>
    <tr>
      <th>89</th>
      <td>Sit4Anthems</td>
      <td>63.80</td>
      <td>89.65</td>
      <td>9</td>
    </tr>
    <tr>
      <th>59</th>
      <td>BigBradyBrand</td>
      <td>64.18</td>
      <td>108.25</td>
      <td>6</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Sit4Anthems</td>
      <td>65.40</td>
      <td>109.84</td>
      <td>2</td>
    </tr>
    <tr>
      <th>88</th>
      <td>The Golden Yogis</td>
      <td>68.32</td>
      <td>97.26</td>
      <td>9</td>
    </tr>
    <tr>
      <th>119</th>
      <td>Sit4Anthems</td>
      <td>68.56</td>
      <td>107.78</td>
      <td>12</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Butkicker&amp;Tygod</td>
      <td>69.84</td>
      <td>120.96</td>
      <td>1</td>
    </tr>
    <tr>
      <th>49</th>
      <td>Team 8</td>
      <td>71.40</td>
      <td>108.28</td>
      <td>5</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Butkicker&amp;Tygod</td>
      <td>73.18</td>
      <td>114.74</td>
      <td>3</td>
    </tr>
    <tr>
      <th>58</th>
      <td>The Golden Yogis</td>
      <td>74.46</td>
      <td>102.25</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



## Top Three Scores in Season, Per Team


```python
#top three scores in season per team
if weeks_elapsed > 2:
    k = 3
else:
    k = weeks_elapsed
matchups_stacked[["Team", "Score", "Proj.Score","Week"]].sort_values(["Team", "Score"], ascending = False) \
.groupby("Team").head(k).reset_index(drop=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>Score</th>
      <th>Proj.Score</th>
      <th>Week</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>The Golden Yogis</td>
      <td>116.60</td>
      <td>126.62</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>The Golden Yogis</td>
      <td>115.46</td>
      <td>110.78</td>
      <td>12</td>
    </tr>
    <tr>
      <th>2</th>
      <td>The Golden Yogis</td>
      <td>109.52</td>
      <td>120.19</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>TeamGooseEggs</td>
      <td>157.16</td>
      <td>118.86</td>
      <td>5</td>
    </tr>
    <tr>
      <th>4</th>
      <td>TeamGooseEggs</td>
      <td>136.44</td>
      <td>125.67</td>
      <td>6</td>
    </tr>
    <tr>
      <th>5</th>
      <td>TeamGooseEggs</td>
      <td>132.82</td>
      <td>124.77</td>
      <td>4</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Team 8</td>
      <td>136.84</td>
      <td>104.01</td>
      <td>11</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Team 8</td>
      <td>128.32</td>
      <td>121.17</td>
      <td>3</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Team 8</td>
      <td>121.84</td>
      <td>122.70</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Sit4Anthems</td>
      <td>125.80</td>
      <td>98.08</td>
      <td>3</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Sit4Anthems</td>
      <td>114.94</td>
      <td>118.75</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Sit4Anthems</td>
      <td>112.82</td>
      <td>104.81</td>
      <td>8</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Sean McBae</td>
      <td>182.44</td>
      <td>134.84</td>
      <td>12</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Sean McBae</td>
      <td>159.64</td>
      <td>126.12</td>
      <td>11</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Sean McBae</td>
      <td>139.80</td>
      <td>105.48</td>
      <td>9</td>
    </tr>
    <tr>
      <th>15</th>
      <td>LordN’Savior Josh G</td>
      <td>151.26</td>
      <td>115.44</td>
      <td>6</td>
    </tr>
    <tr>
      <th>16</th>
      <td>LordN’Savior Josh G</td>
      <td>135.50</td>
      <td>107.83</td>
      <td>8</td>
    </tr>
    <tr>
      <th>17</th>
      <td>LordN’Savior Josh G</td>
      <td>128.18</td>
      <td>122.92</td>
      <td>2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Healthyplayersplz</td>
      <td>146.98</td>
      <td>114.73</td>
      <td>6</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Healthyplayersplz</td>
      <td>121.88</td>
      <td>105.58</td>
      <td>5</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Healthyplayersplz</td>
      <td>117.74</td>
      <td>101.65</td>
      <td>10</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Clippernation</td>
      <td>125.82</td>
      <td>112.58</td>
      <td>2</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Clippernation</td>
      <td>124.38</td>
      <td>118.98</td>
      <td>4</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Clippernation</td>
      <td>122.34</td>
      <td>117.56</td>
      <td>5</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Butkicker&amp;Tygod</td>
      <td>132.32</td>
      <td>112.73</td>
      <td>12</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Butkicker&amp;Tygod</td>
      <td>118.60</td>
      <td>102.36</td>
      <td>9</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Butkicker&amp;Tygod</td>
      <td>110.90</td>
      <td>104.23</td>
      <td>8</td>
    </tr>
    <tr>
      <th>27</th>
      <td>BigBradyBrand</td>
      <td>151.28</td>
      <td>122.59</td>
      <td>4</td>
    </tr>
    <tr>
      <th>28</th>
      <td>BigBradyBrand</td>
      <td>146.24</td>
      <td>111.80</td>
      <td>9</td>
    </tr>
    <tr>
      <th>29</th>
      <td>BigBradyBrand</td>
      <td>135.62</td>
      <td>122.21</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>



## Bottom Three Scores in Season, Per Team


```python
#bottom three scores in season per team
if weeks_elapsed > 2:
    k = 3
else:
    k = weeks_elapsed
matchups_stacked[["Team", "Score", "Proj.Score","Week"]].sort_values(["Team", "Score"]) \
.groupby("Team").head(k).reset_index(drop=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team</th>
      <th>Score</th>
      <th>Proj.Score</th>
      <th>Week</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BigBradyBrand</td>
      <td>64.18</td>
      <td>108.25</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BigBradyBrand</td>
      <td>87.88</td>
      <td>118.63</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BigBradyBrand</td>
      <td>91.58</td>
      <td>118.03</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Butkicker&amp;Tygod</td>
      <td>62.86</td>
      <td>112.87</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Butkicker&amp;Tygod</td>
      <td>69.84</td>
      <td>120.96</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Butkicker&amp;Tygod</td>
      <td>73.18</td>
      <td>114.74</td>
      <td>3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Clippernation</td>
      <td>75.82</td>
      <td>104.92</td>
      <td>3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Clippernation</td>
      <td>76.16</td>
      <td>107.82</td>
      <td>9</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Clippernation</td>
      <td>87.44</td>
      <td>96.16</td>
      <td>10</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Healthyplayersplz</td>
      <td>80.62</td>
      <td>122.35</td>
      <td>4</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Healthyplayersplz</td>
      <td>83.84</td>
      <td>108.38</td>
      <td>8</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Healthyplayersplz</td>
      <td>90.42</td>
      <td>117.50</td>
      <td>7</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LordN’Savior Josh G</td>
      <td>81.12</td>
      <td>100.64</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>LordN’Savior Josh G</td>
      <td>83.70</td>
      <td>129.99</td>
      <td>4</td>
    </tr>
    <tr>
      <th>14</th>
      <td>LordN’Savior Josh G</td>
      <td>93.62</td>
      <td>110.73</td>
      <td>7</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Sean McBae</td>
      <td>86.62</td>
      <td>116.79</td>
      <td>3</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Sean McBae</td>
      <td>96.26</td>
      <td>112.95</td>
      <td>5</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Sean McBae</td>
      <td>100.24</td>
      <td>104.85</td>
      <td>8</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Sit4Anthems</td>
      <td>63.80</td>
      <td>89.65</td>
      <td>9</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Sit4Anthems</td>
      <td>65.40</td>
      <td>109.84</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Sit4Anthems</td>
      <td>68.56</td>
      <td>107.78</td>
      <td>12</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Team 8</td>
      <td>71.40</td>
      <td>108.28</td>
      <td>5</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Team 8</td>
      <td>80.08</td>
      <td>99.29</td>
      <td>9</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Team 8</td>
      <td>81.52</td>
      <td>123.09</td>
      <td>6</td>
    </tr>
    <tr>
      <th>24</th>
      <td>TeamGooseEggs</td>
      <td>78.26</td>
      <td>109.88</td>
      <td>8</td>
    </tr>
    <tr>
      <th>25</th>
      <td>TeamGooseEggs</td>
      <td>86.24</td>
      <td>137.42</td>
      <td>12</td>
    </tr>
    <tr>
      <th>26</th>
      <td>TeamGooseEggs</td>
      <td>90.26</td>
      <td>125.30</td>
      <td>2</td>
    </tr>
    <tr>
      <th>27</th>
      <td>The Golden Yogis</td>
      <td>68.32</td>
      <td>97.26</td>
      <td>9</td>
    </tr>
    <tr>
      <th>28</th>
      <td>The Golden Yogis</td>
      <td>74.46</td>
      <td>102.25</td>
      <td>6</td>
    </tr>
    <tr>
      <th>29</th>
      <td>The Golden Yogis</td>
      <td>76.66</td>
      <td>117.36</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>


