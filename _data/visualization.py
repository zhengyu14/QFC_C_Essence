import matplotlib.pyplot as plt
import pandas as pd

data1 = pd.read_csv('result_001_w_0010_2y.csv')
#data2 = pd.read_csv('result_001_w_0010_2y.csv')
data3 = pd.read_csv('result_002_w_90100_2y.csv')
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(data1['Datetime'], data1['Benchmark'], color='#678BC7', label='Benchmark')
ax.plot(data1['Datetime'], data1['Strategy'], color='#759421', label='Top 10%')
#ax.plot(data2['Datetime'], data2['Strategy'], color='#E09D00', label='')
ax.plot(data3['Datetime'], data3['Strategy'], color='#C14646', label='Bottom 10%')
ax.legend()
plt.show()