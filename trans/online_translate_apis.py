import os
import hashlib
import requests


def baidu_fanyi_api(src):
    with open('baidu_api/appid') as f_appid:
        appid = int(f_appid.read())
    with open('baidu_api/key') as f_key:
        key = f_key.read()
    salt = os.urandom(1)[0]
    sign_str = str(appid) + src + str(salt) + key
    m = hashlib.md5()
    m.update(sign_str.encode('utf-8'))
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    response = requests.post(url, params = {
        'q': src,
        'from': 'auto',
        'to': 'zh',
        'appid': appid,
        'salt': salt,
        'sign': m.hexdigest(),
    })
    return response.json()['trans_result'][0]['dst']
