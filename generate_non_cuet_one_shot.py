import MySQLdb
hostname = 'localhost'
username = 'djshaji'
password = 'jennahaze'
database = 'noncuet'

import pandas, sys, pprint

myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
cur = myConnection.cursor()

def allotted (filename, course):
    f = open (filename).read ().split ("\n")
    for a in f:
        if a == "":
            continue
        sql = f'update `{course}` set list = {filename [-1]} where Registration_no = {a}'
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
        course = ""
        for row in rows:
            # ~ print (k, rows.keys ()[k], row)
            data [rows.keys () [k]] = row
            if k == 2:
                course = row
            cols += "`" + rows.keys () [k] + "`"
            vals += "'" + str (row).replace ("'", "") + "'"
            
            k += 1
            if k < l:
                cols += ','
                vals += ','
            else:
                cols += ')'
                vals += ')'
        
        # ~ exit ()
        sql = f"insert into `{course}` {cols} values {vals}"
        print (f'{course}: {current}')

        try:
            cur.execute (sql)
        except Exception as e:
            print (e)
            if not str (e).startswith ('(1062, "Duplicate entry'):
                print (rows)
                exit ()
        
        current += 1
    myConnection.commit ()

# ~ for a in sys.argv [1:]:
    # ~ insert (a)

# ~ allotted (sys.argv [1])

def merit (course, total, _list):
    data = []
    merit_list = []
    
    sql = f"select * from `{course}` where programme_name = '{course}' and list is null ORDER by XIIBEST5 desc"
    
    cur.execute (sql)
    data = cur.fetchall ()
    
    print (f'{len (data)} -> {total}:', sql)

    merit_list = list (data [:total])
    x = len (merit_list)
    
    if x < len (data):
        while data [x][24] == merit_list [-1][24]:
            merit_list.append (data [x])
            x += 1
            if x == len (data):
                break
        
    for m in merit_list:
        print (m [1], m[2], m[3], m[24])
        sql = f'update `{course}` set list = {_list} where Registration_no = {m[1]}'
        print (sql)
        try:
            cur.execute (sql)
        except Exception as e:
            print (e)
            exit ()
        
    myConnection.commit ()

merit (sys.argv [1], int (sys.argv [2]), int (sys.argv [3]))
# ~ for filename in sys.argv [1:]:
    # ~ insert (filename)
# ~ allotted (sys.argv [1], sys.argv [2])
