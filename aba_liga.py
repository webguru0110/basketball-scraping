import json
import os
import shutil
from bs4 import BeautifulSoup
import requests

def get_boxscore(url:str):
    boxscore = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        tables = soup.find_all("table", class_='match_boxscore_team_table')
        if tables != None:
            # first(team_home = True) is home team, second is away team
            team_home = True
            for table in tables:
                rows = table.find("tbody").find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    item = {
                        'player_id': '',
                        'team_id': '',
                        'minutes_played': '',
                        'points': '',
                        'overall_percent': '',
                        'fg2_made': '',
                        'fg2_attepmted': '',
                        'fg2_percent': '',
                        'fg3_made': '',
                        'fg3_attempted': '',
                        'fg3_percent': '',
                        'ft_made': '',
                        'ft_attempted': '',
                        'ft_percent': '',
                        'rebs_d': '',
                        'rebs_o': '',
                        'rebs_t': '',
                        'assists': '',
                        'steals': '',
                        'turnovers': '',
                        'blocks_fv': '',
                        'blocks_ag': '',
                        'foul_cm': '',
                        'foul_rv': '',
                        'point_from_paint': '',
                        'point_from_2ndch': '',
                        'point_from_fstbr': '',
                        'plus_minus': '',
                        'total_val': '',
                    }
                    try:
                        item['player_id'] = cols[1].get_text().strip()
                        item['team_id'] = team_home
                        item['minutes_played'] = cols[2].get_text().strip()
                        item['points'] = cols[3].get_text().strip()
                        item['overall_percent'] = cols[4].get_text().strip()
                        item['fg2_made'] = cols[5].get_text().strip()
                        item['fg2_attepmted'] = cols[6].get_text().strip()
                        item['fg2_percent'] = cols[7].get_text().strip()
                        item['fg3_made'] = cols[8].get_text().strip()
                        item['fg3_attempted'] = cols[9].get_text().strip()
                        item['fg3_percent'] = cols[10].get_text().strip()
                        item['ft_made'] = cols[11].get_text().strip()
                        item['ft_attempted'] = cols[12].get_text().strip()
                        item['ft_percent'] = cols[13].get_text().strip()
                        item['rebs_d'] = cols[14].get_text().strip()
                        item['rebs_o'] = cols[15].get_text().strip()
                        item['rebs_t'] = cols[16].get_text().strip()
                        item['assists'] = cols[17].get_text().strip()
                        item['steals'] = cols[18].get_text().strip()
                        item['turnovers'] = cols[19].get_text().strip()
                        item['blocks_fv'] = cols[20].get_text().strip()
                        item['blocks_ag'] = cols[21].get_text().strip()
                        item['foul_cm'] = cols[22].get_text().strip()
                        item['foul_rv'] = cols[23].get_text().strip()
                        item['point_from_paint'] = cols[24].get_text().strip()
                        item['point_from_2ndch'] = cols[25].get_text().strip()
                        item['point_from_fstbr'] = cols[26].get_text().strip()
                        item['plus_minus'] = cols[27].get_text().strip()
                        item['total_val'] = cols[28].get_text().strip()
                    except Exception as ee:
                        print(ee)
                    boxscore.append(item)
                team_home = False
    except Exception as ee:
        print(ee)
        print("Boxscore retrieving failed.")
    print("Boxscore retrieving completed!")
    return boxscore

def handle_graphic_stats_item(value1, value2):
    ret = ''
    if value2 == '-' or value2 == '':
        ret = value1
    else:
        ret = f'{value1}/{value2}'
    ret = ret.replace('-', '')
    return ret

def calc_fraction_str(fraction):
    # fraction = '10/50'
    numerator, denominator = map(int, fraction.split('/'))
    result = numerator / denominator
    return result

