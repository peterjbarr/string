# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 22:09:37 2021

@author: PBarr
"""
# Unit 2 Section 4 assessment
# How to read csv file
# import the pandas library as pd for short hand
import pandas as pd
from tabulate import tabulate

#expanding the columns in frame to show data
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('mode.use_inf_as_na', True)

# read the CSV file
epd_20 = pd.read_csv(r'C:\Users\PBarr\Documents\git\string\data\EPD_202004.csv')
epd_21 = pd.read_csv(r'C:\Users\PBarr\Documents\git\string\data\EPD_202104.csv')
# displaying the contents of the CSV file - this will take a few seconds.
print(epd_20)
print(epd_21)
# check that a data frame has been created for each epd dataset
type(epd_20)
type(epd_21)

# read in the second EDP file as above
# you are now ready to explore the data


#-----new df for BNF_CHAPTER_PLUS_CODE and TOTAL_QUANTITY April 20----
epdq_20 = epd_20[['BNF_CHAPTER_PLUS_CODE','TOTAL_QUANTITY','ACTUAL_COST']].copy()
#print(epdq_20)

##group by BNF_CHAPTER_PLUS_CODE
epdq_20 = epdq_20.groupby(['BNF_CHAPTER_PLUS_CODE']).sum()

epdq_20.rename(columns={'TOTAL_QUANTITY':'QUANTITY_APRIL20'}, inplace=True) 
epdq_20.rename(columns={'ACTUAL_COST':'COST_APRIL20'}, inplace=True)
#epdq_20.['COST_APRIL20'] = epdq_20['COST_APRIL20'].apply(lambda x: "£{:.1f}k".format((x/1000)))
#print(epdq_20)
#ordered=True

#epdq_20.plot(kind = 'barh')
#----------------------------------------------------------------------
#------new df for BNF_CHAPTER_PLUS_CODE and TOTAL_QUANTITY April 21----
epdq_21 = epd_21[['BNF_CHAPTER_PLUS_CODE','TOTAL_QUANTITY','ACTUAL_COST']].copy()
#print(epdq_21)

##group by BNF_CHAPTER_PLUS_CODE
epdq_21 = epdq_21.groupby(['BNF_CHAPTER_PLUS_CODE']).sum()
epdq_21.rename(columns={'TOTAL_QUANTITY':'QUANTITY_APRIL21'}, inplace=True)
epdq_21.rename(columns={'ACTUAL_COST':'COST_APRIL21'}, inplace=True)


#print(epdq_21)
#epdq_21.plot(kind = 'barh')
#-----------------------------------------------------------------------

# now merge frames together using merge function
result = pd.merge(epdq_20, epdq_21, how = "outer", on="BNF_CHAPTER_PLUS_CODE")
# change null value to 0
result = result.fillna(0)
# add total line
result.loc['Total']= result.sum(numeric_only=True, axis=0)
      
#add columns comparing quanity and cost
result["DiffFrom2020_Quan"] = (result["QUANTITY_APRIL21"] - result["QUANTITY_APRIL20"])
result["Percentage_Change_Quan"] = ((result["DiffFrom2020_Quan"] / result["QUANTITY_APRIL20"])*100)

result["DiffFrom2020_Cost"] = (result["COST_APRIL21"] -  result["COST_APRIL20"])
result["Percentage_Change_Cost"] = ((result["DiffFrom2020_Cost"] / result["COST_APRIL20"])*100)

# plot quantity and cost differences (Percentage Change)
percent_change = result[['Percentage_Change_Quan', 'Percentage_Change_Cost']].copy()


plot1 = percent_change.plot(kind = 'barh', title='Percentage Change in Quantity and Cost April 21 compared with April 20')
plot1.xlabel = "Percentage Change (%)"
plot1.set_xlabel("Percentage Change (%)")
plot1.set_ylabel("BNF Chapter")


plot2 = percent_change.plot(kind = 'barh', title='Percentage Change in Quantity and Cost April 21 compared with April 20 (x axis reduced)')
plot2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plot2.set_xlim(-25, 25)
plot2.set_xlabel("Percentage Change (%)")
plot2.set_ylabel("BNF Chapter")

#----------------------------------------------
# 14: Immunological Products and Vaccines - increased by 400% - what was it that increased in this category

# 14: Immunological Products and Vaccines - increased by 400% - what was it that increased in this category


#filter data for 14. Vaccines only April 20
epd_20_Vaccines = epd_20[epd_20.BNF_CHAPTER_PLUS_CODE == '14: Immunological Products and Vaccines'][['BNF_CHAPTER_PLUS_CODE','CHEMICAL_SUBSTANCE_BNF_DESCR','TOTAL_QUANTITY','ACTUAL_COST']]
#apply group by
epd_20_Vaccines = epd_20_Vaccines.groupby(['CHEMICAL_SUBSTANCE_BNF_DESCR']).sum()
#rename TOTAL_QUANTITY and ACTUAL_COST columns
epd_20_Vaccines.rename(columns={'TOTAL_QUANTITY':'QUANTITY_APRIL20'}, inplace=True) 
epd_20_Vaccines.rename(columns={'ACTUAL_COST':'COST_APRIL20'}, inplace=True)
#print(epd_20_Vaccines)

#filter data for 14. Vaccines only April 21
epd_21_Vaccines = epd_21[epd_21.BNF_CHAPTER_PLUS_CODE == '14: Immunological Products and Vaccines'][['BNF_CHAPTER_PLUS_CODE','CHEMICAL_SUBSTANCE_BNF_DESCR','TOTAL_QUANTITY','ACTUAL_COST']]
#apply group by 
epd_21_Vaccines = epd_21_Vaccines.groupby(['CHEMICAL_SUBSTANCE_BNF_DESCR']).sum()
#rename TOTAL_QUANTITY and ACTUAL_COST columns
epd_21_Vaccines.rename(columns={'TOTAL_QUANTITY':'QUANTITY_APRIL21'}, inplace=True) 
epd_21_Vaccines.rename(columns={'ACTUAL_COST':'COST_APRIL21'}, inplace=True)

epd_Vaccines_merg = pd.merge(epd_20_Vaccines, epd_21_Vaccines, how = "outer", on="CHEMICAL_SUBSTANCE_BNF_DESCR")
# change null value to 0
epd_Vaccines_merg = epd_Vaccines_merg.fillna(0)
# add total line
epd_Vaccines_merg.loc['Total']= result.sum(numeric_only=True, axis=0)

#add columns comparing quanity and cost
epd_Vaccines_merg["DiffFrom2020_Quan"] = (epd_Vaccines_merg["QUANTITY_APRIL21"] - epd_Vaccines_merg["QUANTITY_APRIL20"])
epd_Vaccines_merg["Percentage_Change_Quan"] = ((epd_Vaccines_merg["DiffFrom2020_Quan"] / epd_Vaccines_merg["QUANTITY_APRIL20"])*100)

epd_Vaccines_merg["DiffFrom2020_Cost"] = (epd_Vaccines_merg["COST_APRIL21"] -  epd_Vaccines_merg["COST_APRIL20"])
epd_Vaccines_merg["Percentage_Change_Cost"] = ((epd_Vaccines_merg["DiffFrom2020_Cost"] / epd_Vaccines_merg["COST_APRIL20"])*100)


#format numbers
def format(x):
        return "£{:,.0f}".format(x)

epd_Vaccines_merg['COST_APRIL20'] = epd_Vaccines_merg['COST_APRIL20'].apply(format)
epd_Vaccines_merg['COST_APRIL21'] = epd_Vaccines_merg['COST_APRIL21'].apply(format)
epd_Vaccines_merg['DiffFrom2020_Cost'] = epd_Vaccines_merg['DiffFrom2020_Cost'].apply(format)

def format(x):
        return "{:,.0f}".format(x)
epd_Vaccines_merg['QUANTITY_APRIL20'] = epd_Vaccines_merg['QUANTITY_APRIL20'].apply(format)
epd_Vaccines_merg['QUANTITY_APRIL21'] = epd_Vaccines_merg['QUANTITY_APRIL21'].apply(format)
epd_Vaccines_merg['DiffFrom2020_Quan'] = epd_Vaccines_merg['DiffFrom2020_Quan'].apply(format)

def format(x):
    return "{:,.0f}".format(x)
    
    
epd_Vaccines_merg['Percentage_Change_Quan'] = epd_Vaccines_merg['Percentage_Change_Quan'].apply(format)
epd_Vaccines_merg['Percentage_Change_Cost'] = epd_Vaccines_merg['Percentage_Change_Cost'].apply(format)

print(epd_Vaccines_merg)
#--------------------------------------------



#plot actual cost difference
cost_diff = result[['DiffFrom2020_Cost']].copy()
cost_diff2 = result[['COST_APRIL20','COST_APRIL21']].copy()

print(cost_diff2)


plot3 = cost_diff2.plot(kind = 'bar', title='Actual cost comparison in BNF Chapters April 20 and April 21')
plot3.set_xlabel("BNF Chapter")
plot3.set_ylabel("£m")
plot3.legend(loc='center left', bbox_to_anchor=(1, 0.5))


plot4 = cost_diff2.plot(kind = 'bar', title='Actual cost comparison in BNF Chapters April 20 and April 21')
plot4.set_xlabel("BNF Chapter")
plot4.set_ylabel("£m")
plot4.set_ylim(0,1750000)
plot4.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plot5 = cost_diff.plot(kind = 'bar', title='Actual cost increase/descrease in BNF Chapter Categories April 20 and April 21')
plot5.set_xlabel("BNF Chapter")
plot5.set_ylabel("£")
plot6 = cost_diff.plot(kind = 'bar', title='Actual cost increase/descrease in BNF Chapter Categories April 20 and April 21')
plot6.set_xlabel("BNF Chapter")
plot6.set_ylabel("£")
plot6.set_ylim(-70000,110000)



#now format columns 
def format(x):
        return "£{:,.1f}K".format(x/1000)

result['COST_APRIL20'] = result['COST_APRIL20'].apply(format)
result['COST_APRIL21'] = result['COST_APRIL21'].apply(format)
result['DiffFrom2020_Cost'] = result['DiffFrom2020_Cost'].apply(format)

def format(x):
        return "{:,.1f}K".format(x/1000)
result['QUANTITY_APRIL20'] = result['QUANTITY_APRIL20'].apply(format)
result['QUANTITY_APRIL21'] = result['QUANTITY_APRIL21'].apply(format)
result['DiffFrom2020_Quan'] = result['DiffFrom2020_Quan'].apply(format)

def format(x):
    return "{:,.1f}".format(x)
    
    
result['Percentage_Change_Quan'] = result['Percentage_Change_Quan'].apply(format)
result['Percentage_Change_Cost'] = result['Percentage_Change_Cost'].apply(format)



print(result)


print(tabulate(result, headers='keys', tablefmt='psql'))



#plt.show()


#print(result)

