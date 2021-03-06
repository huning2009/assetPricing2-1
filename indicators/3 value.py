# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-22  15:07
# NAME:assetPricing2-3 value.py
from data.outlier import detect_outliers
from dout import read_df
from zht.utils.mathu import get_inter_frame
import numpy as np
import pandas as pd

from data.dataTools import save, read_unfiltered, \
    quaterly2monthly


#compare the bps of wind with bv of gta
def compare_wind_gta_bps():
    '''
    the result is different a lot!!!

    :return:
    '''
    bps_wind=read_unfiltered('bps_wind')
    # bps_wind=load_data('bps_wind')
    # bps=load_data('bps')
    bps=read_unfiltered('bps')
    # bps_wind.columns=[str(int(col[:-3])) for col in bps_wind.columns] #this method will lead to the missing of columns.name
    bps_wind.columns=pd.Index([str(int(col[:-3])) for col in bps_wind.columns],
                                     name=bps_wind.columns.name)

    bps_wind=bps_wind.sort_index(axis=1)
    bps=bps.sort_index(axis=1)
    bps_wind,bps=get_inter_frame([bps_wind,bps])

    detect_outliers(bps_wind,'a1')
    detect_outliers(bps,'a2')

def get_bm():
    '''
    this function can be bookmarked as a snippet of how to manipulate date index
    in Pandas

    A little different with the book,here we use be and me for one share,
    but the data in the book is for all floating shares.However,it doesn't
    affect the bm.

    :return:
    '''
    # be=load_data('bps')
    be=read_unfiltered('bps')
    be=be[be.index.month==12]
    me=read_unfiltered('stockCloseY')
    # me=load_data('stockCloseY')
    be,me=get_inter_frame([be,me])
    # me[me<=0]=np.nan
    bm=be/me
    bm[bm<=0]=np.nan #delete those samples with bm<0
    bm=quaterly2monthly(bm, shift='6M')
    logbm=np.log(bm)

    bm=bm.stack()
    logbm=logbm.stack()
    x=pd.concat([bm,logbm],axis=1,keys=['bm','logbm'])
    x.index.names=['t','sid']
    x.columns.name='type'

    save(x,'value')

if __name__ == '__main__':
    get_bm()

