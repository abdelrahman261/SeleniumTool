from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np 
from functions import SeleniumToolScraping , Coordinates



df=pd.read_excel("/Users/abdelrahmanhesham/Downloads/qal vs helwan.xlsx")
df3=df[:5]

## Make Sure X , Y  with same shape as shown

katameya_scraper = SeleniumToolScraping("Katameya Heights, New Cairo, Egypt","29.992708,31.293171")

result_df = katameya_scraper.PreprocessData(df3)



print (result_df)