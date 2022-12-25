import configparser
from faker import Faker
from faker_vehicle import VehicleProvider
import cx_Oracle
from sql import *
from info import *
import datetime as dt
import random
import time
from faker_vehicle import VehicleProvider



fake = Faker('ko-KR')
fake.add_provider(VehicleProvider)

config = configparser.ConfigParser()    
config.read('config.ini', encoding='utf-8') 

config.sections()

db_host = config['oracle_connect_info']['db_host']
db_port = config['oracle_connect_info']['db_port']
db_name = config['oracle_connect_info']['db_name']
db_username = config['oracle_connect_info']['db_username']
db_password = config['oracle_connect_info']['db_password']
insert_row_cnt = int(config['table_info']['insert_row_cnt'])
commit_cnt = int(config['table_info']['commit_cnt'])
owner = config['table_info']['owner'].upper()
table_name = config['table_info']['table_name'].upper()

std_dt = dt.datetime(2021, 1, 1)


try :
    db = cx_Oracle.connect(db_username, db_password, '{}:{}/{}'.format(db_host,db_port,db_name))
    cursor = db.cursor()
    cursor.execute(connection_check_sql)

    row = cursor.fetchone()
    info("I", row[0])
except Exception as e :    
    info("E", e)

cursor.execute(
                table_list_sql.format(
                                        owner=owner,
                                        table_name=table_name
                                        )
                )

rows = cursor.fetchall()

columns = {}

for row in rows :
    columns[row[0]] = [row[1], row[2], row[3], row[4]]

columns = dict(sorted(columns.items()))

insert_column = ""

for k, v in columns.items() :
    insert_column += k + ", "

insert_column = insert_column + "|"
insert_column = insert_column.replace(", |","")


insert_value = ""

for k, v in columns.items() :
    insert_value += ":" + k +  ", "

insert_value = insert_value + "|"
insert_value = insert_value.replace(", |","")

insert_sql = insert_sql.format(
                                    owner=owner,
                                    table_name = table_name,
                                    insert_column = insert_column,
                                    insert_value = insert_value
                                )

def f_fake_val(k,v,start_id,increment_id,insert_row_cnt) :    

    column_name = k

    data_type = v[0]
    data_size = v[1]
    data_length1 = v[2] # data_precision
    data_length2 = v[3] # data_length

    if column_name == "ID" or column_name == "id" :
        return increment_id

    if "VARCHAR" in data_type :
        if 1 == 0 :
            pass
        elif column_name.endswith("CST_NM") :            
            return fake.name()
        elif column_name.endswith("_ID") :            
            return fake.profile()['username']
        elif column_name.endswith("_DT") :            
            return fake.date_between(std_dt).strftime('%Y%m%d')
        elif column_name.endswith("PRD_NM") :            
            return fake.vehicle_make()
        elif column_name.endswith("_EADR") :            
            return fake.email()
        elif column_name.endswith("_HADR") :            
            return fake.address()
        elif column_name.endswith("_JBNM") :            
            return fake.profile()['job']
        elif column_name.endswith("_CMNM") :            
            return fake.profile()['company']
        elif column_name.endswith("_SSN") :            
            return fake.profile()['ssn']
        elif column_name.endswith("_URL") :            
            return fake.profile()['website'][0]
        elif column_name.endswith("_SEX") :            
            return fake.profile()['sex']        
        elif column_name.endswith("_PATH") :            
            return fake.file_path(depth=3)
        else :
            size = random.choice(range(1,data_size))            
            if size > 5 :
                return fake.text(size)
            else :
                return "".join(fake.random_letters(length=size))
    
    elif "NUMBER" in data_type :
        if 1==0 :
            pass
        elif column_name.endswith("_ID") :  
            return fake.pyint(min_value=1, max_value=start_id+insert_row_cnt)          
        elif column_name.endswith("_AGE") :  
            return fake.pyint(min_value=10, max_value=80)          
        elif column_name.endswith("_QTY") :  
            return fake.pyint(min_value=1, max_value=20)          
        elif column_name.endswith("_AMT") :  
            return fake.pyint(min_value=1000, max_value=100000)          
        else :
            return fake.pyint(min_value=0, max_value=int("1".ljust(data_length1-data_length2,'0')))	
    
    elif "DATE" in data_type :
        if 1==0 :
            pass
        elif column_name == "MOD_DTM" :
            return dt.datetime.now()
        elif column_name == "REG_DTM" :
            return fake.date_between(std_dt, dt.datetime.now()-dt.timedelta(1))
        else :
            return fake.date_between(std_dt)

    elif data_type == "CLOB" :

        if 1==0 :
            pass
        elif column_name == "PRD_CNTS" :
            # lob_size = 0.5 * 1024 * 1024 # MB
            lob_size = 100  # Byte
            rate = random.choice([0.2,0.5,0.7,1])
            text_size = fake.pyint(min_value=int(lob_size * rate), max_value=lob_size)
            return fake.text(text_size)
        


cursor.execute(check_start_id.format(owner=owner, table_name=table_name))
row = cursor.fetchone()
start_id = row[0]
increment_id = start_id
info("I", "Last ID : " + str(start_id))
info("I", "Start ID : " + str(start_id+1))


start_time = time.time() 

bulk = []
for i in range(1, insert_row_cnt+1) : 
    
    increment_id += 1

    record = []
    for k, v in columns.items() :
        result = f_fake_val(k,v,start_id,increment_id,insert_row_cnt)
        record.append(result)
    
    bulk.append(record)    

    if i % commit_cnt == 0 :
        cursor.executemany(insert_sql, bulk)
        db.commit()
        info("I", "Commit : " + str(commit_cnt))
        bulk = []
    elif insert_row_cnt == i and insert_row_cnt % commit_cnt != 0 :
        cursor.executemany(insert_sql, bulk)
        db.commit()
        info("I", "Commit : " + str(insert_row_cnt % commit_cnt))


info("I", "Elapsed Time : " + str(round(time.time() - start_time,2)) + " sec")



            











