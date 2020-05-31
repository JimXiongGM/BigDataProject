#!/usr/bin/python
'''
@Author：gm_xiong@pku.edu.cn
'''
import sys,json,time,traceback,os
import random

def key_to_slot(timestamp):
    # return timestamp belongs to which slot (1~18)
    # make sure the timestamp can be transfered to INT !
    '''
    2017年1月1日 | 1483200000
    2017年2月1日 | 1485878400
    2017年3月1日 | 1488297600
    2017年4月1日 | 1490976000
    2017年5月1日 | 1493568000

    2017年6月1日 | 1496246400
    2017年7月1日 | 1498838400
    2017年8月1日 | 1501516800
    2017年9月1日 | 1504195200
    2017年10月1日 | 1506787200

    2017年11月1日 | 1509465600
    2017年12月1日 | 1512057600
    2018年1月1日 | 1514736000
    2018年2月1日 | 1517414400
    2018年3月1日 | 1519833600

    2018年4月1日 | 1522512000
    2018年5月1日 | 1525104000
    2018年6月1日 | 1527782400
    2018年7月1日 | 1530374400
    '''
    try :
        timestamp = int (timestamp)
    except:
        return 0
    if timestamp >= 1483200000 and timestamp < 1485878400:    #2017M1
        return 1
    elif timestamp >= 1485878400 and timestamp < 1488297600:    #2017M2
        return 2
    elif timestamp >= 1488297600 and timestamp < 1490976000:    #2017M3
        return 3
    elif timestamp >= 1490976000 and timestamp < 1493568000:    #2017M4
        return 4
    elif timestamp >= 1493568000 and timestamp < 1496246400:    #2017M5
        return 5
    elif timestamp >= 1496246400 and timestamp < 1498838400:    #2017M6
        return 6
    elif timestamp >= 1498838400 and timestamp < 1501516800:    #2017M7
        return 7
    elif timestamp >= 1501516800 and timestamp < 1504195200:    #2017M8
        return 8
    elif timestamp >= 1504195200 and timestamp < 1506787200:    #2017M9
        return 9
    elif timestamp >= 1506787200 and timestamp < 1509465600:    #2017M10
        return 10
    elif timestamp >= 1509465600 and timestamp < 1512057600:    #2017M11
        return 11
    elif timestamp >= 1512057600 and timestamp < 1514736000:    #2017M12
        return 12
    elif timestamp >= 1514736000 and timestamp < 1517414400:    #2018M1
        return 13
    elif timestamp >= 1517414400 and timestamp < 1519833600:    #2018M2
        return 14
    elif timestamp >= 1519833600 and timestamp < 1522512000:    #2018M3
        return 15
    elif timestamp >= 1522512000 and timestamp < 1525104000:    #2018M4
        return 16
    elif timestamp >= 1525104000 and timestamp < 1527782400:    #2018M5
        return 17
    elif timestamp >= 1527782400 and timestamp < 1530374400:    #2018M6
        return 18
    else:
        return 0
        
for line in sys.stdin:

    #line = line.replace("\"",'')

    data_dict = json.loads(line.replace(" ",""))

    sort_key_list = sorted(data_dict)  #这是key组成的list

    #Hadoop环境使用
    
    filename = os.environ["mapreduce_map_input_file"]
    try:
        filename = filename.split('/')[-1].split('_')[0]
    except:
        filename = "NmaeError"
    

    #本地测试使用
    #filename = "filename_test_"+str(random.randint(0,999))

    for key in data_dict:
        slot = key_to_slot(key)
        #salesrank的18个卡槽，一个key值一个
        ranks_slot = [0 for i in range(0,18)]
        if slot == 0 :
            continue
        ranks_slot[slot-1] = data_dict[key]

        ranks_slot=[str(i) for i in ranks_slot]
        print (filename+'\t'+'|'.join(ranks_slot))

# cat 000721393X_com_norm.json | reducer_18months.py
# :set ff=unix