from ml_service.models import train_all
from tests.helpers import make_rows

def test_train_all_returns_none_on_insufficient_data():
	assert train_all(make_rows(10)) is None

def test_train_all_returns_all_four_predictions():
	result= train_all(make_rows(120))
	assert result is not None

	preds= result["predictions"]
	for key in ["xgboost","random_forest","linear_regression","svm"]:
		assert key in preds
		assert isinstance(preds[key], float)

	assert isinstance(result["last_close"], float)
	assert "xgb_model" in result
	assert "xgb_features" in result