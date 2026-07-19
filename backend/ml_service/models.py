from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from ml_service.features import build_dataset
 
def _predict_with(model, X, y, last_row, scale=False):
	if scale:
		scaler= StandardScaler()
		X_scaled= scaler.fit_transform(X)
		model.fit(X_scaled,y)
		pred= float(model.predict(scaler.transform(last_row))[0])
	else:
		model.fit(X,y)
		pred= float(model.predict(last_row)[0])
	return pred
 
def train_all(rows:list):
	dataset= build_dataset(rows)
	if not dataset:
		return None
	X,y,last_close= dataset
	last_row= X.iloc[[-1]]
	xgb= XGBRegressor(n_estimators=200,max_depth=4,learning_rate=0.05)
	xgb.fit(X,y)
	xgb_pred= float(xgb.predict(last_row)[0])
	rf= RandomForestRegressor(n_estimators=150,max_depth=6,random_state=42)
	rf_pred= _predict_with(rf,X,y,last_row)
	lr_pred= _predict_with(LinearRegression(),X,y,last_row)
	svm_pred= _predict_with(SVR(kernel="rbf",C=10,epsilon=0.1),X,y,last_row,scale=True)
	return {
		"last_close": last_close,
		"xgb_model": xgb,
		"xgb_features": X,
		"predictions": {
			"xgboost": xgb_pred,
			"random_forest": rf_pred,
			"linear_regression": lr_pred,
			"svm": svm_pred,
		},
	}