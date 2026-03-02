import os
from astropy.io import fits

def organize(directory):
    path = '../IoData/'
    files = os.listdir(path+directory)
    files.sort()
    with open(directory+'files'+'.txt', 'w') as r:
        for f in files:
            hdul = fits.open(path+directory+'/'+f)
            date = hdul[0].header['DATE_OBS']
            #r.write('Date' + ": " + date)
            gflt = hdul[0].header['GFLT']
            #r.write('GFLT' + ": " + gflt)
            ob = hdul[0].header['OBJECT']
            r.write('     '+f+ '      Date' + ": " + date + '     GFLT' + ": " + gflt + '     Object' + ": " + ob + '\n')


organize('190625')
