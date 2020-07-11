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


    total = np.sum(ys)

    low_sum = 0
    medium_sum = 0
    high_sum = 0

    for i,x in enumerate(xs):

        if x < 64:
            low_sum+=ys[i]

        elif x < 985:

            medium_sum += ys[i]

        else:

            high_sum +=ys[i]

    print 'total:',total
    print 'low:',low_sum
    print 'medium:',medium_sum
    print 'high:',high_sum
    print 'other:', low_sum-medium_sum-high_sum



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
    
    print 'total number of publications:',np.sum(ys)
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
    fig,axes = plt.subplots(3,1,figsize=(6,12))
    group_xys = json.loads(open('data/data_of_figs/temporal_citation_count_diversity_xys.json').read())
    # plt.figure(figsize=(6,4))
    ax = axes[0]
    for i,group in enumerate(group_xys.keys()):
        xs,ys = group_xys[group]
        ax.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)

    ax.set_xlabel('published year\n(a)')
    ax.set_ylabel('average impact diversity')
    ax.legend(loc=4)
    # plt.tight_layout()
    # plt.savefig('pdf/figs/temporal_citation_count_diversity.jpg',dpi=400)
    # logging.info('saved to pdf/figs/temporal_citation_count_diversity.jpg')


    ## subject diversity
    group_xys = json.loads(open('data/data_of_figs/temporal_subject_diversity_xys.json').read())

    ax1 = axes[2]
    # plt.figure(figsize=(6,4))
    for i,group in enumerate(group_xys.keys()):
        xs,ys = group_xys[group]
        ax1.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)
    ax1.set_xlabel('published year\n(c)')
    ax1.set_ylabel('average subject diversity')
    ax1.legend(loc=4)
    # plt.tight_layout()
    # plt.savefig('pdf/figs/temporal_subject_diversity.jpg',dpi=400)
    # logging.info('saved to pdf/figs/temporal_subject_diversity.jpg')

    ## year diversity
    group_xys = json.loads(open('data/data_of_figs/temporal_year_differences_diversity_xys.json').read())
    # plt.figure(figsize=(6,4))
    ax2 = axes[1]
    for i,group in enumerate(group_xys.keys()):
        xs,ys = group_xys[group]
        ax2.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)

    ax2.set_xlabel('published year')
    ax2.legend(loc=4)
    ax2.set_ylabel('average published year diversity')
    
    plt.tight_layout()
    plt.savefig('pdf/figs/temporal_diversity.jpg',dpi=400)
    logging.info('saved to pdf/figs/temporal_diversity.jpg')


    ### basic diversity distribution
    fig,axes = plt.subplots(3,1,figsize=(6,12))
    three_diversity_values = json.loads(open('data/data_of_figs/three_diversity.json').read())
    n = three_diversity_values['cc']['n']
    bins = three_diversity_values['cc']['bins']
    bins = [float('{:2f}'.format(l)) for l in bins]
    width = np.max(bins)/(len(n)+5)

    # plt.figure(figsize=(6,4))
    ax = axes[0]
    ax.bar(bins[:-1],n,width=width,align='edge') 
    ax.set_xlabel('impact diversity\n(a)')
    ax.set_ylabel('number of publications')
    ax.set_yscale('log')
    # plt.tight_layout()
    # plt.savefig('pdf/figs/cc_diversity_dis.jpg',dpi=400)

    # plt.figure(figsize=(6,4))
    ax1 = axes[2]
    n = three_diversity_values['sd']['n']
    bins = three_diversity_values['sd']['bins']
    bins = [float('{:2f}'.format(l)) for l in bins]
    width = np.max(bins)/(len(n)+5)

    ax1.bar(bins[:-1],n,width=width,align='edge') 
    ax1.set_xlabel('subject diversity\n(c)')
    ax1.set_ylabel('number of publications')
    ax1.set_yscale('log')
    # plt.tight_layout()
    # plt.savefig('pdf/figs/subject_diversity_dis.jpg',dpi=400)


    # plt.figure(figsize=(6,4))
    ax2 = axes[1]
    n = three_diversity_values['yd']['n']
    bins = three_diversity_values['yd']['bins']
    bins = [float('{:2f}'.format(l)) for l in bins]
    width = np.max(bins)/(len(n)+5)


    ax2.bar(bins[:-1],n,width=width,align='edge') 
    ax2.set_xlabel('published year diversity\n(b)')
    ax2.set_ylabel('number of publications')
    ax2.set_yscale('log')

    plt.tight_layout()
    plt.savefig('pdf/figs/diversity_dis.jpg',dpi=400)

    
    ### relation between fields and relations
    # open('data/data_of_figs/diversity_impact_data.json','w').write(json.dumps(fig_data))

    dvs_imp_fig_data = json.loads(open('data/data_of_figs/diversity_impact_data.json').read())
    logging.info('plot citation count vs. impact diversity ...')

    xs,ys = dvs_imp_fig_data['cc_cd']
    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])
    plt.xlabel('citation count')
    plt.ylabel('average impact diversity')
    plt.tight_layout()
    plt.savefig('pdf/figs/cc_cd.jpg',dpi=400)

    xs,ys = dvs_imp_fig_data['cd_cc']
    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])
    plt.xlabel('impact diversity')
    plt.ylabel('average citation count')
    plt.tight_layout()
    plt.savefig('pdf/figs/cd_cc.jpg',dpi=400)

    logging.info('plot subject diversity vs. impact diversity ...')
    xs,ys = dvs_imp_fig_data['cc_sd']
    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])
    plt.xlabel('citation count')
    plt.ylabel('average subject diversity')
    plt.tight_layout()
    plt.savefig('pdf/figs/cc_sd.jpg',dpi=400)

    xs,ys = dvs_imp_fig_data['sd_cc']
    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])
    plt.xlabel('subject diversity')
    plt.ylabel('average citation count')
    plt.tight_layout()
    plt.savefig('pdf/figs/sd_cc.jpg',dpi=400)


    logging.info('plot year diversity vs. impact diversity ...')


    xs,ys = dvs_imp_fig_data['cc_yd']
    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])
    plt.xlabel('citation count')
    plt.ylabel('average year diversity')
    plt.tight_layout()
    plt.savefig('pdf/figs/cc_yd.jpg',dpi=400)


    xs,ys = dvs_imp_fig_data['ys_cc']
    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])
    plt.ylabel('average citation count')
    plt.xlabel('year diversity')
    plt.tight_layout()
    plt.savefig('pdf/figs/yd_cc.jpg',dpi=400)

    logging.info('Done ...')


if __name__ == '__main__':
    plotting_from_data_folder()






















