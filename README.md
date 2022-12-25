# Purpose
Create `Mock Data` to `Oracle Table`

# requierments
```
cx-Oracle==8.3.0
Faker==15.3.3
faker-vehicle==0.2.0
python-dateutil==2.8.2
six==1.16.0
typing_extensions==4.4.0
```

# install
```bash
pip install -r requierments.txt
```

# config
Create `config.ini` file in your project root.
```
[oracle_connect_info]
db_host = X.X.X.X
db_port = 1521
db_name = orcl
db_username = obj_own
db_password = obj_own

[table_info]
total_row_cnt = 1000
commit_cnt = 100
owner = OBJ_OWN
table_name = TEST
```

# example table
```sql
CREATE TABLE OBJ_OWN.TEST
(
ID int,
USER_PRNM VARCHAR(10),
USER_AGE NUMBER,
USER_EADR VARCHAR(100),
USER_HADR VARCHAR(300),
USER_JBNM VARCHAR(300),
USER_CMNM VARCHAR(300),
USER_AMT NUMBER,
USER_QTY NUMBER,
USER_SSN VARCHAR(300),
USER_URL VARCHAR(300),
USER_SEX VARCHAR(300),
USER_URID VARCHAR(300),
USER_PATH VARCHAR(100),
REG_DTM DATE,
MOD_DTM DATE
) TABLESPACE USERS;
CREATE UNIQUE INDEX OBJ_OWN.TEST_PK ON OBJ_OWN.TEST (ID) TABLESPACE USERS;
```

# testing
```bash
$ python mock_data.py
## Info :  DB Connected
## Info :  Start ID : 1
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Commit : 100
## Info :  Elapsed Time : 3.33 sec
$
```

# result
```sql
SELECT *
FROM OBJ_OWN.TEST;
```
![image](img/grid.png)