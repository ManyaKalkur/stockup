import numpy as np, pandas as pd, torch, torch.nn as nn
from ml_service.indicators import add_indicators
from ml_service.xgb_model import FEATURES

SEQ_LEN= 20

class LSTMForecaster(nn.Module):
	def __init__(self, n_features, hidden=32):
		super().__init__()
		self.lstm= nn.LSTM(n_features,hidden,batch_first=True)
		self.fc= nn.Linear(hidden,1)
	def forward(self,x):
		out,_= self.lstm(x)
		return self.fc(out[:,-1,:])

def make_sequences(X:np.ndarray, y:np.ndarray, seq_len=SEQ_LEN):
	xs,ys= [],[]
	for i in range(len(X)-seq_len):
		xs.append(X[i:i+seq_len])
		ys.append(y[i+seq_len])
	return np.array(xs), np.array(ys)

def train_lstm(rows:list, epochs=30):
	df= pd.DataFrame(rows)
	df= add_indicators(df)
	df["target"]= df["close"].shift(-1)
	df= df.dropna()
	if len(df)<SEQ_LEN+30:
		return None
	X_raw= df[FEATURES].values
	y_raw= df["target"].values
	mean,std= X_raw.mean(0), X_raw.std(0)+1e-9
	X_norm= (X_raw-mean)/std
	X_seq,y_seq= make_sequences(X_norm,y_raw)
	X_t= torch.tensor(X_seq,dtype=torch.float32)
	y_t= torch.tensor(y_seq,dtype=torch.float32).unsqueeze(1)
	model= LSTMForecaster(n_features=X_t.shape[2])
	opt= torch.optim.Adam(model.parameters(),lr=0.01)
	loss_fn= nn.MSELoss()
	model.train()
	for _ in range(epochs):
		opt.zero_grad()
		pred= model(X_t)
		loss= loss_fn(pred,y_t)
		loss.backward()
		opt.step()
	model.eval()
	last_seq= torch.tensor(X_norm[-SEQ_LEN:],dtype=torch.float32).unsqueeze(0)
	with torch.no_grad():
		pred= model(last_seq).item()
	return {"prediction":float(pred),"last_close":float(df["close"].iloc[-1]),"final_loss":float(loss.item())}