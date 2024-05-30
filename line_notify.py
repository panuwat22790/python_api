import requests
def notify_to_chat(msg):
    print("notify_to_chat")
    msg = "\n"+msg    
    url     = 'https://notify-api.line.me/api/notify'
    token   = 'lbej8sCNmu7Dpu0w5qvWMdQUjSzVG8nNp0vardwtmuH'
    header  = {'Content-Type':'application/x-www-form-urlencoded','Authorization':f'Bearer {token}'}
    data = {
    "message":msg,
    }
    req = requests.post(url,headers=header,data=data)
    print(req.text)