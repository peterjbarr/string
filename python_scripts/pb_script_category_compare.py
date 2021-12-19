# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 22:09:37 2021

@author: PBarr
"""
# Unit 2 Section 4 assessment
# How to read csv file
# import the pandas library as pd for short hand
import pandas as pd


#expanding the columns in frame to show data
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('mode.use_inf_as_na', True)

# read the CSV file
epd_20 = pd.read_csv(r'C:\Users\PBarr\Documents\git\string\data\EPD_202004.csv')
epd_21 = pd.read_csv(r'C:\Users\PBarr\Documents\git\string\data\EPD_202104.csv')
# displaying the contents of the CSV file - this will take a few seconds.
#print(epd_20)
#print(epd_21)
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

#plot actual cost difference
cost_diff = result[['DiffFrom2020_Cost']].copy()
cost_diff2 = result[['COST_APRIL20','COST_APRIL21']].copy()
print(cost_diff2)


plot3 = cost_diff2.plot(kind = 'bar')
plot4 = cost_diff.plot(kind = 'bar')





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

#plt.show()


#print(result)

