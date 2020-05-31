#!/usr/bin/python
import sys

ing_filename = None
filename = None
slot_num = 18
ing_slot_accumlators = [0 for i in range(0,slot_num)]
ing_slot_sums = [0 for i in range(0,slot_num)]

def trans_to_int(s):
    try:
        return int(s)
    except:
        return 0

for line in sys.stdin:

    line = line.strip()

    filename,slot_string = line.split('\t', 1)

    slot_list = slot_string.split('|')
    int_slot_list = [trans_to_int(i) for i in slot_list]

    # 如果遇到相同key
    if ing_filename == filename:

        for i in range(0,slot_num):
            if int_slot_list[i] == 0 :
                continue
            ing_slot_accumlators[i] += 1    
            ing_slot_sums[i] += int_slot_list[i]

    # key不同
    else:
        if ing_filename:
            result_list = [0 for i in range(0,slot_num)]
            for i in range(0,slot_num):
                if  ing_slot_accumlators[i] == 0:
                    continue
                result_list[i] = int(ing_slot_sums[i]/ing_slot_accumlators[i])
            result_list = [str(i) for i in result_list]
            print (filename+'\t'+'\t'.join(result_list))    

        # 初始化
        ing_slot_accumlators = [0 for i in range(0,slot_num)]
        ing_slot_sums = [0 for i in range(0,slot_num)]
        ing_filename = filename

        # 第一次累加
        for i in range(0,slot_num):
            if int_slot_list[i] == 0 :
                continue
        ing_slot_accumlators[i] += 1    
        ing_slot_sums[i] += int_slot_list[i]


# print 最后一个
result_list = [0 for i in range(0,slot_num)]
for i in range(0,slot_num):
    if  ing_slot_accumlators[i] == 0:
        continue
    result_list[i] = int(ing_slot_sums[i]/ing_slot_accumlators[i])
result_list = [str(i) for i in result_list]
print (filename+'\t'+'\t'.join(result_list)) 

# cat 000721393X_com_norm.json | ./mapper_18months.py | sort -t ' ' -k 1 | ./reducer_18months.py