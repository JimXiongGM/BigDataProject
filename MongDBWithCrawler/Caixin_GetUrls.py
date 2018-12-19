#!/usr/bin/python
'''
@Author：gm_xiong@pku.edu.cn
'''
import urllib,os,traceback,json
from time import sleep
import urllib.request

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  
        os.makedirs(path)  
        #print ("---  new folder...  ---")
    else:
        #print "---  There is this folder!  ---"
        pass

def biuld_headers(channel):
    
    channel_dict = {129:"economy",
                    125:"finance",
                    130:"companies",
                    131:"china",
                    179:"science",
                    132:"international",
                    126:"opinion"}

    headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "CX_FROM=null; GUID=374320945; T_GUID=1544714157942; _ga=GA1.2.451917024.1544714159; gr_user_id=7061674b-4a40-4b6c-8287-7c2b6a91343e; grwng_uid=fab5ca29-4507-4652-947f-150a5da5bb50; point=1545235199000; 872f3eaac31f373e_gr_session_id=330d19fa-aa4b-4d43-a5d8-330060ddf508; _gid=GA1.2.602572359.1545182523; JSESSIONID=D884ECB43FCC7FA7D3F91E1A362773C8; CAIXIN_UUID=802b89fa54c04cf1aaaff276251f2c4d; GID30=1612784707; gr_session_id_872f3eaac31f373e=d8503aca-dd15-4c47-b1fd-53706dec5da7; gr_session_id_872f3eaac31f373e_d8503aca-dd15-4c47-b1fd-53706dec5da7=true; SA_AUTH_TYPE=%E8%B4%A2%E6%96%B0%E7%BD%91; myStast=2018-12-19; 872f3eaac31f373e_gr_last_sent_sid_with_cs1=330d19fa-aa4b-4d43-a5d8-330060ddf508; 872f3eaac31f373e_gr_last_sent_cs1=7907018; 872f3eaac31f373e_gr_session_id_330d19fa-aa4b-4d43-a5d8-330060ddf508=true; myloginMode=email; SA_USER_auth=5a3e2evwalJGYEVMUCMQkiCptCC1KDwNVShUcFLARommeSnVs%2BLVPrubRwEtEPY8cYP%2B4ZdA1ZcuDu%2BKTHpqF4Ks2WmkxrKMHsyjAVDXGVw7FXxkAvE47nxFCVQ0F7V%2BYsku; UID=7907018; SA_USER_UID=7907018; SA_USER_NICK_NAME=GentleMingJim; SA_USER_USER_NAME=gm_xiong@qq.com; SA_USER_UNIT=1; SA_USER_DEVICE_TYPE=5; USER_LOGIN_CODE=283474CDBF3015B2684EFF2F4B336BC2; ENTITY_ID=; backUrl=http%3A//economy.caixin.com/; ENTITY_COUNT=2; lastTime=1545185495646; firstTime=1545185495646; 872f3eaac31f373e_gr_cs1=7907018; _gat=1",
    "DNT": 1,
    "Host": "tag.caixin.com",
    "Referer": "http://"+str(channel_dict[channel])+".caixin.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
    }

    return headers


def fetchJSON():

    #129:economy  125:finance  130:companies  131:china  179:science 132:international  126:opinion
    channel_list = [129,125,130,131,179,132,126]

    mkdir("./caixin_news/urls/")

    for channel in channel_list:
        start=0
        count=100

        #skip filter
        if channel in []:
            continue

        #max:1000
        for i in range(1,20):

            url = 'http://tag.caixin.com/news/homeInterface.jsp?channel='+str(channel)+'&start='+str(start)+'&count='+str(count)+'&picdim=_145_97&callback=jQuery17203729076279107504_1545182543901&_=1545183065166'
            request = urllib.request.Request(url=url,headers=biuld_headers(channel))

            try:
                response = urllib.request.urlopen(request)
            except Exception as err:
                traceback.print_exc()
                break
            context = response.read().decode('utf-8').strip()

            if "link" not in context:
                print ("no tags! now start = "+str(start))
                print ("response :　\n"+context)
                break

            first_occur = context.find("(")

            # slice the json part
            context = context[first_occur+1:-2]
        
            with open('./caixin_news/urls/caixin_'+str(channel)+'_'+str(start)+'_'+str(count)+'.json','w',encoding='utf-8') as fp:
                fp.write(context)
            start += count
            print ("success : " + str(channel) + "_" + str(start) )
            sleep(2)

def yield_file_from_filefold(file_path='./',pattern=""):
    '''return file iteraters with pattern 
    '''
    files_list = []
    if not file_path.endswith('/'):
        file_path+='/'
    try:
        # only have file name.
        for x in os.listdir(file_path):
            if pattern in x:
                files_list.append(x)
                #print (x)
        for i in range(len(files_list)):
            f = open(file_path + files_list[i], 'r',encoding='UTF-8')
            # file_contents=f.readlines()
            yield f
    except Exception as e:
        traceback.print_exc()
        os._exit(1)
    finally:
        pass
    

def yieldURL_fromJSON(channel):

    for json_file in yield_file_from_filefold("./caixin_news/urls/",pattern=str(channel)):
        js = json.loads(json_file.read())
        for item in js['datas']:
            try:
                #print (type(item))
                yield (item['link'])
            except Exception as err:
                traceback.print_exc()
        #break


if __name__=="__main__":
    url_list = [i for i in yieldURL_fromJSON(125)]
    print(url_list)


