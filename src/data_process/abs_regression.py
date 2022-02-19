import sys

sys.path.append('src')
from basic_config import *

import pandas as pd

from linearmodels import PanelOLS

# 筛选数据
def regress_FE():

    data = pd.read_csv('data/ABS_ALLdata.csv')

    data.set_index(['paper id','journal id'])

    print(data.describe())

    mod = PanelOLS.from_formula("invest ~ value + capital + EntityEffects", data=data)
    
    print(mod.fit())

if __name__ =="__main__":

    regress_FE()
