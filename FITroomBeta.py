"""
Created on Sun Jun 24 09:04:05 2018

@author: dougw
"""

import numpy as np
import random
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

Tk().withdraw()
# openfilename = askopenfilename()
openfilename = "scheduleS2test.csv"

dates = ["Names"]
counter = 0
teachers = []
roomlist = []
preps = []
with open(openfilename, 'rt') as f:
    reader = csv.reader(f)
    next(reader,None)
    teacher_index = 0
    for row in reader:
        # get the names of the dates
        if counter == 0:
            for d in row[3:]:
                dates.append(d)
        # for each teacher
        if counter >= 2:           
            # gets teacher name and their home rooms
            teach = []
            for t in row[:3]:
                teach.append(t)
                
                if row[1]:
                    roomlist.append(row[1])
#                     print(row[1])
                if row[2]:
                    roomlist.append(row[2])
#                     print(row[2])
#             print("t is ", teach[0])
            teachers.append((teach,counter-1))
            

        counter = 1 + counter

print("teachers are ", teachers)
print("dates are ", dates)
rooms = list(set(roomlist))
print("rooms = ", rooms.sort())
print("number of room ", len(rooms))

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
            for p in row[3:]:
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
    random_list = list(range(len(teachers)+1))
    random.shuffle(random_list)
    print(random_list)
#     random_list = random.shuffle(range(len(teachers)))  
    rrow = 1
    available = rooms.copy()
#     print(available)
#     while rrow <= len(teachers):
    for rl in random_list:
#         print(schedule[0][col])
        if (schedule[0][col])[0:2] == "Tu":
            roomnumber = teachers[rl-1][0][1]
        elif (schedule[0][col])[0:2] == "Th":
            roomnumber = teachers[rl-1][0][2]
        if roomnumber:
#             print(teachers[rrow-1][0][0],teachers[rrow-1][1])
            try:
                temp = available.index(roomnumber)
            except:
                temp = None
            if temp != None:
                if schedule[rl,col] == '':
                    schedule[rl,col] = roomnumber
#                     print("the t row is ", rrow)
                    if available[temp] != "GYM":
                        t = available.pop(temp)
                        teachfilled += 1

    # try 2nd choice for teachers
        if (schedule[0][col])[0:2] == "Tu":
            roomnumber = teachers[rl-1][0][2]
        elif (schedule[0][col])[0:2] == "Th":
            roomnumber = teachers[rl-1][0][1]
        if roomnumber:
            try:
                temp = available.index(roomnumber)
            except:
                temp = None
            if temp != None:
                if schedule[rl,col] == '':
                    schedule[rl,col] = roomnumber
                    teachfilled += 1
                    if available[temp] != "GYM":
                        available.pop(temp)
        
        rrow += 1
        if col == 1:
            print("teacher set is ", schedule[rl,0])
    # get any room on same floor          
    row = 1
#     while row <= len(teachers)-1:
    for rl in random_list:
        if (schedule[0][col])[0:2] == "Tu":
            roomnumber = teachers[rl-1][0][1]
        elif (schedule[0][col])[0:2] == "Th":
            roomnumber = teachers[rl-1][0][2]
        if roomnumber:
            floor_number = roomnumber[0]
            n = 0
            filled = False
            while n < len(available):
                avail = available[n]
                if avail[0] == floor_number:
                    if schedule[rl,col] == '':
                        schedule[rl,col] = available[n]
                        temp = available.index(available[n])
#                         if col == 1:
#                             print(available[n])
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
#     while row <= len(teachers)-1:
    for rl in random_list:
        n = 0       
        if schedule[rl,col] == '':
            try:
                temp = available[0]
                if available[0] == "GYM" or available[0] == "Library1" or available[0] == "Library2":
                    available.pop(0)
            except:
                print("ran out in column = ", col)
            try:
                schedule[rl,col] = available[0]
                temp = available.index(available[0])
#                 if col == 1:
#                     print(available[0])
                available.pop(temp)
            except:
                print("ran out in column = ", col)
     
        row += 1

    col += 1
    

np.savetxt("foo.csv", schedule, delimiter=",", header='string', comments='', fmt='%s')
