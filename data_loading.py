import logging
import configparser
import pyodbc

config = configparser.ConfigParser()
try:
    config.read('D:\\test\\ini.txt')
except Exception as e:
    logging.info(e)

server = config['Default']['server']
database = config['Default']['database']
username = config['Default']['username']
password = config['Default']['password']

conn_str = ('DRIVER={SQL Server}' +
            ';SERVER=' + server +
            ';DATABASE=' + database +
            ';UID=' + username +
            ';PWD=' + password)

cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()

clients_file = 'D:\\data_loading\\clients.csv'
orders_file = 'D:\\data_loading\\orders.csv'

def get_table_by_file(filename):
    with open(filename, encoding='utf-8', newline='') as reader_1:
        table = [line.split(';') for line in reader_1.readlines()]
        return [[cell.strip() for cell in line] for line in table]
        

def get_clients_id_from_db(cursor):
    r = cursor.execute("SELECT ID FROM CLIENTS WHERE ENABLED = 1").fetchall()
    return [c[0] for c in r]

def write_client_to_db(client,cursor):
    cursor.execute("INSERT INTO CLIENTS(FULLNAME,BIRTHDATE,DOCS,DOCNUM,DOCBEGINDATE,DOCCONTENT,ADDRESS_REG,ADDRESS_FACT,PHONE,MOBILEPHONE,BIRTHPLACE,DOCCODE,ENABLED,OLDNAME,CREATIONDATETIME,USERID)"
                           "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", client[1:])

def get_last_client_id(cursor):
    return cursor.execute("SELECT TOP 1 ID FROM CLIENTS ORDER BY ID DESC").fetchone()[0]


if __name__ == '__main__':

    orders = get_table_by_file(orders_file)
    orders[0][0] = orders[0][0].replace('\ufeff', '')
    for i in orders:
        i[1] = float(i[1])
        i[7] = float(i[7])
        i[11] = float(i[11])
        i[12] = float(i[12])
        i[13] = float(i[13])
        i[8] = int(i[8])
        i[-1] = i[-1].strip()

    clients = get_table_by_file(clients_file)
    for i in clients:
        i[0] = int(i[0])
        i[-1] = i[-1].strip()

    clients_id = get_clients_id_from_db(cursor)

    for client in clients:
        client_id = client[0]
        deals = [o for o in orders if o[8] == client_id]

        if client_id not in clients_id:
            write_client_to_db(client,cursor)
            new_id = get_last_client_id(cursor)
            for deal in deals:
                deal[8] = new_id # обновляем значение clientid для договора

        # записываем договоры в базу            
        try:
            cursor.executemany("INSERT INTO ORDERS(DAYSQUANT,LOANCOSTALL,ENABLED,WORKNAME,WORKADDRESS,WORKPROF,NUMBER,CREATIONDATETIME,CLIENTID,USERID,ORDERSTATUS,PUTDATETIME,PERCENTCOSTALL,LOANRESTCOSTALL,INFO,MAINPERCENT,FULLNAME)"
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", deals)
            print('Orders by client {0} has been loaded! Downloaded {1} orders!'.format(client_id,len(deals)))
            cnxn.commit()
        except pyodbc.ProgrammingError as e: # Если нет договоров у клиента в файле
            print('Client id:{} has not orders!'.format(client_id))

    
    cursor.close()
    cnxn.close()

