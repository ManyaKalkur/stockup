from fastapi import WebSocket
import asyncio, yfinance as yf

class ConnectionManager:
	def __init__(self):
		self.active: dict[str,list[WebSocket]] = {}

	async def connect(self, symbol:str, ws:WebSocket):
		await ws.accept()
		self.active.setdefault(symbol,[]).append(ws)

	def disconnect(self, symbol:str, ws:WebSocket):
		if symbol in self.active and ws in self.active[symbol]:
			self.active[symbol].remove(ws)
			if not self.active[symbol]:
				del self.active[symbol]

	async def broadcast(self, symbol:str, data:dict):
		for ws in self.active.get(symbol,[]):
			try:
				await ws.send_json(data)
			except Exception:
				pass

manager = ConnectionManager()

async def price_poll_loop(symbol:str, interval:int=5):
	t= yf.Ticker(symbol)
	while symbol in manager.active:
		try:
			price= t.fast_info["last_price"]
			await manager.broadcast(symbol,{"symbol":symbol,"price":price})
		except Exception:
			pass
		await asyncio.sleep(interval)