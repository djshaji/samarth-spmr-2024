import pandas, sys, json,math, pprint

data = {"Minor": {},
        "Multi Disciplinary": {},
        "Skill Development": {},
        "Value Added Suject 1": {},	
        "Value Added Subject 2": {},
        "Ability Enhancement": {}}

for filename in sys.argv [1:]:
    xl = pandas.read_excel (filename, engine = "openpyxl")
    for index, row in xl.iterrows():
        for d in data:
            if not row [d] in data [d]:
                data [d][row [d]] = 0
            data [d][row [d]] += 1

for d in data:
    for x in data [d]:
        print (d, x, data [d][x], sep=": ")
