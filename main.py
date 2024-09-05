import pandas, sys, pprint
mapping = {
    "General": "gen",
    "Economically Weaker Sections (EWS)": "ews-sup",
    "Schedule Caste (SC)": "sc",
    "Other Backward Classes": "OBC",
    "Resident of Backward Area(RBA)": "rba",
    "Scheduled Tribes-2": "st2",
    "Scheduled Tribes-1": "st1",
    "Residents of areas adjoining line of actual control (ALC)/ International Border(IB)": "alc/ib",
    "Residents of Backward Area (RBA)": "rba",
    "Scheduled Tribes (ST)": "st1"
}

def check_commerce (data):
    for d in data:
        if str (data [d]).upper () == "ACCOUNTANCY":
            return True
    
    # ~ print (data)
    # ~ print (False)
    # ~ exit ()
    return False

alloted = dict ()
intake = dict ()

selected_course = sys.argv [1]
xl = pandas.read_excel (sys.argv [2], engine = "openpyxl")
for index, rows in xl.iterrows():
    course = rows [3]
    intake [course] = dict ()
    for x in range (len (rows)):
        intake [course][rows .keys ()[x]] = rows [x]
    
category_wise_intake = dict ()
for i in intake:
    if not i in category_wise_intake:
        category_wise_intake [i] = dict ()
    
    category_wise_intake [i]["Intake"] = intake [i]["Intake"]
    x = -1
    for cat in intake [i]:
        x += 1
        if (x < 5):
            continue
        
        category_wise_intake [i][cat] = intake [i][cat]


# ~ print (category_wise_intake)    
# ~ print (intake)
xl = pandas.read_excel (sys.argv [3], engine = "openpyxl")
total = 0
for index, rows in xl.iterrows():
    course = rows [6].split ("CLUJ: ")[1]
    if not course in alloted:
        alloted [course] = dict ()
    cat = rows [15]
    cat = cat.replace ("general", "gen")
    if not cat in alloted [course]:
        alloted [course][cat] = 0
    
    alloted [course][cat] += 1
    total +=1
    
category_wise_intake = category_wise_intake [selected_course]
alloted = alloted [selected_course]
# ~ print ("-------| Total intake |-------------")
# ~ print (category_wise_intake)
# ~ print ("-------| Total alloted |-------------")
# ~ print (total, alloted)

gen_jk = 0
for al in alloted:
    ual = al.lower ()
    
    if ual.startswith ("gen_jk"):
        category_wise_intake ["gen"] -= alloted [al]
    elif ual.startswith ("gen"):
        category_wise_intake ["gen_out"] -= alloted [al]
    else: 
        cat = ual.split ("_")[0]
        if cat in category_wise_intake:
            category_wise_intake [cat] -= alloted [al]

# ~ print ("-------| Remaining |-------------")
# ~ print (gen_jk, category_wise_intake)

total_intake = dict (category_wise_intake)

xl = pandas.read_excel (sys.argv [4], engine = "openpyxl")
full_list = dict ()
i = 0
merit_list = dict ()

for index, rows in xl.iterrows():
    i = 0
    cat = mapping [rows [6]]
    if not cat in full_list:
        full_list [cat] = []
    
    if not cat in merit_list:
        merit_list [cat]= []
        
    data = dict ()
    for x in range (len (rows)):
        data [rows.keys () [x]] = rows [x]

    if category_wise_intake ["gen"] > 0:
        if not "gen" in merit_list:
            merit_list ["gen"] = []
            
        if data ["SchoolState"] != "Jammu and Kashmir":
            print ("\n\n------| school state: ", data ["ScrhoolState"])
            if category_wise_intake ["gen_out"] > 0:
                print (f'left: ', category_wise_intake ["gen_out"])
                category_wise_intake ["gen_out"] -= 1
            else:
                print ('no seats left!')
                continue
        elif not check_commerce (data):
            if alloted ["gen_jk_non_commerce"] < total_intake ["gen"] / 10:
                alloted ["gen_jk_non_commerce"] += 1
            else:
                continue
                    
        category_wise_intake ["gen"] -= 1
        merit_list ["gen"].append (data)
        continue

    full_list [cat] .append (data)

for f in full_list:
    # ~ print (f)
    if f == "gen":
        continue
    for d in full_list [f]:
        if d ["SchoolState"] != "Jammu and Kashmir":
            continue
        
        if category_wise_intake [f] > 0:
            if not f in merit_list:
                merit_list [f] = []

            if not check_commerce (d):
                # ~ print (f"\n-------| {f} not commerce: ")
                if alloted [cat + "_non_commerce"] < total_intake [cat] / 10:
                    # ~ print ("but still alloted", alloted [cat + "_non_commerce"], total_intake [cat] / 10, "\n")
                    alloted [cat + "_non_commerce"] += 1
                else:
                    # ~ print ("not alloted ...!", alloted [cat + "_non_commerce"], total_intake [cat] / 10, "\n")
                    continue
                    
            category_wise_intake [f] -= 1
            merit_list [f].append (d)
        # ~ for data in d:
            # ~ print (data, d[data])

# ~ pprint.pprint (merit_list ["st2"])
# ~ print (len (merit_list ["st2"]))
# ~ print (len (merit_list ["gen"]))

for cat in merit_list:
    i = 1
    for student in merit_list [cat]:
        print (cat, f'[{i}/{round (total_intake [cat])}]', student ["AmissionCategorySelected"], student ["Registration_no"], student ["name"], student ["XIIPERCENTAGE"], f'{check_commerce (student)}', sep=",")
        i += 1

# ~ print (alloted)
# ~ print (total_intake)
