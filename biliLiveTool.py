import requests

#获取用户名
def getUserInfo(session):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    r = requests.get('https://api.live.bilibili.com/User/getUserInfo',cookies=session.cookies,headers=headers)
    if r.json()['code']=='REPONSE_OK':
        return  r.json()['data']['uname']
    
#添加屏蔽词
def add_live_word_req(roomid,keyword,session,csrf):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    url ="https://api.live.bilibili.com/xlive/web-ucenter/v1/banned/AddShieldKeyword"
    if keyword!="":
        data={
            "room_id": roomid,
            "keyword":keyword,
            "csrf_token":csrf,
            "csrf":csrf
        }
        r = session.post(url,data=data,headers=headers)
    return r.json()["code"],r.json()["message"]


#添加屏蔽词
def remove_live_word_req(roomid,keyword,session,csrf):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    url ="https://api.live.bilibili.com/xlive/web-ucenter/v1/banned/DelShieldKeyword"
    if keyword!="":
        data={
            "room_id": roomid,
            "keyword":keyword,
            "csrf_token":csrf,
            "csrf":csrf
        }
        r = session.post(url,data=data,headers=headers)
    return r.json()["code"],r.json()["message"]