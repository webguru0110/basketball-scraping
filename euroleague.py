from bs4 import BeautifulSoup
import requests
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_boxscore(url: str):
    boxscore = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        tables = soup.find_all('div', class_=lambda value: value and value.startswith('game-box-scores-table-grouped_tabContent'))
        team_home = True
        first_team_count = 0
        for table in tables:
            divs = table.find_all('div', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-tab_tableGroupedRowsContainer'))

            sub_divs = divs[0].find_all('div', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-tab_leftColumnTitle'))
            for sub_div in sub_divs:
                try:
                    num_tag = sub_div.find('span', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-tab_dorsal'))
                    num = '' if num_tag == None else  num_tag.get_text().strip()
                    first_name_tag = sub_div.find('span', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-tab_firstName'))
                    first_name = '' if first_name_tag == None else  first_name_tag.get_text().strip()
                    last_name_tag = sub_div.find('b', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-tab_lastName'))
                    last_name = '' if last_name_tag == None else  last_name_tag.get_text().strip()
                    short_name_tag = sub_div.find('div', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-tab_playerShortName'))
                    short_name = '' if short_name_tag == None else  short_name_tag.get_text().strip()
                    item = {
                        'num': num,
                        'first_name': first_name,
                        'last_name': last_name,
                        'short_name': short_name,
                        'team_home': team_home,
                        'data': []
                    }
                    # item = [num, first_name, last_name, short_name, team_home]
                    boxscore.append(item)
                except Exception as ee:
                    print('No player data.')

            sub_divs = divs[1].find_all('div', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-column_tableGroupedColumnStatGroupContainer'))
            r_idx = 0
            for sub_div in sub_divs:
                ss_divs = sub_div.find_all('div', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-column_tableGroupedRowStatGroupContainer') and 'heading' not in value)
                r_idx = 0
                for ss_div in ss_divs:
                    sss_divs = ss_div.find_all('div', class_=lambda value: value and value.startswith('game-box-scores-table-grouped-column_tableStatCell'))
                    if sss_divs == None or len(sss_divs) == 0:
                        continue
                    for sss_div in sss_divs:
                        boxscore[r_idx + first_team_count]['data'].append(sss_div.get_text().strip())
                    r_idx += 1
            team_home = False
            if first_team_count < r_idx:
                first_team_count = r_idx
    except Exception as ee:
        print(ee)
        print("Boxscore retrieving failed.")
    print("Boxscore retrieving completed!")
    return boxscore

def get_graphic_stats(url: str):
    graphic_stats = {}
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        tags = soup.find_all('li', class_=lambda value: value and value.startswith('game-stats-row_statsRow'))
        for tag in tags:
            values = tag.find_all('div', class_=lambda value: value and value.startswith('game-stats-row_teamValue'))

            title_short = tag.find('div', class_=lambda value: value and value.startswith('game-stats-row_statTitleShort')).get_text().strip()
            title = tag.find('div', class_=lambda value: value and value.startswith('game-stats-row_statTitle_')).get_text().strip()

            if title_short.find('%') == -1:
                graphic_stats[f'{title_short}_home'] = int(values[0].get_text().strip())
                graphic_stats[f'{title_short}_away'] = int(values[1].get_text().strip())
            else:
                graphic_stats[f'{title_short}_home'] = float(values[0].get_text().strip())
                graphic_stats[f'{title_short}_away'] = float(values[1].get_text().strip())

    except Exception as ee:
        print(ee)
        print("Graphic Stats retrieving failed.")
    print("Graphic Stats retrieving completed!")
    return graphic_stats

def get_shooting(url: str):
    shooting = []
    try:
        parts = url.strip('/').split('/')
        seasoncode = parts[-3]
        gamecode = parts[-2]

        home_url = f"https://live.euroleague.net/api/Players?gamecode={gamecode}&seasoncode={seasoncode}&disp=&equipo=HAM&temp={seasoncode}"
        away_url = f"https://live.euroleague.net/api/Players?gamecode={gamecode}&seasoncode={seasoncode}&disp=&equipo=HAM&temp={seasoncode}"
        response = requests.get(home_url)
        json_details = json.loads(response.content)
        if response.status_code == 200 and json_details != None and len(json_details) > 0:
            team_home = True
            for json_obj in json_details:
                item = {
                    'game_code': gamecode,
                    'team_id': team_home,
                    'c': json_obj['c'],
                    'ac': json_obj['ac'],
                    'full_name': json_obj['na'],
                    'nu': json_obj['nu'],
                    'st': json_obj['st'],
                    'sl': json_obj['sl'],
                    'nn': json_obj['nn'],
                    'p': json_obj['p'],
                    'image_url': json_obj['im'],
                }
                shooting.append(item)
        response = requests.get(away_url)
        json_details = json.loads(response.content)
        if response.status_code == 200 and json_details != None and len(json_details) > 0:
            team_home = False
            for json_obj in json_details:
                item = {
                    'game_code': gamecode,
                    'team_id': team_home,
                    'c': json_obj['c'],
                    'ac': json_obj['ac'],
                    'full_name': json_obj['na'],
                    'nu': json_obj['nu'],
                    'st': json_obj['st'],
                    'sl': json_obj['sl'],
                    'nn': json_obj['nn'],
                    'p': json_obj['p'],
                    'image_url': json_obj['im'],
                }
                shooting.append(item)

    except Exception as ee:
        print(ee)
        print("Shooting retrieving failed.")
    print("Shooting retrieving completed!")
    return shooting

def get_resultgraph(url: str):
    resultgraph = []
    return resultgraph

def get_playbyplay(url: str):
    playbyplay = []
    try:
        driver = webdriver.Chrome()  # You may need to adjust the path to your Chrome driver
        driver.get(url)

        play_buttons = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href$='#play-by-play']"))
        )
        play_buttons.click()
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class^='play-by-play-buttons-list_listItem']"))
        )
        for i, button in enumerate(buttons):
            if i == 4:
                break
            # Wait until the button is clickable
            if i==0:
                cookie_buttons = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
                )
                cookie_buttons.click()
            clickable_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable(button)
            )
            clickable_button.click()
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "lxml")
            lists = soup.find_all('div', class_=lambda value: value and value.startswith('play-by-play-content-list-item_block'))
            for list in lists:
                child_divs = list.find_all('div', recursive=False)
                if len(child_divs) == 3:
                    # Assign each child div to a variable
                    team1 = child_divs[0].text.strip()
                    time_remaining = child_divs[1].text.strip()
                    team2 = child_divs[2].text.strip()
                item = {
                        'quarter': i+1,
                        'team1_event': team1,
                        'time_remaining': time_remaining,
                        'team2_event':team2
                }
                playbyplay.append(item)

    except Exception as ee:
        print(ee)
        print("PlayByPlay retrieving failed.")
    print("PlayByPlay retrieving completed!")
    return playbyplay

def auto_euroleague(url: str):
    url_boxscore = url + '#boxscore/'
    box_score = get_boxscore(url_boxscore)

    url_graphstats = url + '#graphic-stats/'
    graphic_stats = get_graphic_stats(url_graphstats)

    url_shooting = url + '#shooting-chart/'
    shooting = get_shooting(url_shooting)
    url_resultgraph = url + ''
    result_graph = get_resultgraph(url_resultgraph)
    url_playbyplay = url + '#play-by-play/'
    playbyplay = get_playbyplay(url_playbyplay)


    data = {
        'box_score': box_score,
        'graphic_stats': graphic_stats,
        'shooting_chart': shooting,
        'result_graph': result_graph,
        'playbyplay': playbyplay
    }

    with open('data_results_euroleague.json', 'w') as f:
        json.dump(data, f, indent=4)
        print("Result json has been saved!")


if __name__ == '__main__':
    print('Starting to retrieve from euroleaguebasketball.net')
    url = 'https://www.euroleaguebasketball.net/en/eurocup/game-center/2024-25/veolia-towers-hamburg-u-bt-cluj-napoca/U2024/40/'
    auto_euroleague(url)
