import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

file = pd.read_excel('othergraphs.xlsx')

x1_axis = file['Udate']
y1_axis = file['Ulp']
x2_axis = file['Kdate']
y2_axis = file['Klp']
x3_axis = file['Ldate']
y3_axis = file['Llp']
x4_axis = file['Cdate']
y4_axis = file['Clp']
x5_axis = file['Zdate']
y5_axis = file['Zlp']


plt.scatter(x1_axis, y1_axis, color='red', label='Dekleer Uta')
plt.scatter(x2_axis, y2_axis, color='orange', label='Dekleer Kanehekili')
plt.scatter(x3_axis, y3_axis, color='yellow', label='Dekleer Laki-Oi')
plt.scatter(x4_axis, y4_axis, color='green', label='Dekleer Chalybes')
plt.scatter(x5_axis, y5_axis, color='blue', label='Dekleer Zal')


plt.legend(loc='upper right')
#plt.axvline(datetime.datetime(), color='k')


plt.xlabel("Year")


plt.xlabel("Year")
plt.ylabel("Flux GW/micro/sr")
plt.show()
