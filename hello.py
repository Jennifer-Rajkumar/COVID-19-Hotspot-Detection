# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 16:21:59 2021

@author: Jennifer
"""


import openpyxl 
import pymongo
  
from collections import OrderedDict
wrkbk = openpyxl.load_workbook("C:/Users/Jennifer/.spyder-py3/Hotspot1/Hotspot/vaccine.xlsx") 
  
sh = wrkbk.active 

d={}

for row in sh.iter_rows(min_row=1, min_col=1, max_row=7936, max_col=14): 
    l=[]
    for cell in row: 
        l.append(cell.value) 
    if l[6].lower() not in d:
        d[l[6].lower()]=[l[7].lower()]
    else:
        d[l[6].lower()].append(l[7].lower())
    
for k,v in d.items():
    d[k]=list(OrderedDict.fromkeys(v))

print(d)