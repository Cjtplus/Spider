import base64
import hashlib
import json
import time
import requests

from Crypto.Cipher import AES
from Crypto.Hash import MD5
from jsonpath import jsonpath


def get_response(translate_content):
    url = r'https://dict.youdao.com/webtranslate'
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    cookie = {
        'OUTFOX_SEARCH_USER_ID_NCOO': '1681190046.2294936',
        'OUTFOX_SEARCH_USER_ID': '-1523131004@183.6.158.122'
    }

    stamp_time = str(int(time.time()))

    sign = f'client=fanyideskweb&mysticTime={stamp_time}&product=webfanyi&key=fsdsogkndfokasodnaso'
    hl = hashlib.md5()
    hl.update(sign.encode(encoding='utf-8'))
    sign = hl.hexdigest()

    # translate_content = input('请输入要翻译的内容：')

    data = {
        'i': translate_content,
        'from': 'auto',
        'to': '',
        'dictResult': 'true',
        'keyid': 'webfanyi',
        'sign': sign,
        'client': 'fanyideskweb',
        'product': 'webfanyi',
        'appVersion': '1.0.0',
        'vendor': 'web',
        'pointParam': 'client,mysticTime,product',
        'mysticTime': stamp_time,
        'keyfrom': 'fanyi.web'
    }

    response = requests.post(url=url, headers=header, cookies=cookie, data=data)

    return response.text


def decode_response(text):
    key = b"ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
    iv = b"ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"
    cryptor = AES.new(MD5.new(key).digest()[:16], AES.MODE_CBC, MD5.new(iv).digest()[:16])
    res = cryptor.decrypt(base64.urlsafe_b64decode(text))
    txt = res.decode("utf-8")
    return json.loads(txt[: txt.rindex("}") + 1])


def get_translate(json_data):
    translate = jsonpath(json_data, '$..tgt')
    translate_expand_text = jsonpath(json_data, '$..#text')
    translate_expand_tran = jsonpath(json_data, '$..#tran')

    if translate_expand_text:

        if len(translate_expand_text) > 1:
            print('\n翻译：\n', f'{translate[0]}\n', f'\n拓展：')
            for i in range(len(translate_expand_text)):
                print(f'{translate_expand_text[i]}\n', f'{translate_expand_tran[i]}\n')
        else:
            print('\n翻译：\n',
                  f'{translate[0]}\n',
                  f'\n拓展：',
                  f'{translate_expand_text[0]}\n',
                  f'{translate_expand_tran[0]}\n')
    else:
        print('\n翻译：\n', f'{translate[0]}\n')


def run_crawl():
    while True:
        translate_content = input('请输入要翻译的内容：\n')
        response = get_response(translate_content)
        text = decode_response(response)
        get_translate(text)

        exit_or_not = eval(input('是否继续？（输入1继续，输入0退出）\n'))
        if exit_or_not:
            continue
        else:
            break


if __name__ == '__main__':
    run_crawl()
