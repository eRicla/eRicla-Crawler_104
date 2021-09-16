# Crawler_104 (純筆記)
練習爬蟲程式，主要是抓取104人力銀行的資料，程式裡面主要用到2個套件功能
- requests & beautifulsoup
- pandas

然後寫的過程中，有幾點是我自己印象深刻的

1. 判斷檔案是否存在，存在則刪除
```
import os
file = 'C:/crawler_104.xlsx'

if os.path.isfile(file): #判斷檔案是否存在
	os.remove              #若有，就刪除檔案
```

2. 加入headers
```
my_headers = {'User-Agent':'GoogleBot'} #注意大小寫
soup = requests.BeautifulSoup(url,headers=my_headers) #在做網頁解析時加入headers資訊，讓程式以為是Google機器人程式在抓的
```

3. 若遇到網頁元素一樣，則一次抓下來後在分段讀取，然後又因為欄位跟資料都放在一起，所以要在額外切開處理
```
url = 'https://www.104.com.tw/job/775pj?jobsource=hotjob_chr'

r = requests.get(url,headers=my_headers)
html = BeautifulSoup(r.text,'html.parser')
rs = html.find_all('div',class_='job-description-table row')
for r in rs:
  r1 = r.find_all('div',class_='row mb-2') #整個區塊都是這個元素
  r12 = r1[2].text.split()[-1]  #用split()切開，不放入值就是用空白分開，然後放[-1]就是切開後只抓取最後一欄的資料(從右邊開始數起)
```

4. 用pandas去寫入資料
```
要先定義一個list結構檔案
datas = {
  '頁數':[],
  '刊登日期':[],
  '職缺名稱':[],
}

#寫入df
datas['頁數'].append(page)
datas['刊登日期'].append(job_date)
datas['職缺名稱'].append(job_name)

# 使用pandas匯出excel
df = pd.DataFrame(datas, columns=['頁數','刊登日期', '職缺名稱'])
df.to_excel(file, encoding="utf-8", index=False)  #file的檔名跟路徑是在一開始就定義好的
```


#這是還原的版本
