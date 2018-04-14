#coding:utf-8
'''
	ploting all figs from data folder
'''

from basic_config import *

	### basic statistic data
    open('data/data_of_figs/stats_fig_data.json','w').write(json.dumps(fig_data))
	
	### temporal diversity changes 
    open('data/data_of_figs/temporal_citation_count_diversity_xys.json','w').write(json.dumps(group_xys))
    open('data/data_of_figs/temporal_subject_diversity_xys.json','w').write(json.dumps(group_xys))
    open('data/data_of_figs/temporal_year_differences_diversity_xys.json','w').write(json.dumps(group_xys))

    ### basic diversity distribution
    open('data/data_of_figs/three_diversity_values.json','w').write(json.dumps(fig_data))

    ### relation between fields and relations
    open('data/data_of_figs/diversity_impact_data.json','w').write(json.dumps(fig_data))
