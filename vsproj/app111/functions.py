import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class Coordinates:

    @staticmethod
    def X_Y_Coordinates(row):
        return f"{row['Y']},{row['X']}"
    


class SeleniumToolScraping:
    

    def __init__(self ,discribtion , site):

        self.discribtion=discribtion
        self.site=site
        self.driver=None


    def initialize_driver(self):

        if self.driver is None:
            self.driver = webdriver.Firefox()
            self.driver.get("https://www.google.com/maps/@29.9892736,31.3982976,12z?hl=en&entry=ttu")
            direction_button = self.driver.find_element(By.ID, "hArJGc")
            direction_button.click()
            time.sleep(3)
    

    def close_driver(self):

        if self.driver:
            self.driver.quit()
            self.driver = None

    
    @staticmethod
    def CoordinatesModifacation(df):
       
        df["Coordinates"]=df.apply(Coordinates.X_Y_Coordinates,axis=1)
        return (df)
    


    
    def Operation(self , row):
       
        try:
            self.initialize_driver()
            
            direction_box_site = self.driver.find_element(By.CLASS_NAME, "tactile-searchbox-input")
            direction_box_client = self.driver.find_element(By.XPATH, "//*[@id='sb_ifc51']/input")
            
            direction_box_site.click()
            direction_box_site.clear()
            direction_box_site.send_keys(self.site)
            
            direction_box_client.click()
            direction_box_client.clear()
            direction_box_client.send_keys(row['Coordinates'])  
            
            time.sleep(1)
            
            bus_icon_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/button/div[1]/span")
            bus_icon_button.click()
            
            best_icon_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[1]/div/div/div/div[1]/button/div[1]")
            best_icon_button.click()
            
            time.sleep(2)
            
            distance = self.driver.find_element(By.XPATH, "//*[@id='section-directions-trip-0']/div[1]/div/div[1]/div[2]").text
            time_text = self.driver.find_element(By.XPATH, "//*[@id='section-directions-trip-0']/div[1]/div/div[1]/div[1]").text
            
            print(f"Row {row.name}: Distance={distance}, Time={time_text}")
            
            return pd.Series([distance, time_text])
            
        except Exception as e:
            print(f"Error processing row {row.name}: {str(e)}")
            return pd.Series([np.nan, np.nan])
    

    def PreprocessData(self,df):

        df=SeleniumToolScraping.CoordinatesModifacation(df)
        df["Counter"] = range(1, len(df) + 1)

        try :
             df[["Distance", "Time"]] = df.apply(self.Operation, axis=1)

        finally:
              self.close_driver()

        return df 

    def __str__(self):
                    return f"{self.df}"
