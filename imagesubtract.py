from copy import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from astropy.io import fits
from astropy.visualization import LinearStretch, LogStretch
from astropy.visualization import ZScaleInterval, MinMaxInterval
from astropy.visualization import ImageNormalize

from photutils.aperture import CircularAperture, ApertureStats, CircularAnnulus
from astropy.visualization import simple_norm


import numpy as np
import glob, os
import math

palette = copy(plt.cm.gray)
palette.set_bad('r', 0.75)
#import properimage.single_image as si
#from properimage.operations import subtract

#swarp_path="SWarp"
#os.system(swarp_path)

stref_path = '../IoData/190508/sgd.2019A040.190508.iorun.00001.a.fits' #BD+2D2957
stnew_path = '../IoData/190508/sgd.2019A040.190508.iorun.00002.b.fits'
Ioref_path = '../IoData/190508/sgd.2019A040.190625.iorun.00622.a.fits'
Ionew_path = '../IoData/190508/sgd.2019A040.190625.iorun.00223.b.fits'
flat = '../IoData/flat0622.fits'
# My directory is set up so I have IoData which contains all of the data and then folders per year which contain just the images and not the associated text files

#does image subtraction and divides by the flat field
def imgsubtract(ref_path,new_path):

    hdul = fits.open(ref_path) 
    hdul.verify('fix')
    data = hdul[0].data
    
    hdul1 = fits.open(new_path)
    hdul1.verify('fix')
    data1 = hdul1[0].data
    
    hdulflat = fits.open(flat)
    hdulflat.verify('fix')
    hdulflat = hdulflat[0].data
    
    size = hdul[0].header['NAXIS1']

    hdulflat = hdulflat[128:size+128,128:size+128]

    data2 = data/hdulflat-data1/hdulflat
    
    #take out # from these lines to show a specific image data2 should be replaced with the data set you want to display

    #plt.figure()
    #plt.imshow(data2, cmap='gray')
    #plt.show()
    return data2

print(imgsubtract(stref_path,stnew_path))

#finds the maximum value of the array and returns its position
def maxvalxy(ref_path,new_path):
    data = imgsubtract(ref_path,new_path)
    mymax = data[0][0]
    x = 0
    y = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if mymax < data[i][j]:
                mymax = data[i][j]
                x = j
                y = i
    #print(mymax)
    return(x, y)

print(maxvalxy(stref_path,stnew_path))

#calculates the instrument flux of the image
def f(ref_path,new_path):
    
    positions = maxvalxy(ref_path,new_path)
    aperone = CircularAperture(positions, r=2.5)
    apertwo = CircularAperture(positions,r=5)
    data = imgsubtract(ref_path,new_path)

    aperonestats = ApertureStats(data,aperone)
    aperonesum = aperonestats.sum
    
    apertwostats = ApertureStats(data,apertwo)
    apertwosum = apertwostats.sum
    f = 4/3*aperonesum - 1/3*apertwosum
    
    return f

print(f(stref_path,stnew_path))

#does the distance converstion calculation delta is in AU
def d(delta):
    d = delta*1.496*10**11
    return d

print(d(4.13))

#calculates the C_A by getting the airmass from the header of the images
def CA(stref_path, Ioref_path):
    
    hdul = fits.open(stref_path)
    hdul.verify('fix')
    amst = hdul[0].header['TCS_AM']

    hdul1 = fits.open(Ioref_path)
    hdul1.verify('fix')
    amIo = hdul1[0].header['TCS_AM']

    b = 0.09
    st = -b*amst
    Io = -b*amIo
    CA = np.exp(st)/np.exp(Io)
    return CA

print(CA(stref_path,Ioref_path))

#Opens up a file that contains the known star magnitude and parses through to find the correct magnitude
def stmag(path):

    hdul = fits.open(path)
    date = path.replace('../IoData/','')[0:5] #have to change the path to where image data is stored
    obj = hdul[0].header['OBJECT']
    with open('starmag.txt', 'r') as file:
        for l in file:
            data = l.split()
            if data[1] == obj:
                if data[0][0:3] == date:
                    return data[2]
                return data[2]
    with open('extrastarmag.txt', 'r') as file:
        for l in file:
            data = l.split()
            if data[0] == obj:
                return data[1]
    print("Star magnitude doesn't exist")

print(stmag(stref_path))

#returns the flux of Io
def brightness(stref_path,stnew_path,Ioref_path,Ionew_path):
    
    F_0 = 5.31*10**(-11.0)
    M_st = float(stmag(stref_path)) 
    f_Io = f(Ioref_path,Ionew_path)
    f_st = f(stref_path,stnew_path)
    C_A = CA(stref_path,Ioref_path)
    #print(M_st,f_Io,f_st,C_A)
    C_M = 0.993
    dist = d(4.308) #190625 = 4.308 190508 = 4.524
    #print(dist)
    F_I = F_0*10**(-M_st/2.5)*(f_Io/f_st)*C_A*C_M*dist**2.0
    return F_I/1000000000

print(brightness(stref_path,stnew_path, Ioref_path, Ionew_path))

