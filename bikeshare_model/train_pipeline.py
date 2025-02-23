from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from processing import data_mamager
import pipeline
import joblib
import config.core as core


df = data_mamager.read_input_data()
X=df.drop(columns=['cnt'])
y=df['cnt']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


X_train = pipeline.piperline.fit_transform(X_train, y_train)
X_test = pipeline.piperline.fit_transform(X_test, y_test)

trained_model = pipeline.piperline_predict.fit(X_train,y_train)
joblib.dump(trained_model, core.MODEL_PATH)
y_pred = trained_model.predict(X_test)
print(f'Predicted value: {y_pred}')

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R2 Score: {r2}")