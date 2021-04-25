import os
from bs4 import BeautifulSoup
import urllib.request as req
import requests
import time

headers = {
    "user-agent" : "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2825.67 Safari/537.36",
    "cookie" : "customLocale=zh_TW"
}
number = input('輸入車號：')

url1 = 'https://www.wnacg.org/photos-slide-aid-'+ number + '.html'
print(url1)
request = req.Request(url1, headers=headers)
with req.urlopen(request) as response:
    Wnacg_data1 = response.read().decode('utf-8')  

Wnacg_title1 = BeautifulSoup(Wnacg_data1,'html.parser')#'html.parser'為HTML的解析器
file_name = Wnacg_title1.title.text.replace(' - 列表 - 紳士漫畫-專註分享漢化本子|邪惡漫畫','')
# print(file_name)

url2 = 'https://www.wnacg.org/photos-gallery-aid-'+ number + '.html'
print(url2)
request = req.Request(url2, headers=headers)
with req.urlopen(request) as response:
    Wnacg_data2 = response.read().decode('utf-8')
Wnacg_title2 = BeautifulSoup(Wnacg_data2,'html.parser')
SWnacg_title2 = str(Wnacg_title2)
SWnacg = SWnacg_title2.split(';')[16] # 將str切分成list
# print(SWnacg[16])

SWnacg = SWnacg.split("url: fast_img_host+\\")
# print(SWnacg)

i=1
links=[]
while(i < len(SWnacg)-1):
    # print(SWnacg[i])
    if i != len(SWnacg)-1:
        SWnacg1 = SWnacg[i].replace('"//','')
        posi = SWnacg1.find('\\')
        # SWnacg2 = SWnacg1.replace('\\", caption: \\"[00' + str(i) + ']\\"},{ ','') 不夠嚴謹
        SWnacg2 = SWnacg1.replace(SWnacg1[posi:],'')

    links.append(SWnacg2)
    i += 1
# print(links[0])

file_path = 'D:\\Users\\Desktop' + '\\' + file_name
if not os.path.exists(file_path):
    try:
        os.mkdir(file_path)
    except:
        print('該車車的名字：', file_name)
        os.mkdir('D:\\Users\\Desktop' + '\\待命名')
        file_path =  'D:\\Users\\Desktop' + '\\待命名'

from tqdm import tqdm   #進度條    
progress = tqdm(total = len(links))
index = 1
for link in links:
    img = requests.get('https://'+link, allow_redirects=True)
    picture = open(file_path + "\\" + str(index) + '.png', "wb")  # 開啟資料夾及命名圖片檔 # 寫入圖片的二進位碼 
    picture.write(img.content)
    picture.close()
    # print(str(index) + '/' + str(len(links)) + '   Done!')
    progress.update(1)  #進度條更新
    index += 1
    # time.sleep(1.5)
