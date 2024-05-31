import pyodbc
from sqlite3 import DatabaseError
from fastapi.responses import JSONResponse
from line_notify import notify_to_chat

server = "wash.sbcservice.com"
database = "wash"
username = "sbc"
password = "platinum"

def connect(): return pyodbc.connect(f"Driver={'SQL Server'};Server={server};Database={database};Uid={username};Pwd={password}")

"""TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT """

def set_data_new(data):
    franchises_list     = data['franchises'] 
    stations_list       = [] 
    devices_list        = []    
    for franchise in franchises_list:
        stations_list.extend(franchise['stations'])
        for station in franchise['stations']:
            devices_list.extend(station['devices'])
    # print(data['date'])
    if save_to_DB(franchises_list,data['date']):
        # return "Success to fetch data from API"
        print(data['date'], "== > OK.")
    else:
        return "Insert Fail "
def save_to_DB(franchises_list,date): 
    for franchises in franchises_list:
        f = Duplicate_Franchise(franchises)
        f_id = f[0]
        f_name = f[1]
        for station in franchises["stations"]:
            s = Duplicate_Station(f_id,station)
            s_id = s[0]
            s_code = s[1]
            for device in station['devices']:
                d = Duplicate_Device(s_id,device)
                d_id = d[0]
                d_Washer_ID = d[1]
                insert_Daily_WashTransaction(f_id,f_name,s_id,s_code,d_id,d_Washer_ID,device["revenue"],date)

    return "Success to fetch data from API"

"""TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT """

#Duplicate
def Duplicate_Franchise(franchise):
    try:
        with connect() as conn:
            cursor      = conn.cursor()
            sql = f"select id,name from Franchise WHERE Code = '{franchise["id"]}'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                return rows[0][0],rows[0][1]
            else:
                return insert_Franchise(franchise)
    except DatabaseError as e:
        conn.rollback()
        return JSONResponse(content={"DatabaseError": str(e)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        if conn is not None:
            conn.close()
def Duplicate_Station(f_id,station):
    try:
        with connect() as conn:
            cursor      = conn.cursor()
            sql = f"select id,Code from Station WHERE Code ='{station["name"]}' and Franchise = {f_id} "
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                return rows[0][0],rows[0][1]
            else :
                return insert_Station(f_id,station) 
    except DatabaseError as e:
        conn.rollback()
        return JSONResponse(content={"DatabaseError": str(e)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        if conn is not None:
            conn.close()
def Duplicate_Device(s_id,device):
    try:
        with connect() as conn:
            cursor = conn.cursor()
            sql = f"""
                    select id,Washer_ID from WashMachine 
                    WHERE Washer_ID = '{device["name"]}' and station = {s_id}
                """
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.commit()
            if rows:
                return rows[0][0],rows[0][1]
            else :
                return insert_Device(s_id,device) 
    except DatabaseError as e:
        conn.rollback()
        return JSONResponse(content={"DatabaseError": str(e)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        if conn is not None:
            conn.close()   
              
#insert_data
def insert_Franchise(franchise):
    try:
        with connect() as conn:
            cursor      = conn.cursor()          
            sql =f"""
                 INSERT INTO Franchise 
                     (Code, Name, SurName,TimeStempDate,isMaster,Tax)
                 VALUES
                     ('{franchise["id"]}','{franchise["fname"]}','{franchise["lname"]}', GETDATE(),'Y',0)
                 """
            cursor.execute(sql)  
        conn.commit()
        return Duplicate_Franchise(franchise)
    except DatabaseError as e:
        conn.rollback()
        return JSONResponse(content={"DatabaseError": str(e)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        if conn is not None:
            conn.close()
def insert_Station(f_id,station) :
    try:
        with connect() as conn:
            cursor      = conn.cursor()       
            sql =f"""
                 INSERT INTO Station
                     (Code, Name, location,FranChise)
                 VALUES
                     ('{station["name"]}','{station["detail"]}','{station["location"]}',{f_id})
                 """  
            cursor.execute(sql)  
        conn.commit()
        return Duplicate_Station(f_id,station)
    except DatabaseError as e:
        conn.rollback()
        return JSONResponse(content={"DatabaseError": str(e)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        if conn is not None:
            conn.close()
def insert_Device(s_id,device):
    try:
        with connect() as conn:
            cursor      = conn.cursor()       
            sql =f"""
                 INSERT INTO WashMachine
                     (Washer_ID, MAC_Address,Station)
                 VALUES
                     ('{device["name"]}','{device["mac"]}',{s_id})
                 """
            cursor.execute(sql)  
        conn.commit()
        print("Add Device")
        return Duplicate_Device(s_id,device) 
    except DatabaseError as e:
        conn.rollback()
        return JSONResponse(content={"DatabaseError": str(e)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        if conn is not None:
            conn.close()

#WashTransaction            
def insert_Daily_WashTransaction(f_id,f_name,s_id,s_code,d_id,d_Washer_ID,revenue,date):
    if revenue["totalCash"] > 0 or revenue["totalQr"] > 0 or revenue["totalAmount"] > 0  :
       if revenue["cycle"] == 0:
            notify_to_chat(
                f""" ตรวจพบข้อผิดพลาด Wash API (E01) \n
                Detail : valuse = 0 Exception
                Date : {date} \n
                franchise ID : {f_id} {f_name}\n
                station ID : {s_id} {s_code}\n
                device ID : {d_id} {d_Washer_ID}\n  """

       )
    if revenue["totalCash"] is None or revenue["totalQr"] is None or revenue["cycle"] is None:
       notify_to_chat(
            f""" ตรวจพบข้อผิดพลาด Wash API (E02) \n
            Detail : Null Exception
            Date : {date} \n
            franchise ID : {f_id} {f_name}\n
            station ID : {s_id} {s_code}\n
            device ID : {d_id} {d_Washer_ID}\n  """

       )


    try:
        with connect() as conn:
            cursor      = conn.cursor()           
            sql =f"""
                    INSERT INTO WashTransaction 
                        (LogDate,Franchise,Station,WashMachine,AmountCoin_Baht,AmountQRCode_kip,Total_cycle,Date)
                    VALUES 
                        (GETDATE(),{f_id},{s_id},{d_id},{revenue["totalCash"]},{revenue["totalQr"]},{revenue["cycle"]},'{date}')
                 """
            cursor.execute(sql)  
        conn.commit()
    except DatabaseError as e:
        conn.rollback()
        return JSONResponse(content={"DatabaseError": str(e)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    finally:
        if conn is not None:
            conn.close()
