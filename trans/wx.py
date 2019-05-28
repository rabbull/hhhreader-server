import requests


def get_openid(app_id: str, app_secret: str, js_code: str):
    openid = requests.get('https://api.weixin.qq.com/sns/jscode2session', {
        # appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
        'appid': app_id,
        'secret': app_secret,
        'js_code': js_code,
        'grant_type': 'authorization_code'
    }).json()['openid']
    return openid
