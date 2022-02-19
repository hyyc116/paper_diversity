import sys

sys.path.append('src')
from basic_config import *

import pandas as pd

from linearmodels import PanelOLS

# 筛选数据
def regress_FE():

    data = pd.read_csv('data/ABS_ALLdata.csv')

    data10 = data[data['year']<2010]

    data10 = pd.DataFrame(data=data10,columns=["year","journal_id","teamsize", "age_mean", "age_std", "rank_mean", "rank_std","c10","c2","c5","d10"])

    print(data10.describe())

    data10 = data10.set_index(['journal_id','year'],append=False)
    # data10 = data10.set_index(['year'], append=True)

    POLS(data10, 'c10',
         ["teamsize", "age_mean", "age_std", "rank_mean", "rank_std"],False,False)

    POLS(data10, 'c10',
         ["teamsize", "age_mean", "age_std", "rank_mean", "rank_std"], True,
         False)

    POLS(data10, 'c10',
         ["teamsize", "age_mean", "age_std", "rank_mean", "rank_std"], False,
         True)

    POLS(data10, 'c10',
         ["teamsize", "age_mean", "age_std", "rank_mean", "rank_std"], True,
         True)






    # exog_vars = ["teamsize", "age_mean", "age_std", "rank_mean", "rank_std"]
    # exog = sm.add_constant(data10[exog_vars])
    # mod = PanelOLS(data10.c10, exog, entity_effects=False)
    # fe_res = mod.fit()
    # print(fe_res)

    # mod = PanelOLS(data10.c10, exog, entity_effects=True)
    # fe_res = mod.fit()
    # print(fe_res)

    # mod = PanelOLS(data10.c10, exog, time_effects=True)
    # fe_res = mod.fit()
    # print(fe_res)

    # mod = PanelOLS(data10.c10, exog, entity_effects=True, time_effects=True)
    # fe_res = mod.fit()
    # print(fe_res)


def POLS(data,y,xs,includeFixed=False,includeTime=False):
    xs_str = ' + '.join(xs)
    formula = f'{y}~{xs_str} + 1'
    if includeFixed:
        formula += '+ EntityEffects'
    if includeTime:
        formula += '+ TimeEffects'
    print(formula)
    mod = PanelOLS.from_formula(formula, data=data)
    ori = mod.fit()
    print(formula)
    print(ori.params)
    print(ori.pvalues)
    print(ori.rsquared_overall)
    print('\n')


if __name__ =="__main__":

    regress_FE()
