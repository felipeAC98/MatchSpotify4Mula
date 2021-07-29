import pandas as pd
df = pd.read_parquet('4mula_metadata.parquet')

for item in df:
	print(item)