#coding:utf-8
'''
    ploting all figs from data folder
'''

from basic_config import *

def plotting_from_data_folder():
    ### basic statistic data
    logging.info('plotting statistics from data folder')
    stats_fig_data = json.loads(open('data/data_of_figs/stats_fig_data.json').read())

    xs,ys = stats_fig_data['wos_stats_cc'] 
    plt.plot(xs,ys,'o',fillstyle='none',c=color_sequence[0], linewidth=2)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('number of citations')
    plt.ylabel('number of publications')
    plt.xlim(0.9,10**5)
    plt.ylim(0.9,10**6)

    plt.tight_layout()
    plt.savefig('pdf/figs/wos_stats_cc.jpg',dpi=400)

    logging.info('Plotting number of publications VS. published year ...')
    fig,ax2 = plt.subplots(figsize=(6,4))

    xs,ys = stats_fig_data['number_of_papers'] 
    # print xs
    # print ys
    l2 = ax2.plot(xs,ys,label='number of publications',c=color_sequence[0], linewidth=2)
    ax2.set_xlabel('published year')
    ax2.set_ylabel('number of publications')
    ax2.set_yscale('log')

    ## average citation count VS. published year
    ax3 = ax2.twinx()
    xs,ys = stats_fig_data['average_citation']

    l3 = ax3.plot(xs,ys,label='average number of citation',c='r', linewidth=2)

    l4 = ax3.plot([2004]*10,np.linspace(0,np.max(ys),10),'--',c=color_sequence[2],label='year=2004')

    ax3.set_ylabel('average number of citations')
    ax3.set_yscale('log')

    ls = l2+l3+l4
    labels = [l.get_label() for l in ls]

    ax2.legend(ls,labels,loc=4)

    plt.tight_layout()
    plt.savefig('pdf/figs/wos_stats_year.jpg',dpi=400)

    # ## t2: number of publications VS. number of references
    # ax4 = axes[2]
    fig,ax = plt.subplots(figsize=(6,4))
    xs,ys = stats_fig_data['wos_stats_refs']
    logging.info('Plotting number of papers VS. number of references ...')
    ax.plot(xs,ys,c=color_sequence[0], linewidth=2)
    ax.plot([2]*10,np.linspace(0,np.max(ys),10),'--',label='x=2')
    ax.set_xlabel('number of references')
    ax.set_ylabel('number of publications')
    ax.set_xscale('log')
    ax.set_xlim(0.9,3*10**2)
    ax.legend()
    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True) 
    formatter.set_powerlimits((-1,1)) 
    ax.yaxis.set_major_formatter(formatter) 
    plt.tight_layout()
    plt.savefig('pdf/figs/wos_stats_refs.jpg',dpi=400)

    ### temporal diversity changes 

    # citation count diversity
    group_xys = json.loads(open('data/data_of_figs/temporal_citation_count_diversity_xys.json').read())
    plt.figure(figsize=(6,4))
    for i,group in enumerate(group_xys.keys()):
        xs,ys = group_xys[group]
        plt.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)

    plt.xlabel('published year')
    plt.ylabel('average citation count diversity')
    plt.legend(loc=4)
    plt.tight_layout()
    plt.savefig('pdf/figs/temporal_citation_count_diversity.jpg',dpi=400)
    logging.info('saved to pdf/figs/temporal_citation_count_diversity.jpg')


    ## subject diversity
    group_xys = json.loads(open('data/data_of_figs/temporal_subject_diversity_xys.json').read())


    plt.figure(figsize=(6,4))
    for i,group in enumerate(group_xys.keys()):
        xs,ys = group_xys[group]
        plt.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)
    plt.xlabel('published year')
    plt.ylabel('average subject diversity')
    plt.legend(loc=4)
    plt.tight_layout()
    plt.savefig('pdf/figs/temporal_subject_diversity.jpg',dpi=400)
    logging.info('saved to pdf/figs/temporal_subject_diversity.jpg')

    ## year diversity
    group_xys = json.loads(open('data/data_of_figs/temporal_year_differences_diversity_xys.json').read())
    plt.figure(figsize=(6,4))
    for i,group in enumerate(group_xys.keys()):
        xs,ys = group_xys[group]
        plt.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)

    plt.xlabel('published year')
    plt.legend(loc=4)
    plt.ylabel('average year differences diversity')
    plt.tight_layout()
    plt.savefig('pdf/figs/temporal_year_difference_diversity.jpg',dpi=400)
    logging.info('saved to pdf/figs/temporal_year_difference_diversity.jpg')


    ### basic diversity distribution
    fig_data = json.loads(open('data/data_of_figs/three_diversity_values.json').read())
    cc_diversity_values = fig_data['cc']
    subject_diversity_values = fig_data['subject']
    year_differences_diversity_values = fig_data['year']

    plt.figure(figsize=(6,4))
    plt.hist(cc_diversity_values,bins=30)   
    plt.xlabel('impact diversity')
    plt.ylabel('number of publications')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/figs/impact_diversity_dis.jpg',dpi=400)

    plt.figure(figsize=(6,4))
    plt.hist(subject_diversity_values,bins=30)    
    plt.xlabel('subject diversity')
    plt.ylabel('number of publications')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/figs/subject_diversity_dis.jpg',dpi=400)

    plt.figure(figsize=(6,4))
    plt.hist(year_differences_diversity_values,bins=30)   
    plt.xlabel('year diversity')
    plt.ylabel('number of publications')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/figs/year_differences_diversity_dis.jpg',dpi=400)

    ### relation between fields and relations
    # open('data/data_of_figs/diversity_impact_data.json','w').write(json.dumps(fig_data))


if __name__ == '__main__':
	plotting_from_data_folder()






