#Finds all of the ab pairs for a single night and stores them in a dictionary with the first object of the dicitonary as the object name
def abpairs(date):
    
    path = '../IoData/'
    files = os.listdir(path+date)
    files.sort()
    lastfile = files[0]
    Io = {'obj' :'Io (501)'}
    ls = [Io]
    for f in files:
        hdul = fits.open(path+date+'/'+f)
        gflt = hdul[0].header['GFLT']
        ob = hdul[0].header['OBJECT']
        com = hdul[0].header['COMMENT']
        hdullast = fits.open(path+date+'/'+lastfile)
        oblast = hdullast[0].header['OBJECT']
        gfltlast = hdullast[0].header['GFLT']
        obin = False
        if lastfile.endswith(".a.fits") and f.endswith(".b.fits") and gflt == 'Lp' and gflt == gfltlast and ob == oblast:
            for l in ls:
                if l['obj'] == ob:
                    l[lastfile] = f
                    obin = True
            if obin == False:
                newdict = {}
                newdict['obj'] = ob
                newdict[lastfile] = f
                ls.append(newdict)

        lastfile = f
        obin = False

    return ls #returns a list of all of the dictionaries 

print(abpairs('190508')) #data always has to be in quotes

#This just creates a new file for any night that lists the img number obj name etc.
def instrumagflux(date):
    #image number, obj name, airmass, instrumag and instruflux
    ls = abpairs(date)
    #print(len(ls),len(ls[0]),len(ls[1]),len(ls[2]))
    path = '../IoData/' + date + '/'
    with open(date + 'flugmag.txt', 'w') as r: 
        for i in range(len(ls)):
            for k in ls[i]:
                if k != 'obj':
                    flux = f(path+k,path+ls[i].get(k))
                    hdul = fits.open(path+k)
                    ob = hdul[0].header['OBJECT']
                    airmass = hdul[0].header['TCS_AM']
                    mag = -2.5*math.log(flux)
                    r.write('Img Pair: '+ k + ' ,' + ls[i].get(k) + '     Object' + ": " + ob + '     Airmass:' + str(airmass) + '     Instru Flux: ' + str(flux) + '     Instru Mag:' + str(mag) + '\n')

#instrumagflux('190625')

#Not needed just for trial
def test():
    path = '../IoCode/'
    for file in os.listdir(path):
        if file.endswith("files.txt"):
            print(file)

#This calculates the average flux/brightness of Io for the night by taking the list of all the ab pairs and putting them in the brightness function and averaging the value
def avgbrightness(date):
    ls = abpairs(date)
    path = '../IoData/' + date + '/'
    sumbright = 0
    totalbright = 0
    '''maxlen = len(ls[1])
    stdstar = ls[1]
    for i in range(len(ls)-1):
        if len(ls[i+1]) > maxlen:
            stdstar = ls[i+1]
        

    #print(len(ls),len(ls[0]),len(ls[1]),len(ls[2]))
    path = '../IoData/' + date + '/'
    sumbright = 0
    totalbright = 0

    for k in ls[0]:
        if k != 'obj':
            for j in ls[1]:
                if j != 'obj':
                    #print(k,stdstar.get(j))
                    #print(path+j,path+stdstar.get(j),path+k,path+stdstar.get(k))
                    sumbright = sumbright + brightness(path+j,path+ls[1].get(j),path+k,path+ls[0].get(k))
                    totalbright = totalbright + 1'''

    for i in range(len(ls)-1):
        for k in ls[0]:
            if k != 'obj':
                for j in ls[i+1]:
                    #print(j)
                    if j != 'obj':
                       # print([path+j,path+ls[i+1].get(j),path+k,path+ls[0].get(k)])
                        sumbright = sumbright + brightness(path+j,path+ls[i+1].get(j),path+k,path+ls[0].get(k))
                        totalbright = totalbright + 1
    avg = sumbright/totalbright
    print(sumbright)
    print(totalbright)
    return avg
            
#print(brightness('../IoData/190625/sgd.2019A040.190625.iorun.00365.a.fits', '../IoData/190625/sgd.2019A040.190625.iorun.00366.b.fits', '../IoData/190625/sgd.2019A040.190625.iorun.00141.a.fits', '../IoData/190625/sgd.2019A040.190625.iorun.00142.b.fits'))

print(avgbrightness('190625'))



'''annulus_aperture = CircularAnnulus(positions, r_in=2.95, r_out=5.9)
norm = simple_norm(data, 'sqrt', percent=99)
plt.imshow(data, norm=norm, interpolation='nearest')
plt.xlim(0, 250)
plt.ylim(0, 100)

ap_patches = aperone.plot(color='white', lw=2,
                           label='Photometry aperture')
ann_patches = annulus_aperture.plot(color='red', lw=2,label='Background annulus')
handles = (ap_patches[0], ann_patches[0])
plt.legend(loc=(0.17, 0.05), facecolor='#458989', labelcolor='white', handles=handles, prop={'weight': 'bold', 'size': 11})

plt.show()'''









