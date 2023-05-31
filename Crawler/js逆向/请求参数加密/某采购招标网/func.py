import io
import re
import pandas as pd
from config import url_base
from pyquery import PyQuery as pq


def remove_annotation(code):
    ret = ''
    length = len(code)
    i = 0
    flag = 0
    while i < length:
        next_code = ''
        if i < length - 1:
            next_code = code[i + 1]
        if flag == 0 and code[i] == '/' and next_code == '/':
            break
        elif flag == 0 and code[i] == '/' and next_code == '*':
            flag = 1
            i = i + 1
        elif flag == 1 and code[i] == '*' and next_code == '/':
            flag = 0
            i = i + 1
        elif flag == 1:
            i = i + 1
            continue
        else:
            ret = ret + code[i]
        i = i + 1
    return ret


def string_contains(text, token):
    ret = False
    for i in range(len(text)):
        if token == text[i]:
            ret = True
            break
    return ret


def strip_token(code, token_list):
    ret = ''
    for i in range(len(code)):
        if string_contains(token_list, code[i]) is False:
            ret = ret + code[i]
    return ret


def parser_qt(text):
    f = io.StringIO(text)
    content = []
    locate_caigou8 = False
    while True:
        line = f.readline()
        if not line:
            break
        else:
            if locate_caigou8 is False and "0!caigou8" in line:
                locate_caigou8 = True
            if locate_caigou8:
                if "success" in line:
                    break
                t = line.strip()
                t = remove_annotation(t)
                if len(t) > 0:
                    content.append(t)
    length = len(content)
    qt = strip_token(content[2], "'+") + strip_token(content[3], "'+")
    return qt


def parse_content(content):
    content = pq(content)
    table_data = content('table.zb_result_table')
    trs = table_data('tr')
    unit = []
    notice = []
    title = []
    web_time = []
    title_url = []
    for tr in trs.items():
        title_id = tr.attr('onclick')
        if title_id is None:
            pass
        else:
            tid = re.findall(r"selectResult\((.*?)\)", title_id)[0]
            tid_url = url_base + eval(tid)
            title_url.append(tid_url)
        tds = tr('td')
        td_text = []
        for td in tds.items():
            if td.text() is None or td.text() == '采购需求单位':
                break
            else:
                td_text.append(td.text())
        if len(td_text) > 1:
            # print(td_text)
            unit.append(td_text[0])
            notice.append(td_text[1])
            title.append(td_text[2])
            web_time.append(td_text[3])
        else:
            continue

    dic = {
        '采购需求单位': unit,
        '公告类型': notice,
        '标题': title,
        '时间': web_time,
        '链接': title_url
    }
    df = pd.DataFrame.from_dict(dic)

    return df