def get_graphic_stats(url: str):
    graphic_stats = {
        'game_id': 0,
        'home_team_id': 0,
        'away_team_id': 0,
        'starter_points_home': 0,
        'starter_points_away': 0,
        'bench_points_home': 0,
        'bench_points_away': 0,
        'turnovers_home': 0,
        'turnovers_away': 0,
        'rebounds_home': 0,
        'rebounds_away': 0,
        'assists_home': 0,
        'assists_away': 0,
        'steals_home': 0,
        'steals_away': 0,
        'blocks_home': 0,
        'blocks_away': 0,
        'fg_percentage_home': 0,
        'fg_percentage_away': 0,
        'three_pt_percentage_home': 0,
        'three_pt_percentage_away': 0,
        'ft_percentage_home': 0,
        'ft_percentage_away': 0,
    }
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        gs_home1 = soup.find('p', {'id': 'graphic_stats_home1'})
        gs_home1_str = gs_home1.get_text().strip()
        gs_home1_array = gs_home1_str.split(',')

        gs_home2 = soup.find('p', {'id': 'graphic_stats_home2'})
        gs_home2_str = gs_home2.get_text().strip()
        gs_home2_array = gs_home2_str.split(',')

        gs_away1 = soup.find('p', {'id': 'graphic_stats_away1'})
        gs_away1_str = gs_away1.get_text().strip()
        gs_away1_array = gs_away1_str.split(',')
        gs_away2 = soup.find('p', {'id': 'graphic_stats_away2'})
        gs_away2_str = gs_away2.get_text().strip()
        gs_away2_array = []
        gs_away2_array_temp = gs_away2_str.split(',')
        for gs_away2_item in gs_away2_array_temp:
            if gs_away2_item.strip() != '' and gs_away2_item.strip() != '-':
                gs_away2_array.append(gs_away2_item.strip())

        if len(gs_home1_array) > 0 and len(gs_home2_array) > 0:
            graphic_stats['starter_points_home'] = int(handle_graphic_stats_item(gs_home1_array[0], gs_home2_array[0]))
        if len(gs_away1_array) > 0:
            graphic_stats['starter_points_away'] = int(handle_graphic_stats_item(gs_away1_array[0], ''))

        if len(gs_home1_array) > 1 and len(gs_home2_array) > 1:
            graphic_stats['bench_points_home'] = int(handle_graphic_stats_item(gs_home1_array[1], gs_home2_array[1]))
        if len(gs_away1_array) > 1:
            graphic_stats['bench_points_away'] = int(handle_graphic_stats_item(gs_away1_array[1], ''))

        if len(gs_home1_array) > 9 and len(gs_home2_array) > 9:
            graphic_stats['turnovers_home'] = int(handle_graphic_stats_item(gs_home1_array[9], gs_home2_array[9]))
        if len(gs_away1_array) > 9:
            graphic_stats['turnovers_away'] = int(handle_graphic_stats_item(gs_away1_array[9], ''))

        # Rebounds O, Rebounds D. Handled the first item.
        if len(gs_home1_array) > 5 and len(gs_home2_array) > 5:
            graphic_stats['rebounds_home'] = int(handle_graphic_stats_item(gs_home1_array[5], gs_home2_array[5]))
        if len(gs_away1_array) > 5:
            graphic_stats['rebounds_away'] = int(handle_graphic_stats_item(gs_away1_array[5], ''))

        if len(gs_home1_array) > 7 and len(gs_home2_array) > 7:
            graphic_stats['assists_home'] = int(handle_graphic_stats_item(gs_home1_array[7], gs_home2_array[7]))
        if len(gs_away1_array) > 7:
            graphic_stats['assists_away'] = int(handle_graphic_stats_item(gs_away1_array[7], ''))

        if len(gs_home1_array) > 8 and len(gs_home2_array) > 8:
            graphic_stats['steals_home'] = int(handle_graphic_stats_item(gs_home1_array[8], gs_home2_array[8]))
        if len(gs_away1_array) > 8:
            graphic_stats['steals_away'] = int(handle_graphic_stats_item(gs_away1_array[8], ''))

        # Blocks made, Blocks receiveed. Handled the first item.
        if len(gs_home1_array) > 10 and len(gs_home2_array) > 10:
            graphic_stats['blocks_home'] = int(handle_graphic_stats_item(gs_home1_array[10], gs_home2_array[10]))
        if len(gs_away1_array) > 10:
            graphic_stats['blocks_away'] = int(handle_graphic_stats_item(gs_away1_array[10], ''))

        if len(gs_home1_array) > 3 and len(gs_home2_array) > 3:
            graphic_stats['fg_percentage_home'] = calc_fraction_str(handle_graphic_stats_item(gs_home1_array[3], gs_home2_array[3]))
        if len(gs_away1_array) > 3 and len(gs_away2_array) > 1:
            graphic_stats['fg_percentage_away'] = calc_fraction_str(handle_graphic_stats_item(gs_away1_array[3], gs_away2_array[1]))

        # last part is to get percentage from fraction. Like this, we can get all values according to index.
    except Exception as ee:
        print(ee)
        print("Graphic Stats retrieving failed.")
    print("Graphic Stats retrieving completed!")
    return graphic_stats

def get_shooting_chart(url: str):
    ret = []
    try:
        response = requests.get(url)
        json_details = json.loads(response.content)
        if response.status_code == 200 and json_details != None and len(json_details) > 0:
            for json_obj in json_details:
                # print(f'ekipa {json_obj['ekipa']}, koordinata_x {json_obj['koordinata_x']}, koordinata_y {json_obj['koordinata_y']}')
                # print(f'koordinata_uspeh {json_obj['koordinata_uspeh']}, player_id {json_obj['player_id']}, player_name {json_obj['player_name']}')
                item = {
                    'game_id': 0,
                    'team_id': json_obj['ekipa'],
                    'player_id': json_obj['player_id'],
                    'player_name': json_obj['player_name'],
                    'x_coordinate': json_obj['koordinata_x'],
                    'y_coordinate': json_obj['koordinata_y'],
                    'coordingate_success': json_obj['koordinata_uspeh'],
                }
                ret.append(item)
    except Exception as ee:
        print(ee)
        print('Shooting Chart retrieving failed.')
    print("Shooting Chart retrieving completed!")
    return ret

