import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

file = 'C:/crawler_104.xlsx'
if os.path.isfile(file):
      os.remove(file)

#放入user-agent，在瀏覽網站時才可以抓到資料
my_headers={"User-Agent":"GoogleBot"}
page = 1

#新增lisa，並放入欄位跟空值
datas = {
  '頁數':[],
  '刊登日期':[],
  '職缺名稱':[],
  '管理責任':[],
  '上班時段':[],
  '薪資':[],
  # '可上班日':[],
  '公司名稱':[],
  '公司地址':[],
  '出差外派':[],
  '網址':[]
}

#抓取網站資料
for i in range(1,21):
    url = f'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E8%B2%A1%E5%8B%99%E6%9C%83%E8%A8%88&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000&order=14&asc=0&page={page}&mode=s&jobsource=2018indexpoc' #財務會計

    url1 = f'https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007002000%2C2007001000&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000&order=11&asc=0&page={page}&mode=s&jobsource=2018indexpoc' #IT
    
    #解析網頁上的元素
    t = requests.get(url1, headers=my_headers)
    ObjSoup = BeautifulSoup(t.text,'html.parser')
    jobs = ObjSoup.find_all('article',class_='js-job-item')
    for job in jobs:
          job_date = job.find('span',class_="b-tit__date").text.strip()  #刊登日期
          job_name = job.find('a',class_="js-job-link").text #職缺名稱
          job_company_name = job.get('data-cust-name') #公司名稱
          job_company_addr = job.find('ul', class_='job-list-intro').find('li').text #地址
          job_pay = job.find('span',class_='b-tag--default').text #薪資
          job_link = job.find('a').get('href') #職缺網址，用於後面詳細資料解析

          #職缺詳細網址,先用?切開原本的工作清單網址，再去組合成工作職缺的詳細路徑
          sub_job_link = 'https:'+job_link.split('?')[0]+'?jobsource=hotjob_chr'

          #解析詳細工作明細網頁資料
          r = requests.get(sub_job_link,headers=my_headers)
          html = BeautifulSoup(r.text,'html.parser')
          rs = html.find_all('div',class_='job-description-table row')
          for r in rs:
              r1 = r.find_all('div',class_='row mb-2')
              r12 = r1[2].text.split()[-1]  #工作性質
              r13 = r1[3].text.split()[-1]  #上班地點
              r14 = r1[4].text.split()[-1]  #管理責任
              r15 = r1[5].text.split()[-1]  #出差外派
              r16 = r1[6].text.split()[-1]  #上班時段
              r17 = r1[7].text.split()[-1]  #休假制度
              # r18 = r1[8].text.split()[-1]  #可上班日
         
          try:
            # 寫入data frame
            datas['頁數'].append(page)
            datas['刊登日期'].append(job_date)
            datas['職缺名稱'].append(job_name)
            datas['管理責任'].append(r14)
            datas['上班時段'].append(r16)
            datas['薪資'].append(job_pay)
            # datas['可上班日'].append(r18)
            datas['公司名稱'].append(job_company_name)
            datas['公司地址'].append(job_company_addr)
            datas['出差外派'].append(r15)
            datas['網址'].append(sub_job_link)

            # 使用pandas匯出excel
            df = pd.DataFrame(datas, columns=['頁數','刊登日期', '職缺名稱','管理責任','上班時段','薪資','公司名稱','公司地址','出差外派','網址'])
            df.to_excel(file, encoding="utf-8", index=False)

          except IndexError:
                pass
          continue


    page = page + 1

