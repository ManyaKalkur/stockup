from ml_service.features import build_dataset, FEATURES
from tests.helpers import make_rows

def test_build_dataset_returns_none_for_short_history():
	assert build_dataset(make_rows(20)) is None

def test_build_dataset_returns_correct_shapes():
	result= build_dataset(make_rows(120))
	assert result is not None
	X, y, last_close= result
	assert list(X.columns)== FEATURES
	assert len(X)== len(y)
	assert isinstance(last_close, float)