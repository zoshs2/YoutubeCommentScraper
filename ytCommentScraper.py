import os
import datetime
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

# Queue의 기본적인 기능 구현
class Queue():
    def __init__(self, maxsize):
        self.queue = []
        self.maxsize = maxsize
        
    # Queue에 Data 넣음
    def enqueue(self, data):
        self.queue.append(data)

    # Queue에 가장 먼저 들어온 Data 내보냄
    def dequeue(self):
        dequeue_object = None
        if self.isEmpty():
            print("Queue is Empty")
        else:
            dequeue_object = self.queue[0]
            self.queue = self.queue[1:]
        return dequeue_object
    
    # Queue에 가장 먼저들어온 Data return
    def peek(self):
        peek_object = None
        if self.isEmpty():
            print("Queue is Empty")
        else:
            peek_object = self.queue[0]
        return peek_object
    
    # Queue가 비어있는지 확인
    def isEmpty(self):
        is_empty = False
        if len(self.queue) == 0:
            is_empty = True
        return is_empty
    
    # Queue의 Size가 Max Size를 초과하는지 확인
    def isMaxSizeOver(self):
        queue_size = len(self.queue)
        if (queue_size > self.maxsize):
            return False
        else :
            return True

        
if __name__=="__main__":
    # Set Chrome webdriver options
    options = webdriver.ChromeOptions()
    options.add_argument('disable-gpu')
    options.add_argument('user')
    options.add_argument('--no-sandbox')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    options.add_argument("lang=ko_KR")
    
    '''
    # 1) 일반적으로 쓰이는 방법: 24년 11월 기준, 크롬클라이언트(실제 우리가 로컬에서 쓰는 브라우저의) 버전은 131 인데, 
    # ChromeDriverManager().install()로 하면, 131 버전과 호환되는 드라이버 설치가 불가능함.
    # 따라서, 이 경우에는 직접 크롬드라이버를 다운받아서 executable_path로 지정해줘야 함.
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    '''
    # 2) 최신크롬드라이버 다운경로: https://googlechromelabs.github.io/chrome-for-testing/
    driver = webdriver.Chrome(executable_path='~/Documents/YoutubeComment/ChromeDriverLatest/chromedriver-mac-x64/chromedriver', options=options) # TODO; 올바른 경로로 설정
    driver.maximize_window()

    # Crawling Youtube Video's URL
    data_list = []
    driver.get("https://www.youtube.com/watch?v=jNQXAC9IVRw") # TODO: 탐색하고자 하는 유튭 URL 
    # Caution!!! When a browser window popped out, you should come back and stay in the terminal where you ran this script, till < Notice Message > shown.
    
    print("< Notice Message >:: Go Back to Web, and Staring at it")
    time.sleep(8)

    # Down the scroll
    body = driver.find_element_by_tag_name('body')
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    # max size 50의 Queue 생성
    # 0.1sec * 100 = 10sec 동안 Scroll 업데이트가 없으면 스크롤 내리기 종료
    szQ = Queue(100)
    enqueue_count = 0
    
    while True:
        # Scroll 내리기
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        
        # Scroll Height를 가져오는 주기
        time.sleep(0.1)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        # Queue가 꽉 차는 경우 스크롤 내리기 종료
        if(enqueue_count > szQ.maxsize):
            break
        
        # 첫 Loop 수행 (Queue가 비어있는 경우) 예외 처리
        if(szQ.isEmpty()) :
            szQ.enqueue(new_page_height)
            enqueue_count += 1
            
        # Queue에 가장 먼저 들어온 데이터와 새로 업데이트 된 Scroll Height를 비교함
        # 같으면 그대로 Enqueue, 다르면 Queue의 모든 Data를 Dequeue 후 새로운 Scroll Height를 Enqueue 함.    
        else :
            if(szQ.peek() == new_page_height) :
                szQ.enqueue(new_page_height)
                enqueue_count += 1
            else :
                szQ.enqueue(new_page_height)
                for z in range(enqueue_count) :
                    szQ.dequeue()
                enqueue_count = 1
    
    html0 = driver.page_source
    driver.close()
    html = BeautifulSoup(html0, 'html.parser')
    comments_list = html.findAll('ytd-comment-thread-renderer', {'class':'style-scope ytd-item-section-renderer'})

    data = {'youtube_id': [], 'comment': []}
    for j in range(len(comments_list)):
        comment = comments_list[j].find('yt-formatted-string',{'id':'content-text'}).text
        comment = comment.replace('\n', '')
        comment = comment.replace('\r', '')
        comment = comment.replace('\t', '')
        comment = comment.replace(' ', '')

        youtube_id = comments_list[j].find('a', {'id': 'author-text'}).span.text
        youtube_id = youtube_id.replace('\n', '') 
        youtube_id = youtube_id.replace('\t', '')
        youtube_id = youtube_id.strip()
    
        data['youtube_id'].append(youtube_id)
        data['comment'].append(comment)
    
    result_df = pd.DataFrame(data) 
    now = datetime.datetime.now()
    scrap_time = f"_{now.year}{now.month:02d}{now.day:02d}_{now.hour:02d}{now.minute:02d}_0"
    FILENAME = "YOUTUBE_COMMENTS_RESULTS" # TODO: filename for prefix
    full_name = FILENAME + scrap_time
    BasePath = '~/Documents/YoutubeComment' # TODO: saving path
    while os.path.exists(os.path.join(BasePath, full_name)):
        idx = full_name.split('_')[-1]
        full_name = full_name[:-len(idx)] + str(int(idx) + 1)

    full_name += '.pkl'
    result_df.to_pickle(full_name)