#!/usr/local/bin/python3
# coding: utf-8

from datetime import datetime, date, timedelta
import sys
import os
import cgi
import io
import json
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def sugg_is_not_passed(info_):
    if "true" not in info_['kettei']:
        return -1
    temp_ = info_['hiduke'] + " " +  info_['kettei'].split("||")[1] + ":00"
    try:
        temp_endtime = datetime.strptime(temp_, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return -1
    if temp_endtime > datetime.now():
        return 1
    else:
        return -1

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

dt_now = datetime.now()



# submitted data read
form = cgi.FieldStorage()
user_ = form.getvalue('user')
wadai_ = form.getvalue('wadai')
hiduke_ = form.getvalue('hiduke')
jikan_ = form.getvalue('jikan')
will_ = form.getvalue('will')
kettei_ = "false"
temp_data = {"user": user_, "wadai": wadai_, "hiduke": hiduke_, "jikan": jikan_, "will": will_, "kettei": kettei_}
temp_data_json = json.dumps(temp_data, ensure_ascii=False)
# submitted data read

save_path = "log/" + dt_now.strftime('%Y%m')
if not os.path.exists(save_path):
    os.mkdir(save_path)

# save submitted data
if not user_ is None:
    with open(save_path + "/"+ dt_now.strftime('%Y%m%d%H%M%S') +"_"+ str(user_) + '.txt', 'w',encoding='utf-8') as f:
        f.writelines(temp_data_json)
# save submitted data


# show existing data  # 変更があったときのcgiは別のファイルに飛ぶように
with open('existing_denwa.html', 'r', encoding='utf-8') as f:
    existing_template = f.read()
with open('existing_denwa_fixed.html', 'r', encoding='utf-8') as f:
    existing_fixed_template = f.read()


# 2回繰り返ししたい
existing_presentations = ""
sug_list = []
file_list = [f for f in os.listdir(save_path) if ".txt" in f]
file_list = sorted(file_list, key=natural_keys, reverse=True)
for sug_ in file_list:
    with open(save_path + "/" + sug_, 'r', encoding='utf-8') as f:
        temp_sugg_info = json.load(f)
        if (not temp_sugg_info["user"] is None and temp_sugg_info["kettei"] == "false"):
            sug_list.append(save_path + "/" + sug_)
        elif temp_sugg_info["kettei"] != "died":
            if sugg_is_not_passed(temp_sugg_info) == 1:
                sug_list.append(save_path + "/" + sug_)
    if len(sug_list) >= 2:
        break

if len(sug_list) < 2:
    save_path_ = "log/" + (dt_now- timedelta(days=28)).strftime('%Y%m')
    if os.path.exists(save_path_):
        file_list = [f for f in os.listdir(save_path_) if ".txt" in f]
        file_list = sorted(file_list, key=natural_keys, reverse=True)
        for sug_ in file_list:
            with open(save_path_ + "/" + sug_, 'r', encoding='utf-8') as f:
                temp_sugg_info = json.load(f)
                if temp_sugg_info["kettei"] == "false":
                    sug_list.append(save_path_ + "/" + sug_)
                elif temp_sugg_info["kettei"] != "died":
                    if sugg_is_not_passed(temp_sugg_info) == 1:
                        sug_list.append(save_path_ + "/" + sug_)
            if len(sug_list) >= 2:
                break

# "kettei"={false/true/died}||{start}||{end}
# filename = "20220223164148_shogo.txt"
for sug_top in sug_list:
    filename = sug_top

    with open(filename, encoding='utf-8') as f:
        sugg_info = json.load(f)
    sug_id = filename.split('.')[0]

    if (sugg_info["kettei"].split("||")[0] == "true"):
        args_ = (sug_id, sugg_info["user"], sugg_info["hiduke"], sugg_info["will"], sugg_info["wadai"], sugg_info["jikan"], sugg_info["kettei"].split("||")[1], sugg_info["kettei"].split("||")[2])
        existing_presentation = existing_fixed_template % args_
    else:
        args_ = (sug_id, sugg_info["user"], sugg_info["hiduke"], sugg_info["will"], sugg_info["wadai"], sugg_info["jikan"])
        existing_presentation = existing_template % args_
    existing_presentations += existing_presentation

# show existing data








presentation = ""
with open('denwa.html', 'r', encoding='utf-8') as f:
    html_body = f.read()
presentation += html_body % (existing_presentations)


print('Content-Type:text/html; charset=UTF-8\n')
print(presentation)
