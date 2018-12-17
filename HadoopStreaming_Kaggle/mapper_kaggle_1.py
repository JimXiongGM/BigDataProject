#!/usr/bin/python
import sys,json,time,traceback,os
import random

def trans_to_time(ss):
     try:
          return time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(float(ss)))
     except Exception as err:
          #traceback.print_exc()
          return 'time error: '+str(err)

for line in sys.stdin:

     #line = line.replace("\"",'')

     data_dict = json.loads(line.replace(" ",""))

     sort_key_list = sorted(data_dict)  #这是key组成的list
     sort_value_list = sorted(data_dict.values())  #这是values组成的list
     
     time_first = trans_to_time(sort_key_list[0])
     time_last = trans_to_time(sort_key_list[-1])

     null_value = sort_value_list.count("")

     #Hadoop环境使用
     #filename = os.environ["mapreduce_map_input_file"]

     #本地测试使用
     filename = "filename_test_"+str(random.randint(0,999))


     print ('%s_len\t%s'%(filename,str(len(data_dict))))
     print ('%s_first\t%s'%(filename,time_first))
     print ('%s_last\t%s'%(filename,time_last))

     if '2017-10-31' in time_first:
          print ('2017-10-31\t1')
     else:
          print ('2017-10-31\t0')




#{"1509379200":327588,"1509386400":348041,"1509393600":353297,"1509404400":369732}
