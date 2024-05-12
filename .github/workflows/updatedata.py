# -*- coding: utf-8 -*-
"""updateData

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eiXmgGJYlrJx64vYp5t02yYp4MV_IvSa
"""

import pandas as pd
import json
import plotly.express as px
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

year = str((datetime.now() - relativedelta(months=2)).year)
month = ((datetime.now() - relativedelta(months=2)).strftime("%b")).lower()

link = (f'https://api.census.gov/data/{year}/cps/basic/{month}?get=PEEDUCA,HEFAMINC,PREXPLF,CBSA,PRHRUSL,PESEX,PRNMCHLD,PTDTRACE,PEMARITL,PEERNHRO,STATE&key=79d639ad2cdd37e119e00de062d8835dfa11355f')

datareq = requests.get(link).text
sample = json.loads(datareq)
item = 1
while item < len(sample):
  sample[item] += [year]
  item += 1

sample.pop(0)
final = sample

df = pd.DataFrame(final)
df

#Dictionary pulls
import pandas as pd
import requests
import json

#CBSA
citydict = requests.get("https://api.census.gov/data/2024/cps/basic/jan/variables/CBSA.json").text
citydict = json.loads(citydict)
citydict = citydict['values']['item']

#STATE
statelink = ("https://api.census.gov/data/2024/cps/basic/jan/variables/STATE.json")
statereq = requests.get(statelink).text
statedict = json.loads(statereq)
statedict = statedict['values']['item']

#PEEDUCA
educationlink = ("https://api.census.gov/data/2024/cps/basic/jan/variables/PEEDUCA.json")
educationreq = requests.get(educationlink).text
educationdict = json.loads(educationreq)
educationdict = educationdict['values']['item']

#HEFAMINC
Incomelink = ("https://api.census.gov/data/2024/cps/basic/jan/variables/HEFAMINC.json")
Incomereq = requests.get(Incomelink).text
Incomedict = json.loads(Incomereq)
Incomedict = Incomedict['values']['item']

#PREXPLF
Unemployedlink = ("https://api.census.gov/data/2024/cps/basic/jan/variables/PREXPLF.json")
Unemployedreq = requests.get(Unemployedlink).text
Unemployeddict = json.loads(Unemployedreq)
Unemployeddict = Unemployeddict['values']['item']

#PRHRUSL
Workweeklink = ("https://api.census.gov/data/2024/cps/basic/jan/variables/PRHRUSL.json")
Workweekreq = requests.get(Unemployedlink).text
Workweekdict = json.loads(Workweekreq)
Workweekdict = Workweekdict['values']['item']

#PESEX
Sexlink = ("https://api.census.gov/data/2024/cps/basic/jan/variables/PESEX.json")
Sexreq = requests.get(Sexlink).text
Sexdict = json.loads(Sexreq)
Sexdict = Sexdict['values']['item']

#PRNCHLD none

#PTDTRACE
Racelink = ("https://api.census.gov/data/2024/cps/basic/jan/variables/PTDTRACE.json")
Racereq = requests.get(Racelink).text
Racedict = json.loads(Racereq)
Racedict = Racedict['values']['item']



#PEMARITL
Maritallink = ("https://api.census.gov/data/2024/cps/basic/jan/variables/PEMARITL.json")
Maritalreq = requests.get(Maritallink).text
Maritaldict = json.loads(Maritalreq)
Martialdict = Maritaldict['values']['item']

#PEERNHRO none

#Data Clean 1
import pandas as pd
df = df.rename(columns=df.iloc[0])
df = df.iloc[1:]
df = df.reset_index(drop=True)

data = df.replace({"STATE":statedict,"CBSA":citydict, "PEEDUCA":educationdict, "HEFAMINC":Incomedict,"PREXPLF":Unemployeddict,"PRHRUSL":Workweekdict,"PESEX":Sexdict,"PTDTRACE":Racedict,"PEMARITL":Martialdict})

#del data['PRHRUSL']
data = data[(data['PEEDUCA'] == "Bachelor's Degree(ex:ba,ab,bs)") | (data['PEEDUCA'] == "MASTER'S DEGREE(EX:MA,MS,MEng,MEd,MSW)") | (data['PEEDUCA'] =="High School Grad-Diploma Or Equiv (ged)")]
data = data.reset_index(drop = True)
#data = data.rename(columns = {'Unnamed: 12':"Year"})

data.to_csv("DataUpdate.csv")
