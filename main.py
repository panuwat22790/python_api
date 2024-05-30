import requests
from fastapi import FastAPI,HTTPException
from dbconn import set_data_new
from datetime import datetime, timedelta
from pathlib import Path
from line_notify import notify_to_chat
app = FastAPI()
headers = {
    'secret': 'e1df1585902df22b9f664380adc8ab34',
    'session': '{"username":"krt.service2023@gmail.com","key":"c81e728d9d4c2f636f067f89cc14862c", "role": "api"}'}

Path = str(Path(__file__).parent.resolve())

@app.get("/api/wash_project/")
async def root():
    print(f"Date Now  {datetime.now()}")
    return {"massage":f"{datetime.now().year, datetime.now().month,datetime.now().day}"}

@app.get("/api/wash_project/all")
async def read_root():
    # กำหนดวันที่เริ่มต้น
    start_date = datetime(2024,2, 1)

    # วันที่ปัจจุบัน
    end_date = datetime.now()

    # วนลูปและพิมพ์วันที่ตั้งแต่เริ่มต้นจนถึงปัจจุบัน
    current_date = start_date
    
    while current_date <= end_date:
        dateNow = current_date.strftime("%Y-%m-%d")
        try:
            url = f"https://api.tnjtek.com/v1/partner/salesDaily?date={dateNow}"
            response = requests.get(url,headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                current_date += timedelta(days=1)
                set_data_new(data)     
            else:
                return "Failed to fetch data from API"  # ร้องขอไม่สำเร็จ
        except requests.exceptions.ConnectTimeout:
            notify_to_chat(""" Wash_API : \n status_code=504, detail="Connection to the external API timed out." """)
            raise HTTPException(status_code=504, detail="Connection to the external API timed out.")
        except requests.exceptions.HTTPError as e:
            notify_to_chat(f""" Wash_API : \n status_code={response.status_code}, detail={str(e)} """)
            raise HTTPException(status_code=response.status_code, detail=str(e))
        except requests.exceptions.RequestException as e:
            notify_to_chat(f""" Wash_API : \n status_code={response.status_code}, detail={str(e)} """)
            raise HTTPException(status_code=500, detail=str(e))
    return 200 ,"Success all data "

@app.get("/api/wash_project/salesDaily")
async def read_root():
    dateNow = datetime.now()
    yesterday = ""
    
    if dateNow.day == 1:
        first_day_of_this_month = dateNow.replace(day=1)
        last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
        yesterday = last_day_of_last_month
    else:
        yesterday = dateNow - timedelta(days=1)
        
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    try:
        url = f"https://api.tnjtek.com/v1/partner/salesDaily?date={yesterday_str}"
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            set_data_new(data)
        else:
            return "Failed to fetch data from API"  # ร้องขอไม่สำเร็จ
        
    except requests.exceptions.ConnectTimeout:
        notify_to_chat(""" Wash_API : \n status_code=504, detail="Connection to the external API timed out." """)
        raise HTTPException(status_code=504, detail="Connection to the external API timed out.")
    except requests.exceptions.HTTPError as e:
        notify_to_chat(f""" Wash_API : \n status_code={response.status_code}, detail={str(e)} """)
        raise HTTPException(status_code=response.status_code, detail=str(e))
    except requests.exceptions.RequestException as e:
        notify_to_chat(f""" Wash_API : \n status_code={response.status_code}, detail={str(e)} """)
        raise HTTPException(status_code=500, detail=str(e))
    return 200 ,"Success all data "

@app.get("/api/wash_project/test")
async def read_root():
    dateNow = datetime(2024,5,3).strftime("%Y-%m-%d")
    try:
        url = f"https://api.tnjtek.com/v1/partner/salesDaily?date={dateNow}"
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            return {"data":data}
        else:
            return "Failed to fetch data from API"
    except requests.exceptions.ConnectTimeout:
        notify_to_chat(""" Wash_API : \n status_code=504, detail="Connection to the external API timed out." """)
        raise HTTPException(status_code=504, detail="Connection to the external API timed out.")
    except requests.exceptions.HTTPError as e:
        notify_to_chat(f""" Wash_API : \n status_code={response.status_code}, detail={str(e)} """)
        raise HTTPException(status_code=response.status_code, detail=str(e))
    except requests.exceptions.RequestException as e:
        notify_to_chat(f""" Wash_API : \n status_code={response.status_code}, detail={str(e)} """)
        raise HTTPException(status_code=500, detail=str(e))
# 
