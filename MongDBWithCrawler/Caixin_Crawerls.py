#!/usr/bin/python
'''
@Author：gm_xiong@pku.edu.cn
'''
import urllib,os,traceback,Caixin_GetUrls
from time import sleep
from multiprocessing import Pool
import urllib.request

def biuld_headers(url):
    headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "CX_FROM=null; GUID=374320945; T_GUID=1544714157942; _ga=GA1.2.451917024.1544714159; gr_user_id=7061674b-4a40-4b6c-8287-7c2b6a91343e; grwng_uid=fab5ca29-4507-4652-947f-150a5da5bb50; point=1545235199000; _gid=GA1.2.602572359.1545182523; CAIXIN_UUID=802b89fa54c04cf1aaaff276251f2c4d; SA_AUTH_TYPE=%E8%B4%A2%E6%96%B0%E7%BD%91; myStast=2018-12-19; 872f3eaac31f373e_gr_last_sent_cs1=7907018; myloginMode=email; SA_USER_auth=5a3e2evwalJGYEVMUCMQkiCptCC1KDwNVShUcFLARommeSnVs%2BLVPrubRwEtEPY8cYP%2B4ZdA1ZcuDu%2BKTHpqF4Ks2WmkxrKMHsyjAVDXGVw7FXxkAvE47nxFCVQ0F7V%2BYsku; UID=7907018; SA_USER_UID=7907018; SA_USER_NICK_NAME=GentleMingJim; SA_USER_USER_NAME=gm_xiong@qq.com; SA_USER_UNIT=1; SA_USER_DEVICE_TYPE=5; USER_LOGIN_CODE=283474CDBF3015B2684EFF2F4B336BC2; GID30=380489774; 872f3eaac31f373e_gr_session_id=42234c1c-fd7b-4e75-b787-38883ebb37f7; 872f3eaac31f373e_gr_last_sent_sid_with_cs1=42234c1c-fd7b-4e75-b787-38883ebb37f7; 872f3eaac31f373e_gr_session_id_42234c1c-fd7b-4e75-b787-38883ebb37f7=true; backUrl=http%3A//economy.caixin.com/2018-12-02/101354516.html; ENTITY_ID=101354516; SA_USER_AUTH_Statistics=1; 872f3eaac31f373e_gr_cs1=7907018; ENTITY_COUNT=1; lastTime=1545204264126; firstTime=1545204264126",
    "DNT": 1,
    "Host": "gateway.caixin.com",
    "Referer": str(url),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
    }
    return headers

def try_to_get_content(Req):
    try:
        response = urllib.request.urlopen(Req)
        content = response.read().decode('utf-8').strip()
        return content
    except:
        traceback.print_exc()
        return "error"

def start_with_channel(channel):

    Caixin_GetUrls.mkdir("./caixin_news/channel_"+str(channel))
    url_list = [i for i in Caixin_GetUrls.yieldURL_fromJSON(channel)]
    for url in url_list:
        tid = url.split('/')[-1].split('.')[0]
        content = ''
        if os.path.exists("./caixin_news/channel_"+str(channel)+"/"+tid+".txt"):
            #print("yes")
            continue

        retry=0
        url_content="http://gateway.caixin.com/api/newauth/checkAuthByIdJsonp?callback=jQuery172038107031974088157_1545204262982&type=0&id="+str(tid)+"&page=1"
        request = urllib.request.Request(url=url_content,headers=biuld_headers(url))

        while True :
            content_temp = try_to_get_content(request)
            if retry>=3 or content_temp!="error":
                break
            else:
                retry+=1
        content+=content_temp

        with open("./caixin_news/channel_"+str(channel)+"/"+tid+".txt",'w',encoding='UTF-8') as f1:
            f1.write(content)
        sleep(2)

        #break

def multi_process_strat(processes_num):
    
    p = Pool(processes=int(processes_num))

    #129:economy  125:finance  130:companies  131:china  
    #179:science 132:international  126:opinion
    arg_list=[129,125,130,131,179,132,126]

    for i in range(len(arg_list)):
        p.apply_async(start_with_channel, args=(arg_list[i],))

    p.close()
    p.join()
    print('All processes done!')

if __name__=="__main__":
    multi_process_strat(4)
    #start_with_channel(129)