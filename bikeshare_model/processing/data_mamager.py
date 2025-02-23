import pandas as pd 
import config.core as core

def read_input_data():
    print(core.dataFile)
    bikeshare = pd.read_csv(core.dataFile)    
    return bikeshare

