#%%
!which python

#%%
import requests

#https://www.melon.com/mymusic/playlist/mymusicplaylist_list.htm?memberKey=41920075
#https://www.melon.com/mymusic/playlist/mymusicplaylist_list.htm?memberKey=41920075
#https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=490093573
#%%
my_music_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylist_list.htm?memberKey=41920075'

# 멜론의 request는 header 값이 있어야 크롤링 할 수 있음
# 헤더값이 없기 떄문에
# 그냥 하면 406 에러 (멜론에서 거부)
# 406 : Not Acceptable

# %%
r.text
# %%
# %%
r.text
# %%
# %%
r.text
# %%
# %%
r.text
# %%
# %%
r.text
# %%
hdr = { 'User-Agent' : 'Mozilla/5.0'}
r = requests.get(my_music_url,headers=hdr)

# %%
if r.status_code != 200:
    print('URL에서 GET 요청을 받아주지 않습니다')
    exit

# %%
import lxml.html
# %%
html = r.text
# %%
# text로 구성된 html 을 HtmlElement로 변경해서 사용 
root_element = lxml.html.fromstring(html)
# %%
type(root_element)
# %%
buttons = root_element.xpath("//button[@class='btn_icon like']")

    
#type(buttons[0])
buttons
#%%
playno_list = []
# %%
for button in buttons :
    playno_list.append(button.attrib['data-play-no'])

# %%
playno_list
#%%
len(playno_list)
#%%
playno_list
#%%
playno_list.append('475596947')
playno_list.append('475336153')
playno_list.append('467370167')
playno_list.append('456850600')

#%%
# 세부 플레이리스트 https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=475596947
for play_no in playno_list :
    urlp = 'https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=' + play_no
# %%
playno_list
# %%
header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}


r = requests.get('https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=456850600',headers = header)

# %%
r.text
#%%
root = lxml.html.fromstring(r.text)
# %%
root.xpath("//tr[@style='user-select: auto;']")
# %%
root.xpath("//dt")
# %%
root.xpath("//tbody")

# %%
# https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=456850600
# https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=456850600
# https://www.melon.com/mymusic/playlist/mymusicplaylistview_listSong.htm?plylstSeq

#%%
from bs4 import BeautifulSoup
#%%
url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=456850600'
r = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})

# %%
soup = BeautifulSoup(r.text,"html.parser")
# %%
from selenium import webdriver
wd = webdriver.Chrome('./chromedriver')

# %%
wd.get(url)
# %%
html_1 = wd.page_source
#%%
html_1_root = lxml.html.fromstring(html_1)

# %%
x = html_1_root.xpath("//span[@class='cnt']")[0].text
#%%
x = x.replace("(","")
x = x.replace(")","")
#%%
int(x)
#%%
page_num = int(x)//50 
t = [a*50 + 1 for a in range(page_num)]
if int(x)%50 > 0 :
    t.append((page_num)*50+1)  
#%%
t = t - 1
# %%
https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=456850600
https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=456850600#params[plylstSeq]=456850600&po=pageObj&startIndex=1
#params[plylstSeq]=456850600&po=pageObj&startIndex=101

#%%
# titles = html_1_root.xpath("//a[@class='fc_gray']")
# //a[@class='btn btn_icon_detail']/span

# %%
for key, title in enumerate(titles) :
    print(key, title.text)
# %%
titles = html_1_root.xpath("//a[@class='btn btn_icon_detail']/span")
artists = html_1_root.xpath("//div[@id='artistName']")
#%%
for key, artist in enumerate(artists) :
    print(f"Key : {key}, Artist : {len(artist)}")
# %%
if len(titles) != len(artists) :
    print('노래 제목과 아티스트의 수가 일치하지 않습니다.')
    print('해당 스크래이핑은 잘못되었습니다.')

#%%
#{'title': '제목', artist : 'artist'}
play_list = []

for key, artist_list in enumerate(artists) :
    title  = titles[key].text
    artist_string = ''
    for artist in artist_list :
        artist_string = artist_string + artist.text + '. '
    print('title : ', title)
    print('artist : ', artist_string)
    #play_list.append({'title' : title,'artist' : artist_string})
    
# %%
print(play_list)
# %%

import sqlite3
conn = sqlite3.connect('./music.db')
db_cursor = conn.cursor() 
#%%
detail_playlist_url = [('111',),('222',)]
#%%
db_cursor.executemany('INSERT INTO PLAYLIST(playlist_url) VALUES(?)',detail_playlist_url)
# %%
