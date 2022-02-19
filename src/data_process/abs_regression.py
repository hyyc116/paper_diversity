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

    # data10.set_index(['year', 'journal_id'])
    # mod = PanelOLS.from_formula("c10 ~ teamsize + age_mean + age_std + rank_mean + rank_std", data=data10)

    exog_vars = ["teamsize", "age_mean", "age_std", "rank_mean", "rank_std"]
    exog = sm.add_constant(data[exog_vars])
    mod = PanelOLS(data.c10, exog, entity_effects=False)
    fe_res = mod.fit()
    print(fe_res)


if __name__ =="__main__":

    regress_FE()
