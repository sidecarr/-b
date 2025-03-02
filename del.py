
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
    'Referer': 'https://www.bilibili.com/',
    "User-Agent":"",
    'Cookie': ""
}

url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid=&timezone_offset=-480'

req = requests.get(url, headers=headers).json()
dynamic = req["data"]["items"]

space_id = {}
every_orig_id = []
for i in range(len(dynamic)):
    if "orig" in dynamic[i]:
        every_orig_id.append(dynamic[i]["orig"]["id_str"])
        space_id[dynamic[i]["orig"]["id_str"]] = dynamic[i]["id_str"]

next_page_id = dynamic[-1]["id_str"]

#first page
url_orig_model = 'https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice?dynamic_id='
has_lottery_result = []
for i in range(len(every_orig_id)):
    url_orig = url_orig_model + every_orig_id[i]
    req_judge = requests.get(url_orig,headers=headers).json()
    if "lottery_result" in req_judge["data"]:
        has_lottery_result.append(every_orig_id[i])
print("page 1 loaded")
#other pages
url_orig_model_1 = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset="
url_orig_model_2 = "&host_mid=&timezone_offset=-480"
flag = 2
while(1):
    try:
        url_orig_next = url_orig_model_1+next_page_id+url_orig_model_2
        req = requests.get(url_orig_next,headers=headers).json()
        dynamic = req["data"]["items"]

        every_orig_id = []
        for i in range(len(dynamic)):
            if "orig" in dynamic[i]:
                every_orig_id.append(dynamic[i]["orig"]["id_str"])
                space_id[dynamic[i]["orig"]["id_str"]] = dynamic[i]["id_str"]

        next_page_id = dynamic[-1]["id_str"]
    except IndexError:
        break

    for i in range(len(every_orig_id)):
        if every_orig_id[i]:
            url_orig = url_orig_model + every_orig_id[i]
            req_judge = requests.get(url_orig, headers=headers).json()
            if "lottery_result" in req_judge["data"]:
                has_lottery_result.append(every_orig_id[i])
    print("page "+str(flag)+ " loaded")
    flag+=1

space_id_list = []
for i in range(len(has_lottery_result)):
    space_id_list.append(space_id[has_lottery_result[i]])

print("-----------------")
print(str(len(has_lottery_result))+" counted")
time.sleep(2)
print("跳转--")
#delet with selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
browser = webdriver.Chrome(options=options)
for i in range(len(space_id_list)):
    url = "https://t.bilibili.com/" + space_id_list[i]
    browser.get(url)
    # time.sleep(1)
    # browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div[4]/div').click()
    # browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div[4]/div/div/div[2]/div').click()
    # browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/button[1]').click()
    # browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div[1]/div/div[2]/div[4]/div/div').click()
    # browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div[1]/div/div[2]/div[4]/div/div/div/div/div/div[3]/div/div/div').click()
    # browser.find_element_by_xpath('/html/body/div[5]/div[2]/div[4]/button[2]').click()
    # time.sleep(1)
    try:
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/div[1]/div/div[2]/div[4]/div/div').click()
        WebDriverWait(browser, 2).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="app"]/div[3]/div[1]/div[1]/div/div[2]/div[4]/div/div/div/div/div/div[3]/div/div/div'))
        ).click()
        WebDriverWait(browser, 2).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/div[4]/button[2]'))
        ).click()
    except Exception as e:
        print(f"处理 {url} 失败: {e}")
browser.get("https://bilibili.com/")
