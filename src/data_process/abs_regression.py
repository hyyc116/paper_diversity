import sys

sys.path.append('src')
from basic_config import *

import pandas as pd

from linearmodels import PanelOLS

# 筛选数据
def regress_FE():

    data = pd.read_csv('data/ABS_ALLdata.csv')

    data10 = data[data['year']<2010]
    print(data10.describe())

    data.set_index(['year', 'journal id'])
    mod = PanelOLS.from_formula("c10 ~ teamsize + age_mean + age_std + rank_mean + rank_std", data=data10)

    print(mod.fit())

if __name__ =="__main__":

    regress_FE()
