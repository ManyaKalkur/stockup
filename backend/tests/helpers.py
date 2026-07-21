def make_rows(n=60):
	rows= []
	price= 100.0
	for i in range(n):
		price+= 0.5 if i%2== 0 else -0.3
		rows.append({
			"date": f"2024-01-{i+1:02d}",
			"open": price,
			"high": price+1,
			"low": price-1,
			"close": price,
			"volume": 1_000_000 + i*1000,
		})
	return rows