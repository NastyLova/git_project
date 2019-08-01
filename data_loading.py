import logging
import configparser
import pyodbc
import datetime


logfile = 'D:/data_loading/log/log'+datetime.datetime.now().strftime("%Y%m%d_%H%M")+'.txt'
logging.basicConfig(filename=logfile,format='%(asctime)s:%(message)s',level=logging.INFO)


config = configparser.ConfigParser()
try:
    config.read('D:\\data_loading\\ini.txt')
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

#clients_file = 'D:\\'+datetime.datetime.now().strftime("%d%m%Y")+'_blank.csv'
#orders_file = 'D:\\'+datetime.datetime.now().strftime("%d%m%Y")+'_blank.csv'
clients_file = 'D:\\19072019_blank.csv'
orders_file = 'D:\\19072019_blank.csv'

if __name__ == '__main__':
    with open(orders_file, encoding='utf-8', newline='') as reader_1:
        orders = [line.split(',"') for line in reader_1.readlines()]
        orders[0][0] = orders[0][0].replace('\ufeff', '')
        for i in orders:
            i[-1] = i[-1].strip()
        orders = [[c.strip('"') for c in i] for i in orders]

    with open(clients_file, encoding='utf-8', newline='') as reader_2:
        clients = [line.split('","') for line in reader_2.readlines()]
        clients[0][0] = clients[0][0].replace('\ufeff', '')
        for i in clients:
            i[-1] = i[-1].strip()
        clients = [[c.strip('"') for c in i] for i in clients]
        

    
    r = cursor.execute("SELECT COLUMN1 FROM TABLE1 WHERE ENABLED = 1").fetchall()
    cl = [] #преобразование из кортежа в список id
    for c in r:
        cl += [l for l in c]
    #print(cl)
    
    for client in clients:
        client_id = client[0]
        sa_clientid = client[20]
        #print(len(client),len(sa_clientid))

        if sa_clientid not in cl: # поиск айди клиента из файла в базе
            try:
                cursor.execute("INSERT INTO TABLE1(COLUMN2,NAME,NAME1,NAME2,COLUMN3,DOC1,DOC2,DOC3,DOC4,COLUMN4,"
                               "COLUMN5,COLUMN6,COLUMN7,COLUMN8,DOC5,ENABLED,COLUMN9,DATETIME,COLUMN10,COLUMN1)"
                               "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", client[1:-5])
                logging.info('Client anket {} had been loaded! Downloaded {} clients!'.format(client_id,len(client_id)))
            except pyodbc.ProgrammingError as e: # Если нет договоров у клиента в файле
                logging.info('Client id:{} such client exists!'.format(client_id))
        new_id = cursor.execute("SELECT TOP 1 ID FROM TABLE1 ORDER BY ID DESC").fetchone()
    
        deals = [o for o in orders if o[17] == sa_clientid]

        number = cursor.execute("SELECT COLUMN11 FROM TABLE2 WHERE ENABLED = 1").fetchall()
        
        if cl.count(client_id) == 0: # клиент есть в базе
            for deal in deals:
                deal[17] = new_id # обновляем значение clientid для договора
                #print(len(deal))

        # записываем договоры в базу    
        try:
            if orders[:][6] not in number:
                cursor.executemany('''INSERT INTO TABLE2(TCOLUMN1,TCOLUMN2,ENABLED,TCOLUMN3,TCOLUMN4,TCOLUMN5,TCOLUMN6,DATETIME,TCOLUMN7,TCOLUMN8,TCOLUMN9,DATETIME2,TCOLUMN10,
                                   TCOLUMN11,TCOLUMN12,TCOLUMN13,COLUMN2,COLUMN1)
                                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', deals)
                logging.info('Orders by client {} had been loaded! Downloaded {} orders!'.format(client_id,len(deals)))
            else:
                logging.info('Orders by client {}'.format(client_id))
        except pyodbc.ProgrammingError as e: # Если нет договоров у клиента в файле
            logging.info('Such loan already exists'.format(client_id))
    logging.info('Logging completed successfully.')
    logging.info('Downloaded {} orders!'.format(len(deals)))
    logging.info('Downloaded {} clients!'.format(len(new_id)))
cnxn.commit()
cursor.close()
print('Success!')

