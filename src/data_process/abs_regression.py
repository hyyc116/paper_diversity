import sys

sys.path.append('src')
from basic_config import *

import pandas as pd

from linearmodels import PanelOLS
import itertools as it

# 筛选数据
def regress_FE(N=10):

    data = pd.read_csv('data/ABS_ALLdata.csv')

    data10 = data[data['year']<=(2019-N)]

    control_variables = [
        "teamsize", "age_mean", "age_std", "pnum_mean", "pnum_std", "cn_mean",
        "cn_std", "rank_mean", "rank_std", "num_of_refs"
    ]
    fixed_effects = ['journal_id','year']

    independent_variables = [
        "freshness_DIV", f"c{N}_DIV", f"d{N}_DIV"
        "subject_DIV", "variety", "balance", "disparsity", "impact_diversity"
    ]

    dependent_variables = [f'c{N}',f'd{N}']

    ALLVS= []
    ALLVS.extend(independent_variables)
    ALLVS.extend(control_variables)
    ALLVS.extend(fixed_effects)
    ALLVS.extend(independent_variables)

    data10 = pd.DataFrame(data=data10, columns=ALLVS)

    model_name = "Model"
    model_count = 0
    for _N in range(1,len(independent_variables)+1):
        for v in it.combinations(independent_variables,_N):
            Varis=[]
            Varis.extend(control_variables)
            Varis.extend(v)

            data10 = data10.reset_index().set_index(fixed_effects, append=True)

            for dv in dependent_variables:
                model_count+=1
                model_name +=str(model_count)
                res = POLS(data, dv, Varis, includeFixed=False,includeTime=False)

                print_result(res)

                model_count += 1
                model_name += str(model_count)
                res = POLS(data,
                           dv,
                           Varis,
                           includeFixed=True,
                           includeTime=False)

                model_count+=1
                model_name += str(model_count)
                res = POLS(data, dv, Varis, includeFixed=False,includeTime=True)

                model_count += 1
                model_name += str(model_count)
                res = POLS(data,
                           dv,
                           Varis,
                           includeFixed=True,
                           includeTime=True)


def print_result(model_name,res,ALLVs,include_fixed=False,include_time=False):

    R2 = res.rsquared
    params = res.params
    pvs = res.pvalues
    print(params.__class__)
    print(pvs.__class__)
    # for v in ALLVs:







def POLS(data,y,xs,includeFixed=False,includeTime=False):
    xs_str = ' + '.join(xs)
    formula = f'{y} ~ {xs_str} + 1'
    print(formula)
    if includeFixed:
        formula += '+ EntityEffects'
    if includeTime:
        formula += '+ TimeEffects'
    mod = PanelOLS.from_formula(formula, data=data)
    if includeFixed:
        ori = mod.fit(cov_type='clustered', cluster_entity=True)
    else:
        ori = mod.fit()
    # print("Formula:"+formula)
    # print(ori.params)
    # print(ori.pvalues)
    # print(ori.rsquared_overall)
    # print('\n')

    return ori


if __name__ =="__main__":

    regress_FE()
