import pandas as pd
import pipeline
import joblib
import config.core as core
import numpy as np

def getUserDataPreprocessed():
    data={'dteday': '05-11-2012' , 'season': 'winter' , 'hr' : '6am' , 'holiday' : 'No ','weekday' : 'Yes','workingday':'Yes', 'weathersit': 'Mist', 'temp': 6.1,'atemp' : 3.0014, 'hum': 49, 'windspeed': 10.0012}
    user=pd.DataFrame([data])
    user['dteday'] = pd.to_datetime('05-11-2012', format='%d-%m-%Y')
    user_y=129
    user['casual'] = np.nan
    user['registered'] = np.nan
    user=pipeline.piperline.fit_transform(user)
    return user,user_y

def runSavedModel(user):
    print('Loading the saved data for user data verification')
    pipel=joblib.load(core.MODEL_PATH)
    u_pred = pipel.predict(user)
    print(f'User data Predicted with loaded model = {u_pred}')
    return u_pred

def main():
    user,user_y = getUserDataPreprocessed()
    Y_pred = runSavedModel(user)
    print(f'Predicted value: {Y_pred}')
    
if __name__ == "__main__":
    
    main()