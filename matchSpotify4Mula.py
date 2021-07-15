import pandas as pd
df = pd.read_parquet('4mula_tiny.parquet')

#percorrendo todas linhas do df
for index, row in df.iterrows():
	musicName=row['music_name']
	artName=row['art_name']

	