import csv
import time

import requests
from bs4 import BeautifulSoup
from pyfiglet import Figlet

music_l = []
for list in BeautifulSoup(requests.get("https://ongeki-score.net/music").text, 'html.parser').find("tbody", class_="list").find_all("tr"):
    # print(list)
    music_l.append([list.find_all("td")[0].find("span").text, list.find_all("td")[
                   1].text, list.find_all("td")[2].text, list.find_all("td")[3].text])
with open("楽曲リスト.csv", "w", encoding="UTF-8", newline="") as f:
    w = csv.writer(f)
    w.writerows(music_l)
    f.close()

ongeki = Figlet(font='big')
msg = ongeki.renderText('-O.N.G.E.K.I- Rating Math Tool')
print(msg)
print('By Nana_Cat0912')

time.sleep(1)

print("------------------------------注意事項-------------------------------")
print("このプログラムはオンゲキプレミアムコースに加入していないと動きません。")
print("複数枚のAimeを登録している場合は正常動作をしない可能性があります。")
print("---------------------------------------------------------------------\n")
id = str(input("SEGA IDを入力してください : "))
password = str(input("パスワードを入力してください : "))

r = requests.get("https://ongeki-net.com/ongeki-mobile/")

print("あなたのSEGAIDは " + id + " です")
print("パスワードは " + password + " を入力します")
print("\n データ取得中… \n")
time.sleep(3)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://ongeki-net.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://ongeki-net.com/ongeki-mobile/',
    'Accept-Language': 'ja',
}

data = {
    'segaId': id,
    'password': password,
    'save_cookie': 'save_cookie',
    'token': BeautifulSoup(r.text, 'html.parser').find(attrs={'name': 'token'}).get('value')
}

rr = requests.post('https://ongeki-net.com/ongeki-mobile/submit/', headers=headers,
                   cookies=r.cookies.get_dict(), data=data, allow_redirects=False)
login = requests.get('https://ongeki-net.com/ongeki-mobile/aimeList/submit/?idx=0',
                     headers=headers, cookies=r.cookies.get_dict() | rr.cookies.get_dict(), allow_redirects=False)
data = BeautifulSoup(requests.get("https://ongeki-net.com/ongeki-mobile/home/ratingTargetMusic/",
                     headers=headers, cookies=login.cookies.get_dict(), data=data).text, 'html.parser')
print("称号: " + data.find("div",
      class_=lambda value: value and value.startswith('trophy_block')).text.strip())
print("レベル: " + data.find("div", class_='reincarnation_block').text.strip() +
      data.find("div", class_=lambda value: value and value.startswith('lv_block')).text.strip())
print("名前: " + data.find("div",
      class_=lambda value: value and value.startswith('name_block')).text.strip())
print("RATING: " + data.find_all("div",
      class_=lambda value: value and value.startswith('rating_field'))[1].text.strip())

counter = 0
new_song = 0
best_song = 0
recent_song = 0

