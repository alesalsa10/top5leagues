import requests,json, csv
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import pearsonr

        
top5 = []
def api_access():
    codes = ['524', '775', '525','891','754']   #top 5 league codes, current season
    for code in codes:
        url = f"https://api-football-v1.p.rapidapi.com/v2/leagueTable/{code}"

        headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': ""
        }
        response = requests.request("GET", url, headers=headers)
        file = response.json()
        info = file['api']['standings'][0][0:] 
        top5.append(info)

my_list = []

def get_info():
    for x in top5:
        for all in x:
            name = all['teamName']
            points = all['points']
            goal_diff = all['goalsDiff']
            goals_for = all['all']['goalsFor']
            goals_against = all['all']['goalsAgainst']
            rank = all['rank']
            data ={'name': name,'rank': rank, 'points': points, 'goal_diff':goal_diff, 'goals_for':goals_for, 'goals_against': goals_against}
            my_list.append(data)
    return my_list


def save_to_csv():
    with open('stats.csv', 'w', newline='') as stats:
       writer = csv.DictWriter(stats, my_list[0].keys())
       writer.writeheader()
       for i in my_list:
           writer.writerow(i)


def save_graphs():
    columns = [3, 4, 5]
    for item in columns:
        x, y = np.loadtxt('stats.csv', delimiter=',', unpack=True, usecols=(1,item), skiprows = 1 )
        plt.scatter(x, y, label='Top 5 leagues') 
        
        if item == 3:
            y_axis = 'Goal Difference'
        elif item == 4:
            y_axis = 'Goals For'
        else:
            y_axis = 'Goals Against'
        
        plt.xlabel('Rank')
        plt.ylabel(y_axis)
        
        plt.savefig(f'{y_axis}.png', bbox_inches = 'tight')
            
def correlation():
    columns = [3, 4, 5]
    for item in columns:
        x, y = np.loadtxt('stats.csv', delimiter=',', unpack=True, usecols=(1,item), skiprows = 1 )

        if item == 3:
            value = 'goal difference'
        elif item == 4:
            value = 'goals for'
        else:
            value = 'goals against'

        r,p = pearsonr(x,y) # r is the correlation, p is the p-value
        print(f"Comparison between  team rank and {value} returns Pearson's correlation coefficient of {round(r,2)}. ")

api_access()
get_info()
save_to_csv()
save_graphs()
correlation()







