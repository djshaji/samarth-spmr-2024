import MySQLdb
hostname = 'localhost'
username = 'djshaji'
password = 'jennahaze'
database = 'noncuet'

import pandas, sys, pprint

myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
cur = myConnection.cursor()

def allotted (filename):
    f = open (filename).read ().split ("\n")
    for a in f:
        if a == "":
            continue
        sql = f'update admission set list = 2 where Registration_no = {a}'
        print (sql)
        try:
            cur.execute (sql)
        except Exception as e:
            print (e)
        
    myConnection.commit ()
    
    
def insert (filename):  
    xl = pandas.read_excel (filename, engine = "openpyxl")
    current = 0
    for index, rows in xl.iterrows():
        data = dict ()
        k = 0
        cols = "("
        vals = "("
        
        l = len (rows)
        
        for row in rows:
            # ~ print (rows.keys ()[k], row)
            data [rows.keys () [k]] = row
            cols += "`" + rows.keys () [k] + "`"
            vals += "'" + str (row).replace ("'", "") + "'"
            
            k += 1
            if k < l:
                cols += ','
                vals += ','
            else:
                cols += ')'
                vals += ')'
        
        sql = f"insert into admission {cols} values {vals}"
        print (f'file: {current}')

        try:
            cur.execute (sql)
        except Exception as e:
            print (e)
        
        current += 1
    myConnection.commit ()

# ~ for a in sys.argv [1:]:
    # ~ insert (a)

# ~ allotted (sys.argv [1])

def merit (course, total):
    data = []
    merit_list = []
    
    sql = f"select * from admission where programme_name = '{course}' and list is null ORDER by XIIBEST5 desc"
    
    cur.execute (sql)
    data = cur.fetchall ()
    
    print (f'{len (data)} -> {total}:', sql)

    merit_list = list (data [:total])
    x = len (merit_list)
    
    while data [x][24] == merit_list [-1][24]:
        merit_list.append (data [x])
        x += 1
        
    for m in merit_list:
        print (m [1], m[2], m[3], m[24])

merit (sys.argv [1], int (sys.argv [2]))
