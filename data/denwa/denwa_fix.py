#!/usr/local/bin/python3
# coding: utf-8

from datetime import datetime
import sys
import os
import cgi
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

dt_now = datetime.now()
presentation = ""


# submitted data read
form = cgi.FieldStorage()
filename_ = form.getvalue('sug_id')
user_ = form.getvalue('user')
wadai_ = form.getvalue('wadai')
hiduke_ = form.getvalue('hiduke')
jikan_ = form.getvalue('jikan')
will_ = form.getvalue('will')
fixer_ = form.getvalue('fixer')
deleter_ = form.getvalue('deleter')
refixer_ = form.getvalue('refixer')

if (fixer_ == "on"):
    start_ = form.getvalue('fix_start')
    end_ = form.getvalue('fix_end')
    kettei_ = "true" + "||" + start_ + "||" + end_
    temp_data = {"user": user_, "wadai": wadai_, "hiduke": hiduke_, "jikan": jikan_, "will": will_, "kettei": kettei_}
    temp_data_json = json.dumps(temp_data, ensure_ascii=False)
    with open(filename_ + ".txt", 'w',encoding='utf-8') as f:
        f.writelines(temp_data_json)
    presentation = """
    write to %s
    日程を確定しました。<br>
    <a href="denwa.py">戻る</a>
    """ % (filename_)
    
    
if (deleter_ == "on"):
    temp_data = {"user": user_, "wadai": wadai_, "hiduke": hiduke_, "jikan": jikan_, "will": will_, "kettei": "died"}
    temp_data_json = json.dumps(temp_data, ensure_ascii=False)
    with open(filename_ + ".txt", 'w',encoding='utf-8') as f:
        f.writelines(temp_data_json)
    presentation = """
    write to %s
    日程を削除しました。<br>
    <a href="denwa.py">戻る</a>
    """ % (filename_)

if (refixer_ == "on"):
    temp_data = {"user": user_, "wadai": wadai_, "hiduke": hiduke_, "jikan": jikan_, "will": will_, "kettei": "false"}
    temp_data_json = json.dumps(temp_data, ensure_ascii=False)
    with open(filename_ + ".txt", 'w',encoding='utf-8') as f:
        f.writelines(temp_data_json)
    presentation = """
    write to %s
    日程を未確定に戻しました。<br>
    <a href="denwa.py">戻る</a>
    """ % (filename_)

print('Content-Type:text/html; charset=UTF-8\n')
print(presentation)
