# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 22:09:37 2021

@author: PBarr
"""
# Unit 2 Section 4 assessment
# How to read csv file
# import the pandas library as pd for short hand
import pandas as pd
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
epdq_20 = epd_20[['BNF_CHAPTER_PLUS_CODE','TOTAL_QUANTITY']].copy()
print(epdq_20)

##group by BNF_CHAPTER_PLUS_CODE
epdq_20 = epdq_20.groupby(['BNF_CHAPTER_PLUS_CODE']).sum()
print(epdq_20)

epdq_20.plot(kind = 'barh')
#----------------------------------------------------------------------
#------new df for BNF_CHAPTER_PLUS_CODE and TOTAL_QUANTITY April 21----
epdq_21 = epd_21[['BNF_CHAPTER_PLUS_CODE','TOTAL_QUANTITY']].copy()
print(epdq_21)

##group by BNF_CHAPTER_PLUS_CODE
epdq_21 = epdq_21.groupby(['BNF_CHAPTER_PLUS_CODE']).sum()
print(epdq_21)

epdq_21.plot(kind = 'barh')


      
