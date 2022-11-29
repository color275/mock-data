from faker import Faker
fake = Faker('ko-KR')
import cx_Oracle

import datetime as dt
from random import choice

import sys

import random

table_name = sys.argv[1].upper()
pk = sys.argv[2].upper()
spk = sys.argv[3].upper()
ind = int(sys.argv[4])
total_cnt = int(sys.argv[5])
in_cnt = int(sys.argv[6])

cnt = int(total_cnt/in_cnt)

start_dt = dt.datetime(2021, 1, 1)
start_sdt = '2021-01-01'

def f_fake_val(column_name, data_type, data_length, data_precision, data_scale, ind, seq) :    
    if column_name == pk :
        return ind

    if column_name == spk :
        return seq
    
    if data_type == "CLOB" and column_name == "PRD_INFO" :
        text = ""
        i = 0
        while i < 100 :
            text = text + fake.catch_phrase() 
            i = i + 1        
        return text

    if data_type == 'DATE' :
        return fake.date_between(start_dt)
    if data_type == 'NUMBER' :
        if column_name[-4:] == "_AMT" :
            return round(fake.pyint(min_value=1000, max_value=1000000),-2)
        else :
            return fake.pyint(min_value=0, max_value=int("1".ljust(data_precision-data_scale,'0')))	
    
    if data_type[0:3] == 'VAR' :
        if column_name == 'NAME' :
            return fake.name()[0:data_length]        
        elif pk != "CST_ID" and column_name == "CST_ID" :
            return fake.pyint(min_value=1, max_value=100000)
        elif pk != "PRD_ID" and column_name == "PRD_ID" :
            return fake.pyint(min_value=1, max_value=100000)	            	            
        elif column_name == "IMG_PATH" :
            return fake.file_path(depth=3, category='image')
        elif column_name == "PRD_NM" :
            return fake.catch_phrase()[0:data_length]        
        elif column_name == "ADDRESS" :
            return fake.address()
        elif column_name == "POSTCODE" :
            return fake.postcode()
        elif column_name == "COUNTRY" :
            return fake.country()
        elif column_name == "JOB" :
            return fake.job()
        elif column_name[-3:] == "_CD" :
            return fake.text()[0:4].upper().replace(" ","")
        elif column_name == "EMAIL" :
            return fake.email()
        elif column_name == "PHONE" :
            return fake.phone_number()
        elif column_name == "PASSWORD" :
            return fake.text()[0:data_length].lower().replace(" ","")
        elif column_name == "BIRTH" :
            return fake.date_between(dt.datetime(1960, 1, 1)).strftime('%Y%m%d')
        elif column_name[-4:] == "_SEQ" :
            return fake.pyint(min_value=0, max_value=4)	
        elif column_name[-3:] == "_ID" :
            return fake.pyint(min_value=0, max_value=1000000)	
        elif column_name[-3:] == "_DT" :
            return fake.date_between(start_dt).strftime('%Y%m%d')
        elif column_name[-3:] == "_YM" :
            return fake.date_between(start_dt).strftime('%Y%m%d')[0:6]
        elif column_name[-5:] == "_TIME" :
            return fake.time().replace(":","")
        elif column_name[-3:] == "_YN" :
            return choice(['Y', 'N'])
        else :
            return fake.text()[0:data_length]




db = cx_Oracle.connect('dms_own', 'dms_own', '13.124.42.125:1521/orcl')
cursor = db.cursor()


sql = """
select column_name, data_type, data_length, data_precision, data_scale
from all_tab_columns where table_name = '{table_name}'
""".format(table_name = table_name)


cursor.execute(sql)

data_type = []
column_type = {}
for row in cursor :
#     print(row)
    data_type.append(row[1])
    column_type[row[0]] = [row[1], row[2], row[3], row[4]]

column_type = dict(sorted(column_type.items()))

columns = ""
for k, v in column_type.items() :
    columns += k + ", "

columns = columns + "|"    
columns = columns.replace(", |", "")
# columns

v_columns = ""
for k, v in column_type.items() :
    v_columns += ":" + k + ", "

v_columns = v_columns + "|"    
v_columns = v_columns.replace(", |", "")
# v_columns

sql_insert = """INSERT INTO {TABLE_NAME} ( {COLUMNS} )
VALUES
(
{V_COLUMNS}
)""".format(
    TABLE_NAME = table_name,
    COLUMNS = columns,
    V_COLUMNS = v_columns
)
# sql_insert


import time
start = time.time() 


for i in range(1,cnt+1) :
    bulk = []
    for j in range(1,in_cnt+1) :

        seq = 1

        if spk == "NONE" :
            random_seq = 1
        else :
            random_seq = random.randrange(1,8)
        while seq <= random_seq :
            val = []
            for k, v in column_type.items() :
                result = f_fake_val(k, v[0], v[1], v[2], v[3], ind, seq)
                val.append(result)
            
            bulk.append(val)
            
            seq = seq + 1
        
        ind = ind + 1
        
#         print("{k} : {dt} : {vv}".format(k=k, dt=v[0], vv=result))
    cursor.executemany(sql_insert, bulk)
    db.commit()


print("################################")
print("## " +table_name)
print("time :", time.time() - start)  
print("last index : " + str(ind) )
print("################################")
