
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

file = pd.read_excel('rightone.xlsx')
ifile = pd.read_excel('IRTFData.xlsx')

x1_axis = file['date1']
y1_axis = file['lp1']
x2_axis = file['date2']
y2_axis = file['lp2']

ix1_axis = ifile['Jdate']
iy1_axis = ifile['Jcorrected brightness']
ix2_axis = ifile['Udate']
iy2_axis = ifile['Ucorrected brightness']

plt.scatter(x1_axis, y1_axis, color='red', label='Dekleer Uta')
plt.scatter(x2_axis, y2_axis, color='blue', label='Dekleer Janus')

plt.scatter(ix1_axis, iy1_axis, color='green', label='IRTF Janus')
plt.scatter(ix2_axis, iy2_axis, color='orange', label='IRTF Uta')

plt.legend(loc='upper right')
#plt.axvline(datetime.datetime(), color='k')


plt.xlabel("Year")
plt.ylabel("Flux GW/micro/sr")
plt.show()
