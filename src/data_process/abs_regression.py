from pickle import FALSE
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
        "freshness_DIV", f"c{N}_DIV", f"d{N}_DIV",
        "subject_DIV", "variety", "balance", "disparsity", "impact_diversity"
    ]

    dependent_variables = [f'c{N}',f'd{N}']

    ALLVS= []
    ALLVS.extend(independent_variables)
    ALLVS.extend(control_variables)
    ALLVS.extend(fixed_effects)
    ALLVS.extend(dependent_variables)

    VS = []
    VS.extend(independent_variables)
    VS.extend(control_variables)
    vs_str = ','.join(VS)


    data = pd.DataFrame(data=data10, columns=ALLVS)
    data = data.reset_index().set_index(fixed_effects)

    for dv in dependent_variables:
        model_count = 0
        lines = [f'dependents:{dv}']
        lines.append(f',{vs_str},journal fixed,Year fixed,R2,# of Smaples')

        for _N in range(1,len(independent_variables)+1):
            for v in it.combinations(independent_variables,_N):
                Varis=[]
                Varis.extend(control_variables)
                Varis.extend(v)

                model_count+=1
                model_name ="Model "+str(model_count)
                res = POLS(data, dv, Varis, includeFixed=False,includeTime=False)

                line = print_result(model_name,res,VS,False,False)
                lines.append(line)

                model_count += 1
                model_name ="Model "+str(model_count)
                res = POLS(data,
                        dv,
                        Varis,
                        includeFixed=True,
                        includeTime=False)

                line = print_result(model_name, res, VS, True, False)
                lines.append(line)

                model_count+=1
                model_name ="Model "+str(model_count)
                res = POLS(data, dv, Varis, includeFixed=False,includeTime=True)

                line = print_result(model_name, res, VS, False, True)
                lines.append(line)

                model_count += 1
                model_name ="Model "+str(model_count)
                res = POLS(data,
                        dv,
                        Varis,
                        includeFixed=True,
                        includeTime=True)

                line = print_result(model_name, res, VS, True, True)
                lines.append(line)
        
        open(f'data/regression_{dv}_{N}.result.csv','w').write('\n'.join(lines))
        logging.info(f'{dv}_{N} regression saved')
    
    logging.info(F'{N} Done')
            


def print_result(model_name,res,ALLVs,include_fixed=False,include_time=False):

    R2 = res.rsquared
    nobs = res.nobs
    params = res.params
    pvs = res.pvalues
    vs = []
    for v in ALLVs:
        if v in params:
            vs.append('{:.4f}({:})'.format(params[v],sig_star(pvs[v])))
        else:
            vs.append('--')

    return model_name+','+','.join(vs)+','+str(include_fixed)+','+str(include_time)+','+str(R2)+','+str(nobs)



def sig_star(p):
    if p>0.05:
        return ""
    elif p<=0.0001:
        return "****"
    elif p<0.001:
        return "***"
    elif p<0.01:
        return "**"
    elif p<0.05:
        return "*"


def POLS(data,y,xs,includeFixed=False,includeTime=False):
    # xs_str = ' + '.join(xs)
    # formula = f'{y} ~ {xs_str} + 1'
    # print(formula)
    # print(data['c10'].head())
    # if includeFixed:
    #     formula += '+ EntityEffects'
    # if includeTime:
    #     formula += '+ TimeEffects'
    # mod = PanelOLS.from_formula(formula, data=data)
    # if includeFixed:
    #     ori = mod.fit(cov_type='clustered', cluster_entity=True)
    # else:
    #     ori = mod.fit()
    # print("Formula:"+formula)
    # print(ori.params)
    # print(ori.pvalues)
    # print(ori.rsquared_overall)
    # print('\n')

    # data = data.dropna()
    print(xs)

    exog = sm.add_constant(data[xs])
    res = PanelOLS(data[y],exog,entity_effects = includeFixed, time_effects = includeTime).fit()
    return res


if __name__ =="__main__":

    regress_FE(10)
    regress_FE(5)
    regress_FE(2)

