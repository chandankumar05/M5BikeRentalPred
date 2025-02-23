from sklearn.pipeline  import Pipeline
from processing.feature import WeathersitImputer, WeekdayImputer, OutlierHandler, WeekdayOneHotEncoder, Mapper
from sklearn.ensemble import RandomForestRegressor

piperline=Pipeline([
    ('weekday_imputer',WeekdayImputer()),
    ('weathersit_imputer',WeathersitImputer()),
    ('mapper',Mapper()),
    ('outlier_handler',OutlierHandler()),
    ('weekday_one_hot_encoder',WeekdayOneHotEncoder()),
])

piperline_fit=Pipeline([("preprocessing",piperline),('regressor',RandomForestRegressor())])

piperline_predict =  Pipeline([('regressor',RandomForestRegressor())])