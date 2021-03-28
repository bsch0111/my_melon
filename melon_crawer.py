import requests
import lxml.html
import sqlite3

class crawer:
    
    def __init__(self):
        self.base_list_url = 'https://www.melon.com/mymusic/playlist/mymusicplaylist_list.htm?memberKey=41920075'
        self.header = { 'User-Agent' : 'Mozilla/5.0'}
        self.init_playlist_url = []
        self.detail_playlist_url = []
        self.html_list= []

    def put_database(self):
        if len(self.detail_playlist_url) == 0 :
            print('상세 플레이리스트가 지정되지 않았습니다.')
            print('get_detail_play_list()를 수행하세요')
            return False
        
        conn = sqlite3.connect('./music.db')
        db_cursor = conn.cursor()
        db_cursor.executemany('INSERT INTO PLAYLIST(playlist_url) values(?)',self.detail_playlist_url)
        conn.commit()
        conn.close()
        return True

    def get_detail_play_list(self):
        '''
        플레이리스트 안에 음악목록을 가져오기 위한 URL 목록을 수집한다.
        해당 부분은 멜론에서 처리한 부분때문에 단순한 get 요청으로 받아오지 못한다.
        - selenium을 통해 html 을 수집한다.
        '''
        
        self.init_play_list()
        # 카운트가 지정되지 않은 init_playlist_url
        init_playlist_url = self.init_playlist_url
        
        from selenium import webdriver
        wd = webdriver.Chrome('./chromedriver')
        count = 0
        for index, playlist_url in enumerate(init_playlist_url) :
            wd.get(playlist_url)
            p_html = wd.page_source

            html_root = lxml.html.fromstring(p_html)
            p_count = html_root.xpath("//span[@class='cnt']")[0].text
            p_count = p_count.replace("(","")
            p_count = p_count.replace(")","")
            count = int(p_count)

            page_num = count//50
            page_list = [str(p_page * 50 + 1) for p_page in range(page_num + 1) ]
            #if page_list == [''] : page_list = ['1'] 

            for start_index in page_list :
                self.detail_playlist_url.append((playlist_url + start_index,))
                print(self.detail_playlist_url[-1])
            
        return self.detail_playlist_url
        


    def init_play_list(self) :
        '''
        플레이리스트 목록을 가져오는 함수
        - 플레이리스트만 가져올 뿐 플레이리스트 안에 음악목록은 가져오지 않는다.
        '''
        
        
        base_list_url = self.base_list_url 
        header =self.header 
        
        playno_list = []
        r = requests.get(base_list_url,headers=header)

        if r.status_code != 200:
            print('URL에서 GET 요청을 받아주지 않습니다')
            return self.init_playlist_url

        html = r.text
        root_element = lxml.html.fromstring(html)
        buttons = root_element.xpath("//button[@class='btn_icon like']")

        for button in buttons :
            playno_list.append(button.attrib['data-play-no'])

        playno_list.append('475596947')
        playno_list.append('475336153')
        playno_list.append('467370167')
        playno_list.append('456850600')

        for playno in playno_list :
            self.init_playlist_url.append(f"https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq={playno}#params[plylstSeq]={playno}&po=pageObj&startIndex=")


        return self.init_playlist_url
