# -*- coding: utf-8 -*-
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

# summarise the BNF Chapter column for April 2020 
print('Summarise April 2020 Data:')
descrip_BNF_CHAPTER20 = epd_20.BNF_CHAPTER_PLUS_CODE.describe()

print()
print(descrip_BNF_CHAPTER20)

#calculate the total cost of pharmaceutical products in April 2020
sum = epd_20.ACTUAL_COST.sum()
print ("Total Value of Pharm Products April 2020: £{:0,.2f}".format( sum) )
print ("------------------------------------------------------------")

# summarise the BNF Chapter column for April 2021
print('Summarise April 2021 Data')
descrip_BNF_CHAPTER21 = epd_21.BNF_CHAPTER_PLUS_CODE.describe()
print()
print(descrip_BNF_CHAPTER21)

#calculate the total cost of pharmaceutical products in April 2021
sum = epd_21.ACTUAL_COST.sum()
print("Total Value of Pharm Products April 2021: £{:0,.2f}".format( sum))
print ("------------------------------------------------------------")

      