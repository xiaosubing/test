import base64
import hashlib
import time
from io import BytesIO

import ddddocr
import requests
from PIL import Image

req = requests.Session()


headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://qy.chinaunicom.cn',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://qy.chinaunicom.cn/mobile-h5/card/card_list.html',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'uid': '',
}

json_data = {
    'actId': '-1',
    'actName': '卡券列表集合页',
    'pageUrl': 'https://qy.chinaunicom.cn/mobile-h5/card/card_list.html',
    'originalPageUrl': 'https://qy.chinaunicom.cn/mobile-h5/card/card_list.html',
    'fPageUrl': '',
    'pageType': '5',
    'operateName': '',
    'type': '',
    'countType': 1,
    'ip': '',
    'cityName': '',
    'userId': '',
    'channelId': '',
    'source': '3',
    'provinceName': '',
    'operateSystem': '1',
}

response = req.post(
    'https://qy.chinaunicom.cn/mobile/newCommon/saveUserClick',
    params=params,
    headers=headers,
    json=json_data,
)

print("==============================Sid===============")
print(response.text)
sid = response.text
print("==============================Sid===============")

# 获取图片

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://qy.chinaunicom.cn/mobile-h5/card/card_list.html',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Path=/; Path=/; Path=/; acw_tc=276aedef17471419863271125e43c1fa186cf9937c79bef44de662a8c82ea2; CACHE_JSESSIONID=C0FEBC96F22A48D2A96D695976CA8FA4; Hm_lvt_e080bb1a9f98b31badca3d6f6464d7c2=1747141987; HMACCOUNT=5DEB7E923115D747; br-current-appid=3044885f99a241f881835d9b6742b2d0; br-client=4d8d82fa-bff2-4ff3-84b3-4640d273bfd2; SERVERID=fc21778762e7b4ebf4535f11f694aa89|1747143260|1747141986; Hm_lpvt_e080bb1a9f98b31badca3d6f6464d7c2=1747143260; br-session-cache-3044885f99a241f881835d9b6742b2d0=[{"appId":"3044885f99a241f881835d9b6742b2d0","sessionID":"88873e14-46a9-4887-a3e7-edb14f2d6e9d","lastVisitedTime":1747143271385,"startTime":0,"isRestSID":false}]',
}

params = {
    'type': '1',
}

response = req.get('https://qy.chinaunicom.cn/mobile/login/verif/image', params=params,  headers=headers)

backImg = response.json()["shadeImage"]
fontImg = response.json()["cutoutImage"]
yLocal = response.json()["y"]

print("获取到的图片Y坐标：", yLocal)

back = base64.b64decode(backImg)
imgData = BytesIO(back)
img = Image.open(imgData)
img.save("back.png")

icon = base64.b64decode(fontImg)
iconData = BytesIO(icon)
img2 = Image.open(iconData)
img2.save("icon.png")

det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)

with open("back.png", "rb") as f:
    backgroud = f.read()

with open("icon.png", "rb") as f:
    iconpic = f.read()

res = det.slide_match(iconpic, backgroud, simple_target=True)
print(res)
clientX = res["target"][0] / 662



def md5_encrypt(text):
    # 创建 md5 对象
    md5 = hashlib.md5()

    # 更新哈希对象，需要将字符串编码为字节
    md5.update(text.encode('utf-8'))

    # 获取加密后的十六进制字符串
    return md5.hexdigest()

# 获取验证码
timestamp = time.time()
now = int(timestamp * 1000)
strtemp = f"20e78a2{sid}{now}{clientX}{yLocal}132511415251d7838b3ffe73"
print(strtemp)
salt = md5_encrypt(strtemp)
print(salt)

headers = {
    'authority': 'qy.chinaunicom.cn',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'acw_tc=276aede817271915806517390e01ea539f6736b5d28a0e59f9afc9f399a390; CACHE_JSESSIONID=F0E5F68B41DE44038C208EA99C75D436; Hm_lvt_e080bb1a9f98b31badca3d6f6464d7c2=1727191582; HMACCOUNT=FF82D8A7B61D29C5; SERVERID=fc21778762e7b4ebf4535f11f694aa89|1727191680|1727191580; Hm_lpvt_e080bb1a9f98b31badca3d6f6464d7c2=1727191681',
    'origin': 'https://qy.chinaunicom.cn',
    'pragma': 'no-cache',
    'referer': 'https://qy.chinaunicom.cn/mobile-h5/login/login.html?returnUrl=https%3A%2F%2Fqy.chinaunicom.cn%2Fmobile-h5%2Fcard%2FcardNew.html',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest',
}



data = {
    'sid': sid,
    'seq': now,
    'clientX': clientX,
    'clientY': yLocal,
    'phoneNu': '13251141525',
    'businessType': '1',
    's': salt
}
print("----------------")
print(data)
response = req.post('https://qy.chinaunicom.cn/mobile/login/smsCodeNewTow', headers=headers,
                         data=data)
print(response.text)
print(response.status_code)





