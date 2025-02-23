import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


def get_year_and_month(dataframe):

    df = dataframe.copy()
    # convert 'dteday' column to Datetime datatype
    df['dteday'] = pd.to_datetime(df['dteday'], format='%Y-%m-%d')
    # Add new features 'yr' and 'mnth
    df['yr'] = df['dteday'].dt.year
    df['mnth'] = df['dteday'].dt.month_name()

    return df

def drop_columns(df):
    unused_colms = ['casual', 'registered']
    df = df.drop(unused_colms, axis = 1)
    return df

class WeekdayImputer(BaseEstimator, TransformerMixin):
    """ Impute missing values in 'weekday' column by extracting dayname from 'dteday' column """

    def __init__(self,):
        # YOUR CODE HERE
        self.day_names = None

    def fit(self,df,y=None,dteday='dteday',weekday='weekday'):
        # YOUR CODE HERE
        return self

    def transform(self,df,y=None,dteday='dteday',weekday='weekday'):
        # YOUR CODE HERE
        df[dteday]=pd.to_datetime(df['dteday'])
        day_names = df[dteday].dt.day_name()[:3]
        df[weekday] = df[weekday].fillna(day_names)
        df = df.drop(columns=[dteday])
        return df


class WeathersitImputer(BaseEstimator, TransformerMixin):
    """ Impute missing values in 'weathersit' column by replacing them with the most frequent category value """

    def __init__(self,):
        # YOUR CODE HERE
        self.most_frequent_category = None

    def fit(self,df,y=None,weathersit='weathersit'):
        # YOUR CODE HERE
        self.most_frequent_category = df[weathersit].mode()[0]
        return self

    def transform(self,df,y=None,weathersit='weathersit'):
        # YOUR CODE HERE
        df[weathersit] = df[weathersit].fillna(self.most_frequent_category)
        return df
    

class Mapper(BaseEstimator, TransformerMixin):
    """
    Ordinal categorical variable mapper:
    Treat column as Ordinal categorical variable, and assign values accordingly
    """

    def __init__(self,):
        # YOUR CODE HERE
        self.cat_cols = None
        self.mappings={}

    def fit(self,df,y=None):
        # YOUR CODE HERE
        self.cat_cols = cat_cols=df.select_dtypes(include=['object']).columns
        for col in self.cat_cols:
            uq=df[col].unique()
            self.mappings[col]={ value : key+1 for key,value in enumerate(uq)}
        return self

    def transform(self,df,y=None):
        # YOUR CODE HERE
        for col, mapping in self.mappings.items():
            if col in df.columns:
                df['new_'+col] = df[col].map(mapping)
        return df


class OutlierHandler(BaseEstimator, TransformerMixin):
    """
    Change the outlier values:
        - to upper-bound, if the value is higher than upper-bound, or
        - to lower-bound, if the value is lower than lower-bound respectively.
    """

    def __init__(self,method='iqr', factor=1.5):
        # YOUR CODE HERE
        self.method = method
        self.factor = factor

    def fit(self,df,y=None):
        # YOUR CODE HERE
        self.columns= df.select_dtypes(include=['int64', 'float64']).columns
        return self

    def transform(self,df,y=None):
        # YOUR CODE HERE
        df = df.copy()

        for col in self.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - self.factor * IQR
            upper_bound = Q3 + self.factor * IQR

            df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
            df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

        return df

class WeekdayOneHotEncoder(BaseEstimator, TransformerMixin):
    """ One-hot encode weekday column """

    def __init__(self,):
        # YOUR CODE HERE
        self.encoder = None

    def fit(self,df,y=None):
        # YOUR CODE HERE
        return self

    def transform(self, df):
        # YOUR CODE HERE
        df=df.copy()
        weekday=['Mon', 'Tue' , 'Wed', 'Thu', 'Fri' , 'Sat','Sun']
        for idx,day in enumerate(weekday):
            df['weekday'+'_'+str(idx+1)] = np.where(df['weekday'] == day,1,0)
        
        df = df.drop(columns=['weekday'])
        
        return df
    
class Mapper(BaseEstimator, TransformerMixin):
    """
    Ordinal categorical variable mapper:
    Treat column as Ordinal categorical variable, and assign values accordingly
    """

    def _init_(self,):
        # YOUR CODE HERE
        self.cat_cols = None
        self.mappings={}
        

    def fit(self,df,y=None):
        # YOUR CODE HERE

        return self

    def transform(self,df,y=None):
        # YOUR CODE HERE
        df=df.copy()
        season=['winter', 'fall', 'spring', 'summer']
        season_mapping={value:idx for idx,value in enumerate(season)}
        hr = ['12am','1am', '2am', '3am','4am','5am','6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm','11pm']
        hr_mapping = {value:idx for idx,value in enumerate(hr)}
        weathersit = ['Mist', 'Clear', 'Light Rain', 'Heavy Rain']
        weathersit_mapping ={value:idx for idx,value in enumerate(weathersit)}
        holiday = ['Yes','No']
        holiday_mapping = {'Yes' : 1 , 'No': 0}
        workingday = ['Yes','No']
        workingday_mapping = {'Yes' : 1 , 'No': 0}

        df['season']=df['season'].map(season_mapping)
        df['hr'] = df['hr'].map(hr_mapping)
        df['weathersit']=df['weathersit'].map(weathersit_mapping)
        df['holiday']=df['holiday'].map(holiday_mapping)
        df['workingday']=df['workingday'].map(workingday_mapping)

        return df