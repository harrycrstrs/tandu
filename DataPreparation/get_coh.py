import sys
sys.path.append('/home/s1332488/.snap/snap-python/')
from snappy import ProductIO as io
import glob
files = glob.glob('*HS*TC.dim')
import pandas as pd
import os.path as path
import os
import numpy as np

os.chdir('/disk/scratch/local.4/harry/TDX/ifg/topo')

df = pd.read_csv('/home/s1332488/Chapter3/peru_TDX_metadata.csv')
df['coh']=0

def get_data(imageBand):
    # takes SNAP image band object and returns a numpy array containing the data in that band
    W,H = imageBand.getRasterWidth(), imageBand.getRasterHeight()
    array = np.zeros(W*H)
    imageBand.readPixels(0,0,W,H,array)
    return array.reshape(H,W).transpose()

def get_coherence(f):
    im = io.readProduct(f)
    cohB = [x for x in list(im.getBandNames()) if 'coh' in x][0]
    coh = im.getBand(cohB)
    coh_data = get_data(coh)
    coh_vals = coh_data[coh_data >0]
    return coh_vals.mean()

for f in glob.glob('*.dim'):
    print(f)
    datetime = f.split('_')[3]
    df.at[df['file'].str.contains(datetime),'coh'] = get_coherence(f)
    
df.to_csv('/home/s1332488/Chapter3/metadataC.csv')
    
    

    
    