import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

file = pd.read_excel('othergraphs.xlsx')
ifile = pd.read_excel('rightone.xlsx')

x1_axis = file['Udate']
y1_axis = file['Ulp']
x2_axis = file['Cdate']
y2_axis = file['Clp']
x3_axis = ifile['date2']
y3_axis = ifile['lp2']


plt.scatter(x1_axis, y1_axis, color='red', label='Dekleer Uta')
plt.scatter(x2_axis, y2_axis, color='orange', label='Dekleer Chalybes')
plt.scatter(x3_axis, y3_axis, color='yellow', label='Dekleer Janus')

plt.legend(loc='upper right')
#plt.axvline(datetime.datetime(), color='k')


plt.xlabel("Year")


plt.xlabel("Year")
plt.ylabel("Flux GW/micro/sr")
plt.show()


#jul 21st 2017 Janus :8.6, Uta : 6.6, chaylbes : 7.5
#jul 19 2017 our data: 
