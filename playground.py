import pandas as pd

df = pd.DataFrame(columns = ['close'])
close = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
df['close'] = close
data_close = df['close']
ma = data_close.rolling(window=20).mean()[len(data_close) - 1]
std = data_close.std()