def get_resultgraph(url: str):
    ret = []
    try:
        response = requests.get(url)
        json_details = json.loads(response.content)
        if response.status_code == 200 and json_details != None and len(json_details) > 0:
            for json_obj in json_details:
                # print(f'minuta {json_obj['minuta']}, difference {int(json_obj['domaci_rez']) - int(json_obj['tuji_rez'])}')
                item = {
                    'game_id': 0,
                    'home_team_id': 0,
                    'away_team_id': 0,
                    'minutes': json_obj['minuta'],
                    'home_team_points': json_obj['domaci_rez'],
                    'away_team_points': json_obj['tuji_rez']
                }
                ret.append(item)
    except Exception as ee:
        print(ee)
        print('Result Graph retrieving failed.')
    print("Result Graph retrieving completed!")
    return ret

def get_palybyplay(url: str):
    palybyplay = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # table = soup.find("table", class_='match_table_play_by_play')
        tables = soup.find_all('table', {'id': 'playbyplay-res'})
        if tables != None and len(tables) > 0:
            quarter = 0
            while quarter < 4:
                if len(tables) <= quarter:
                    break
                table = tables[quarter]
                rows = table.find("tbody").find_all('tr')
                for i, row in enumerate(rows):
                    if i == 0:
                        continue
                    cols = row.find_all('td', recursive=False)
                    item = {
                        'game_id': 0,
                        'quarter': quarter+1,
                        'event': '',
                        'time_remaining': '',
                        'event_type': '',
                        'description': '',
                        'player_name': '',
                        'player_link': '',
                        'team_id': 0,
                        # 'related_player_id': 0          # ???
                    }
                    try:
                        item['time_remaining'] = cols[0].text.strip()
                        item['event'] = cols[2].text.strip()
                        temp = cols[0].get_text().strip() + cols[2].get_text().strip()
                        detail = temp.split('.')[-1].strip()
                        if detail.find('(') > -1 and detail.find(')') > -1:
                            item['event_type'] = detail[detail.find('(') + 1: detail.find(')') - detail.find('(') - 1].strip()
                            detail = detail.replace(item['event_type'], '')
                            detail = detail.replace('(', '').strip()
                            detail = detail.replace(')', '').strip()
                        item['description'] = detail

                        player_a_tag = row.find('a')
                        if player_a_tag != None:
                            player_name = player_a_tag.get_text().strip()
                            item['player_name'] = player_name
                            player_link = player_a_tag.attrs['href']        # .get('href')
                            item['player_link'] = player_link
                    except Exception as ee:
                        print(ee)
                    palybyplay.append(item)
                quarter+=1
                team_home = False
    except Exception as ee:
        print(ee)
        print("PlayByPlay retrieving failed.")
    print("PlayByPlay retrieving completed!")
    return palybyplay

def auto_aba_liga(url: str):
    id = ''
    sez = ''
    lea = ''
    try :
        temp = url[url.find('match/') + 6:]
        temp = temp[:temp.find('/Overview')]
        id = temp.split('/')[0]
        sez = temp.split('/')[1]
        lea = temp.split('/')[2]
        if id == '' or sez == '' or lea == '':
            print(f'unvalid: {url}')
            return []
    except Exception as ee:
        print(f'unvalid: {url}')
        return []

    url_boxscore = url.replace('Overview', 'Boxscore')
    box_score = get_boxscore(url_boxscore)

    url_graphstats = url.replace('Overview', 'GraphicStats')
    graphic_stats = get_graphic_stats(url_graphstats)

    url_shooting = f'https://www.aba-liga.com/live-match/rezultati-1718/create_shooting_chart.php?id={id}&sez={sez}&lea={lea}'
    shooting_chart = get_shooting_chart(url_shooting)

    # url_resultgraph = url.replace('Overview', 'ResultGraph')
    url_resultgraph = f'https://www.aba-liga.com/live-match/rezultati-1718/create_scoredifference.php?id={id}&sez={sez}&lea={lea}'
    result_graph = get_resultgraph(url_resultgraph)

    url_playbyplay = url.replace('Overview', 'PlayByPlay')
    playbyplay = get_palybyplay(url_playbyplay)

    data = {
    'box_score': box_score,
    'graphic_stats': graphic_stats,
    'shooting_chart': shooting_chart,
    'result_graph': result_graph,
    'playbyplay': playbyplay
    }

    with open('data_results_liga.json', 'w') as f:
        json.dump(data, f, indent=4)
        print("Result json has been saved!")

if __name__ == '__main__':
    print('Starting to retrieve from aba-liga.com')
    url = 'https://www.aba-liga.com/match/27/24/1/Overview/q1/1/home/cedevita-olimpija-split/'
    auto_aba_liga(url)