for list in data.find_all("div", class_=lambda value: value and value.startswith('basic_btn')):
    if counter == 0:
        print("---------------------------------------------------------------------------\n\n\n\n新曲")
    elif counter == 15:
        print("---------------------------------------------------------------------------\n\n\n\nベスト")
    elif counter == 45:
        print("---------------------------------------------------------------------------\n\n\n\nリーセント")
    elif counter == 55:
        print("---------------------------------------------------------------------------\n\n\n\nレーティング候補曲")
    print("---------------------------------------------------------------------------")
    song = list.find(
        "div", class_=lambda value: value and value.startswith('music_label')).text
    print("楽曲名: " + song)
    if "master" in list.find_all("img")[1].get('src'):
        difficult = "Master"
        print("難易度: Master")
    elif "expert" in list.find_all("img")[1].get('src'):
        difficult = "Expert"
        print("難易度: Expert")
    elif "advanced" in list.find_all("img")[1].get('src'):
        difficult = "Advanced"
        print("難易度: Advanced")
    elif "basic" in list.find_all("img")[1].get('src'):
        difficult = "Basic"
        print("難易度: Basic")
    elif "lunatic" in list.find_all("img")[1].get('src'):
        difficult = "Lunatic"
        print("難易度: Lunatic")
    level = list.find("div", class_=lambda value: value and value.startswith(
        'score_level')).text.strip()
    print("楽曲レベル: " + level)
    score = list.find(
        "div", class_=lambda value: value and value.startswith('f_14')).text
    print("テクニカルスコア: " + score)
    for list in music_l:
        if song.lower() in list[0].lower():
            if difficult in list[1]:
                if level in list[2]:
                    print("譜面定数: " + list[3])
                    if counter < 15:
                        if 970000 <= int(score.replace(",", "")) < 990000:
                            rating_default = float(list[3])
                            score_rate = int(score.replace(",", "")) - 970000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            new_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 990000 <= int(score.replace(",", "")) < 994000:
                            rating_default = float(list[3]) + 1.0
                            score_rate = int(score.replace(",", "")) - 990000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            new_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 994000 <= int(score.replace(",", "")) < 1000000:
                            rating_default = float(list[3]) + 1.2
                            score_rate = int(score.replace(",", "")) - 994000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            new_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1000000 <= int(score.replace(",", "")) < 1030000:
                            rating_default = float(list[3]) + 1.5
                            score_rate = int(score.replace(",", "")) - 1000000
                            rating_add = float(round(score_rate/150*0.01, 2))
                            rate = rating_add + rating_default
                            new_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1003000 <= int(score.replace(",", "")) < 1007500:
                            rating_default = float(list[3]) + 1.7
                            score_rate = int(score.replace(",", "")) - 1003000
                            rating_add = float(round(score_rate/150*0.01, 2))
                            rate = rating_add + rating_default
                            new_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1007500 <= int(score.replace(",", "")):
                            rating_default = float(list[3]) + 2.0
                            new_song += rating_default
                            print("レーティング: " + str(rating_default))
                    elif 14 < counter <= 44:
                        if 970000 <= int(score.replace(",", "")) < 990000:
                            rating_default = float(list[3])
                            score_rate = int(score.replace(",", "")) - 970000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            best_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 990000 <= int(score.replace(",", "")) < 994000:
                            rating_default = float(list[3]) + 1.0
                            score_rate = int(score.replace(",", "")) - 990000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            best_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 994000 <= int(score.replace(",", "")) < 1000000:
                            rating_default = float(list[3]) + 1.2
                            score_rate = int(score.replace(",", "")) - 994000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            best_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1000000 <= int(score.replace(",", "")) < 1030000:
                            rating_default = float(list[3]) + 1.5
                            score_rate = int(score.replace(",", "")) - 1000000
                            rating_add = float(round(score_rate/150*0.01, 2))
                            rate = rating_add + rating_default
                            best_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1003000 <= int(score.replace(",", "")) < 1007500:
                            rating_default = float(list[3]) + 1.7
                            score_rate = int(score.replace(",", "")) - 1003000
                            rating_add = float(round(score_rate/150*0.01, 2))
                            rate = rating_add + rating_default
                            best_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1007500 <= int(score.replace(",", "")):
                            rating_default = float(list[3]) + 2.0
                            best_song += rating_default
                            print("レーティング: " + str(rating_default))
                    elif 44 < counter <= 54:
                        if 970000 <= int(score.replace(",", "")) < 990000:
                            rating_default = float(list[3])
                            score_rate = int(score.replace(",", "")) - 970000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            recent_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 990000 <= int(score.replace(",", "")) < 994000:
                            rating_default = float(list[3]) + 1.0
                            score_rate = int(score.replace(",", "")) - 990000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            recent_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 994000 <= int(score.replace(",", "")) < 1000000:
                            rating_default = float(list[3]) + 1.2
                            score_rate = int(score.replace(",", "")) - 994000
                            rating_add = float(round(score_rate/200*0.01, 2))
                            rate = rating_add + rating_default
                            recent_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1000000 <= int(score.replace(",", "")) < 1030000:
                            rating_default = float(list[3]) + 1.5
                            score_rate = int(score.replace(",", "")) - 1000000
                            rating_add = float(round(score_rate/150*0.01, 2))
                            rate = rating_add + rating_default
                            recent_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1003000 <= int(score.replace(",", "")) < 1007500:
                            rating_default = float(list[3]) + 1.7
                            score_rate = int(score.replace(",", "")) - 1003000
                            rating_add = float(round(score_rate/150*0.01, 2))
                            rate = rating_add + rating_default
                            recent_song += rate
                            print("レーティング: " + str(rating_add+rating_default))
                        elif 1007500 <= int(score.replace(",", "")):
                            rating_default = float(list[3]) + 2.0
                            recent_song += rating_default
                            print("レーティング: " + str(rating_default))
    counter += 1
print("---------------------------------------------------------------------------\nレート: " +
      str(round((new_song/15 + best_song/30 + recent_song/10)/3, 2)))
print("新曲レート:" + str(round((new_song/15), 2)))
print("ベストレート:" + str(round((best_song/30), 2)))
print("リーセントレート:" + str(round((recent_song/10), 2)))
print("※オンゲキ.net側でのレートの表記と差異があります。目安程度という扱いでお願いします。")
input()
