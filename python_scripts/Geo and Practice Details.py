# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:17:36 2021

@author: nickw
"""

import pandas as pd

import matplotlib.pyplot as plt

import requests

import plotly.express as px

import plotly.io as pio

pio.renderers.default = 'browser'

##Import Data

M2020 = pd.read_csv (r'C:\Users\nickw\OneDrive\Documents\Python Scripts\Test\Test\EPD_202004.csv')

M2021 = pd.read_csv (r'C:\Users\nickw\OneDrive\Documents\Python Scripts\Test\Test\EPD_202104.csv')

##Import Population Data by Practice

pop_gp = pd.read_csv (r'C:\Users\nickw\OneDrive\Documents\Python Scripts\Test\Test\gp_pop.csv')

pop__gp_2021 = pd.read_csv (r'C:\Users\nickw\OneDrive\Documents\Python Scripts\Test\Test\GP_Pop_2021.csv')

##Import Geojson

r = requests.get('https://raw.githubusercontent.com/missinglink/uk-postcode-polygons/master/geojson/M.geojson')

Manchester_Map = r.json()


##Split the postcode

M2020[['Postcode_Region', 'Postcode_Detail']] = M2020.POSTCODE.str.split(" ", expand=True)

##Group by Practice sum

M2020 = M2020.groupby(['PRACTICE_CODE', 'POSTCODE', 'PRACTICE_NAME', 'Postcode_Region']).sum().reset_index()

## Link with Popualtion Data for GP Practices

M2020 = pd.merge(M2020,pop_gp ,on='PRACTICE_CODE',how='left')

M2020 ['Cost_Capita']= M2020.ACTUAL_COST/M2020.Population

##Test all rows where null 

TestM2020= M2020[M2020.isna().any(axis=1)]

print(TestM2020['PRACTICE_NAME'])

M2020 = M2020[M2020['Population'].notna()]

##New Dataset by Postcode

M2020_Postcode = M2020.groupby(['Postcode_Region']).sum().reset_index()

M2020_Postcode['Cost_Capita2']= M2020_Postcode.ACTUAL_COST/M2020_Postcode.Population

##Repeat for M2021

M2021[['Postcode_Region', 'Postcode_Detail']] = M2021.POSTCODE.str.split(" ", expand=True)

M2021 = M2021.groupby(['PRACTICE_CODE', 'POSTCODE', 'PRACTICE_NAME', 'Postcode_Region']).sum().reset_index()

M2021 = pd.merge(M2021,pop__gp_2021 ,on='PRACTICE_CODE',how='left')

M2021['Cost_Capita']= M2021.ACTUAL_COST/M2021.Population

##Test all null rows are non-specific to GP Practice

TestM2021= M2021[M2021.isna().any(axis=1)]

print(TestM2021['PRACTICE_NAME'])

M2021 = M2021[M2021['Population'].notna()]

M2021_Postcode = M2021.groupby(['Postcode_Region']).sum().reset_index()

M2021_Postcode['Cost_Capita2']= M2021_Postcode.ACTUAL_COST/M2021_Postcode.Population

##Rename Columns

M2020.rename(columns = {'Cost_Capita' : 'Cost_2020'}, inplace= True)

M2021.rename(columns = {'Cost_Capita' : 'Cost_2021'}, inplace= True)

##Merge 2020/2021

Site_Cost = pd.merge(M2020,M2021, how='outer', on= 'PRACTICE_CODE')

##Remove unneccessary columns

Site_Cost.drop(Site_Cost.columns[3:13], axis = 1, inplace = True)

Site_Cost.drop(Site_Cost.columns[4:16], axis = 1, inplace = True)

##Percentage Change

Site_Cost['Percentage_Change']= (Site_Cost.Cost_2021/Site_Cost.Cost_2020-1)*100

## Sort by 2021

Site_Cost =Site_Cost.sort_values(by = 'Cost_2021', ascending= False)

Site_Cost.set_index("PRACTICE_NAME_x", drop=False, inplace = True)

## Merge for Postcode

M2021_Postcode.rename(columns = {'Cost_Capita2' : 'Cost_2021'}, inplace= True)

M2020_Postcode.rename(columns = {'Cost_Capita2' : 'Cost_2020'}, inplace= True)

M2020_Postcode.drop(M2020_Postcode.columns[1:11], axis = 1, inplace = True)

M2021_Postcode.drop(M2021_Postcode.columns[1:11], axis = 1, inplace = True)

Postcode_Cost = pd.merge(M2020_Postcode,M2021_Postcode, how='outer', on= 'Postcode_Region')

Postcode_Cost['Percentage_Change']= (Postcode_Cost.Cost_2021/Postcode_Cost.Cost_2020-1)*100

##boxplot explore
 
Comparison_Practice_21_22 = Site_Cost[['Cost_2020', 'Cost_2021']].boxplot()


##bar explore

Bar_Site = Site_Cost.plot(kind = 'barh', y= 'Cost_2021', x='PRACTICE_NAME_x').tick_params(axis= 'y' , labelsize = 2)

## Top 10

Site_Cost_Top_10 = Site_Cost.nlargest(10, "Cost_2021")

Top_10 = Site_Cost_Top_10[['Cost_2021', 'Cost_2020']].plot.barh()
plt.ylabel('PRACTICE NAME')
plt.xlabel('Cost Per Capita (£), April')
plt.title('Top 10 Highest Spending (Per Capita) GP Surgeries')

# Bottom 10

Site_Cost_Bottom_10 = Site_Cost.nsmallest(10, "Cost_2021")

Bottom_10 = Site_Cost_Bottom_10[['Cost_2021', 'Cost_2020']].plot.barh()
plt.ylabel('PRACTICE NAME')
plt.xlabel('Cost Per Capita (£), April')
plt.title('Bottom 10 Spending (Per Capita) GP Surgeries')
plt.xlim(0,20 )
plt.show()

##Change difference

Site_Cost =Site_Cost.sort_values(by = 'Percentage_Change', ascending= False)

Site_Change = Site_Cost.boxplot( column = "Percentage_Change", return_type = 'axes')

print(Site_Cost.describe())

print(Site_Cost.head())

##Regional Look Bar Chart

Postcode_Cost =Postcode_Cost.sort_values(by = 'Cost_2021', ascending= False)

Postcode_Cost.set_index("Postcode_Region", drop=False, inplace = True)

Postcode_Bar = Postcode_Cost[['Cost_2021', 'Cost_2020']].plot.bar()
plt.xlabel('Postcode Region')
plt.ylabel('Cost Per Capita (£), April')
plt.title('Postcode Per Capita Cost')
plt.show()

##Regional Map 2021 & Change

Manchester_Map['features'][1]['properties']

Postcode_Cost['id']= Postcode_Cost['Postcode_Region']

Postcode_Dictionary = {}

for feature in Manchester_Map['features']:
    feature['id']=feature['properties']['name']
    Postcode_Dictionary[feature['properties']['name']] =feature['id']
    
fig1 = px.choropleth(Postcode_Cost, locations = 'id', geojson= Manchester_Map, color= 'Cost_2021', hover_name='Postcode_Region', title= "Cost Per Capita April 2021" )
fig1.update_geos(fitbounds = "locations", visible= False)
fig1.show()

fig2 = px.choropleth(Postcode_Cost, locations = 'id', geojson= Manchester_Map, color= 'Cost_2020', hover_name='Postcode_Region', title= "Cost Per Capita April 2020" )
fig2.update_geos(fitbounds = "locations", visible= False)
fig2.show()

fig3 = px.choropleth(Postcode_Cost, locations = 'id', geojson= Manchester_Map, color= 'Percentage_Change', hover_name='Postcode_Region', title= "Cost Per Capita April 2020" )
fig3.update_geos(fitbounds = "locations", visible= False)
fig3.show()