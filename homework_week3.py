import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.Sprata_homework

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

# 음악 제목
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(2) > td.info > a.title.ellipsis

# 가수 이름
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

# 앨범 이름
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.albumtitle.ellipsis

# 앨범 그림
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > a > span

# 노래 순위
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number

# 음악 차트 크롤링

musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for music in musics:
    name = music.select_one('td.info > a.title.ellipsis')
    rank_raw= music.select_one('td.number')
    rank = [int(i) for i in rank_raw.text.split() if i.isdigit()]
    artist = music.select_one('td.info > a.artist.ellipsis')
    album = music.select_one('td.info > a.albumtitle.ellipsis')
    #album_image = music.select_one('td:nth-child(3) > a > span')
    data = {
        'rank': rank[0],
        'name': name.text.strip(),
        'artist': artist.text,
        'album': album.text
    }
    #print(data) #제대로 찍히나 확인
    db.music_rank2.insert_one(data)
