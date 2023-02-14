"""
Created on Sun Jun 24 09:04:05 2018

@author: dougw
"""

import numpy as np
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

Tk().withdraw()
# openfilename = askopenfilename()
openfilename = "scheduleS2.csv"

dates = ["Names"]
counter = 0
teachers = []
roomlist = []
preps = []
with open(openfilename, 'rt') as f:
    reader = csv.reader(f)
    next(reader,None)

    for row in reader:
        # get the names of the dates
        if counter == 0:
            for d in row[6:]:
                dates.append(d)
        # for each teacher
        if counter >= 2:           
            # gets teacher name and their home rooms
            teach = []
            for t in row[:4]:
                teach.append(t)
                if row[1]:
                    roomlist.append(row[1])
                    print(row[1])
                if row[2]:
                    roomlist.append(row[2])
                    print(row[2])
                if row[3]:
                    roomlist.append(row[3])
                    print(row[3])
            teachers.append(teach)

        counter = 1 + counter


rooms = list(set(roomlist))
print("rooms = ", rooms)

schedule = np.empty((len(teachers)+1,len(dates)), dtype='<U100')

i = 0
for d in dates:
    schedule[0,i] = d
    i += 1

with open(openfilename, 'rt') as f:
    reader = csv.reader(f)
    next(reader,None)
    
    line = 0
    for row in reader:
        if line >= 2:
            col = 0
            schedule[line-1,col] = row[0]
            # preps is a list in list. each list inside gets the preps
            for p in row[6:]:
                data = p.strip().lower()
                if p == "OFF/PREP":
                    schedule[line-1,col+1] = p
                else:
                    schedule[line-1,col+1] = ""
                col += 1
        line += 1

# fill in teachers
col = 1

#teachers with rooms
teachfilled = 0
while col <= len(dates)-1:
# while col <= 2:
    rrow = 1
    available = rooms.copy()
    while rrow <= len(teachers):
        roomnumber = teachers[rrow-1][1]
        if roomnumber:
            if schedule[rrow,col] == '':
                schedule[rrow,col] = roomnumber
                temp = available.index(roomnumber)
                if available[temp] != "GYM":
                    t = available.pop(temp)
                    teachfilled += 1
   
        rrow += 1
    if col == 1:
        print(available)
    if col == 36:
        print("after 1st round = ", available)
        print("teachers left = ", teachleft)
    # try 2nd choice for teachers
    rrow = 1
    while rrow <= len(teachers)-1:
        roomnumber = teachers[rrow-1][2]
        if roomnumber:
            try:
                temp = available.index(roomnumber)
            except:
                temp = None
            if temp != None:
                if schedule[rrow,col] == '':
                    schedule[rrow,col] = roomnumber
                    teachfilled += 1
                    if available[temp] != "GYM":
                        available.pop(temp)
        
        rrow += 1
        
    # try 3rd choice for teachers
    row = 1
    while row <= len(teachers)-1:
        roomnumber = teachers[row-1][3]
        if roomnumber:
            try:
                temp = available.index(roomnumber)
            except:
                temp = None
            if temp != None:
                if schedule[row,col] == '':
                    schedule[row,col] = roomnumber
                    teachfilled += 1
                    if temp != None:
                        if available[temp] != "GYM":
                            available.pop(temp)
                            
        
        row += 1

    # get any room on same floor  
    row = 1
    teachleft = 0
    while row <= len(teachers)-1:
        if schedule[row,col] == '':
            teachleft += 1
        row += 1
        
    row = 1
    while row <= len(teachers)-1:
        roomnumber = teachers[row-1][2]
        if roomnumber:
            floor_number = roomnumber[0]
            n = 0
            filled = False
            while n < len(available):
                avail = available[n]
                if avail[0] == floor_number:
                    if schedule[row,col] == '':
                        schedule[row,col] = available[n]
                        temp = available.index(available[n])
                        if col == 1:
                            print(available[n])
                        available.pop(temp)
                        
  
                n += 1
        row += 1
        
    # get any room
    teachleft = 0
    row = 1
    while row <= len(teachers)-1:
        if schedule[row,col] == '':
            teachleft += 1
        row += 1

    row = 1
    while row <= len(teachers)-1:
        n = 0       
        if schedule[row,col] == '':
            try:
                temp = available[0]
                if available[0] == "GYM" or available[0] == "Library1" or available[0] == "Library2":
                    available.pop(0)
            except:
                print("ran out in column = ", col)
            try:
                schedule[row,col] = available[0]
                temp = available.index(available[0])
#                 if col == 1:
#                     print(available[0])
                available.pop(temp)
            except:
                print("ran out in column = ", col)
     
        row += 1

    col += 1
    

np.savetxt("foo.csv", schedule, delimiter=",", header='string', comments='', fmt='%s')
