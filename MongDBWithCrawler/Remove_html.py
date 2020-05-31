#!/usr/bin/python
'''
@Author：gm_xiong@pku.edu.cn
'''
import re,Caixin_GetUrls,os,traceback

def remove_html(txt):
    try:
        return re.sub(r'<.*?>','',txt)
    except:
        traceback.print_exc()
        return txt

def start_remove(channel):
    Caixin_GetUrls.mkdir("./caixin_news/Clear_channel_"+str(channel))
    for file in Caixin_GetUrls.yield_file_from_filefold(file_path="./caixin_news/channel_"+str(channel)):
        filename = file.name.split(r'/')[-1]

        if os.path.exists("./caixin_news/Clear_channel_"+str(channel)+"/"+filename):
            continue

        context=file.read()
        begin=context.find(r"content\"")+12
        end=context.find(r"fromchannel\"")-5
        context = context[begin:end]

        #print (remove_html(context))
        with open("./caixin_news/Clear_channel_"+str(channel)+"/"+filename,'w',encoding="utf-8") as outfile:
            outfile.write(remove_html(context))
    print ("SUCCESS : channel ",channel)
        
if __name__=="__main__":
    for i in [129,125,130,131,179,132,126]:
        start_remove(i)
