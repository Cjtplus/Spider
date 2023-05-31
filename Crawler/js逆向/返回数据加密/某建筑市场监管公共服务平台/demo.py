import execjs
import requests
from Crypto.Cipher import AES

# base_url = r'https://jzsc.mohurd.gov.cn/APi/webApi/dataservice/query/comp/list?'
page = 0
pagesize = 15
total = 450

url = f'https://jzsc.mohurd.gov.cn/APi/webApi/dataservice/query/comp/list?pg={page}&pgsz={pagesize}&total={total}'

header = {
    'Host': 'jzsc.mohurd.gov.cn',
    'Referer': 'https://jzsc.mohurd.gov.cn/data/company',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
cookie = {
    'Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c': '1684746347',
    'Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c': '1684748628',
}

response = requests.get(url, headers=header, cookies=cookie)

print(response.status_code)
print(response.text)

with open(r'demo.js', encoding='utf-8') as f:
    js_code = f.read()
print(js_code)

node = execjs.get()
ctx = node.compile(js_code, cwd=r'C:/Users/cjt/node_modules')  # crypto-js所在绝对路径

json_data = ctx.call('decrypt', response.text)

"""
解决Python execjs 报错
UnicodeDecodeError: 'gbk' codec can't decode byte 0xac in position 62: illegal multibyte sequence

subprocess.py，将参数 encoding=“None” 修改为 encoding=“utf-8” 即可
链接：https://blog.csdn.net/Amber_shi/article/details/114441983
"""

print(json_data)
