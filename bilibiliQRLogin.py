import requests
from urllib import parse
import time,os
from http.cookiejar import MozillaCookieJar
from PIL import Image
from config import logger
import json
class bilibiliQRLogin():
    def __init__(self):
        self.login_session = ''
        self.global_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        #self.qr_login_url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
        self.qr_login_url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
        #self.qr_login_info_url = 'http://passport.bilibili.com/qrcode/getLoginInfo'
        self.qr_login_info_url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/poll'
        self.user_info_url = 'https://api.bilibili.com/x/space/myinfo'
        self.times = 10 # 超时时间 times*5 秒
        self.cookie_path = './cookie.txt'
        self.qr_path = './qr.png'
        self.load_cookie_from_local()
        ##if not self.check_expire():
        ##    self.get_login_session()
        
        
        

    def qr_scan(self):
        ##加header
        h = requests.get(self.qr_login_url,headers=self.global_headers)

        json_data = h.json()

        oauthKey = json_data['data']['qrcode_key']
        qr_image_url = json_data['data']['url']

        self.save_qr_img(qr_image_url)

        return oauthKey
    
    def save_qr_img(self,qr_image_url):
        try:
            import qrcode
            qr_image = qrcode.make(qr_image_url)
            qr_image.save('qr.png')
            return 
        except ImportError:
            logger.waring("本地没有qrcode库,采用api生成二维码")

        try:
            qr_image = requests.get('http://qr.topscan.com/api.php?text='+qr_image_url).content
            with open('qr.png','wb') as f:
                f.write(qr_image)
        except:
            logger.error("网站api失效，无法生成二维码")
            raise Exception("网站api失效，无法生成二维码")

    def get_qr_scan_status(self,oauthKey):
        data = {
            'qrcode_key':oauthKey
        }
        headers = self.global_headers
        headers["Content-Type"]= "application/x-www-form-urlencoded"
        session = requests.Session()
        session.cookies = MozillaCookieJar(self.cookie_path)
        #h = session.post(self.qr_login_info_url,headers=headers,data = data)
        h = session.get(self.qr_login_info_url+'?qrcode_key='+oauthKey,headers=headers)
        status = h.json()['data']['code']
        if status==0:
            return status,session
        else:
            return status,None

    def check_expire(self):
        if not self.login_session:
            return False
        h = self.login_session.get(self.user_info_url,headers=self.global_headers)
        j = h.json()
        if j['code'] == -101:
            return False
        return True


    def get_login_session(self):
        if self.login_session and self.check_expire():
            return self.login_session
        oauthKey = self.qr_scan()
        logger.info("请扫描二维码")
        img = Image.open(self.qr_path)
        img.show()
        for i in range(self.times):
            time.sleep(10)
            status,session = self.get_qr_scan_status(oauthKey)
            if not status:
                logger.info("等待二维码扫描")
            else:
                logger.info("登录成功")
                self.login_session = session
                self.save_cookie_to_local()
                return session
            if i == self.times - 1:
                logger.error('未扫码超时')
                raise TimeoutError("登录超时")
        return None

    def save_cookie_to_local(self):
        self.login_session.cookies.save(ignore_discard=True, ignore_expires=True)
    
    def load_cookie_from_local(self):
        if os.path.exists(self.cookie_path):
            s = MozillaCookieJar(self.cookie_path)
            s.load(self.cookie_path, ignore_discard=True, ignore_expires=True)
            session = requests.Session()
            session.cookies = s
            self.login_session = session
        else:
            pass
    
    def get_cookie(self,name):
        cookies = self.login_session.cookies
        newcookies = {}
        for cookie in cookies:
            newcookies[cookie.name] = cookie.value
        return newcookies[name] if name in newcookies else None
    

if __name__ == "__main__":
    l = bilibiliQRLogin()
    
    







