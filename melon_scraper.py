import lxml.html

class Scraper :

    def __init__(self):
        self.url_list = []
        self.html_element_list = []
        pass
    
    def set_url_list(self) :
        import sqlite3
        conn = sqlite3.connect('./music.db')
        db_cursor = conn.cursor()
        db_cursor.execute('select * from playlist')
        # (id, url) 튜플을 담은 리스트의 형태로 데이터를 가져옴
        self.url_list = db_cursor.fetchall()
        conn.close()
        
    def set_page_resource(self) :
        from selenium import webdriver
        wd = webdriver.Chrome('./chromedriver')
        
        for url in self.url_list :
            p_url = url[1]
            wd.get(p_url)
            p_html = wd.page_source
            self.html_element_list.append(lxml.html.fromstring(p_html))

    def scraping_title_artist(self):
        import sqlite3
        conn = sqlite3.connect('./music.db')
        db_cursor = conn.cursor()


        for playlist_id, html_root in enumerate(self.html_element_list): 
            titles = html_root.xpath("//a[@class='btn btn_icon_detail']/span")
            artists = html_root.xpath("//div[@id='artistName']")
            
            if len(titles) != len(artists) :
                print('노래 제목과 아티스트의 수가 일치하지 않습니다.')
                print('해당 스크래이핑은 잘못되었습니다.')
            
            for key, artist_list in enumerate(artists) :
            
                title  = titles[key].text
                artist_string = ''
                for artist in artist_list :
                    artist_string = artist_string + artist.text + '. '
                
                db_cursor.execute("INSERT INTO MUSIC(title, artist, playlist_id) VALUES(?,?,?)", (title,artist_string,playlist_id))

        conn.commit()                
        conn.close()    

scraper = Scraper()
scraper.set_url_list()
scraper.set_page_resource()
scraper.scraping_title_artist()