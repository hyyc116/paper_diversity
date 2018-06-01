#coding:utf-8
'''
    calculate diversity of papers.

'''
from basic_config import *


def cal_diversity(com_ids_cc_path,com_ids_subjects_path,selected_IDs_references_path,year_differences_path,com_IDs_year_path,subject_sim_path):

    logging.info('loading com_ids_cc ...')
    com_ids_cc = json.loads(open(com_ids_cc_path).read())

    logging.info('loading com_ids_subjects ...')
    com_ids_subjects = json.loads(open(com_ids_subjects_path).read())

    logging.info('loading papers and references ...')
    selected_IDs_references = defaultdict(list)
    selected_IDs_references_num = defaultdict(int)
    for line in open(selected_IDs_references_path):
        line = line.strip()
        pid,ref_id = line.split("\t")
        selected_IDs_references[pid].append(ref_id)
        selected_IDs_references_num[pid]+=1


    open('data/selected_IDs_references_num.json','w').write(json.dumps(selected_IDs_references_num))

    com_ids_year = json.loads(open(com_IDs_year_path).read())

    subject_sim = json.loads(open(subject_sim_path).read())

    cc_pid_diversity=defaultdict(float)
    subject_pid_diversity = defaultdict(float)

    selected_IDs = selected_IDs_references.keys()
    length = len(selected_IDs)

    selected_IDs_cc = {}

    for i,pid in enumerate(selected_IDs):

        if (i+1)%100000==0:
            logging.info('progress {:}/{:} ...'.format((i+1),length))

        ## published years
        if int(com_ids_year.get(pid,9999))>2004:
            continue

        ## the number of references
        if len(selected_IDs_references[pid])<2:
            continue

        selected_IDs_cc[pid] = com_ids_cc.get(pid,-1)

        # subject = 

        cc_list = []
        subject_list = []

        pid_subjects = com_ids_subjects.get(pid,[])

        for ref_id in selected_IDs_references[pid]:

            if '.' in ref_id:
                continue

            cc = com_ids_cc.get(ref_id,0)

            ref_subjects = com_ids_subjects.get(ref_id,[])

            cc_list.append(cc)

            s_sim = 0
            for ps in pid_subjects:
                for rs in ref_subjects:
                    key = '\t'.join(sorted([ps,rs]))
                    ss = subject_sim[key]
                    if ss>s_sim:
                        s_sim = ss

            subject_list.append(float('{:.10f}'.format(s_sim)))

        # print cc_list
        if len(cc_list)>0:
            cc_gini = gini(cc_list)
            cc_pid_diversity[pid] = cc_gini

        if len(subject_list)>0:
            subject_gini = gini(subject_list)
            subject_pid_diversity[pid] = subject_gini



    open('data/selected_IDs_cc.json','w').write(json.dumps(selected_IDs_cc))
    # open('data/selected_IDs_references_num.json','w').write(json.dumps(selected_IDs_references_num))

    open('data/wos_cc_diversity.json','w').write(json.dumps(cc_pid_diversity))
    logging.info("saved to data/wos_cc_diversity.json.")

    open('data/wos_subject_diversity.json','w').write(json.dumps(subject_pid_diversity))
    logging.info('saved to data/wos_subject_diversity.json')

    year_differences = json.loads(open(year_differences_path).read())

    yd_pid_diversity = defaultdict(float)
    for pid in year_differences.keys():

        ## published years
        if int(com_ids_year.get(pid,9999))>2004:
            continue

        ## the number of references
        if len(selected_IDs_references[pid])<2:
            continue


        yd_pid_diversity[pid]=gini(year_differences[pid])

    open('data/wos_year_differences_diversity.json','w').write(json.dumps(yd_pid_diversity))
    logging.info('saved to data/wos_year_differences_diversity.json')

### plot line chart of papers at three levels, how three kinds of diversity changes over years
def plot_diversity_over_year(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path,com_ids_cc_path,com_IDs_year_path):
    ## ID_cc
    logging.info('loads citation count from {:} ...'.format(com_ids_cc_path))
    com_IDs_cc = json.loads(open(com_ids_cc_path).read())
    com_ids_year = json.loads(open(com_IDs_year_path).read())
    ### citation  count 的diversity的计算
    logging.info('loading data from diversity files ...')
    wos_cc_diversity = json.loads(open(wos_cc_diversity_path).read())
    wos_subject_diversity = json.loads(open(wos_subject_diversity_path).read())
    wos_year_differences_diversity = json.loads(open(wos_year_differences_diversity_path).read())

    # citation count diversity
    group_year_cc = defaultdict(lambda:defaultdict(list))
    for pid in wos_cc_diversity.keys():
        cc = com_IDs_cc.get(pid,0)
        year = int(com_ids_year.get(pid,-1))
        if year==-1:
            continue

        if cc< 64:
            group='low'
        elif cc<985:
            group='medium'
        else:
            group='high'


        cc_gini = wos_cc_diversity[pid]

        group_year_cc[group][year].append(cc_gini)
        group_year_cc['all'][year].append(cc_gini)

    group_xys = {}

    plt.figure(figsize=(6,4))
    for i,group in enumerate(group_year_cc.keys()):
        year_cc = group_year_cc[group]
        xs = []
        ys = []
        for year in sorted(year_cc.keys()):
            xs.append(year)
            ys.append(np.mean(year_cc[year]))

        plt.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)

        group_xys[group] = [xs,ys]

    open('data/data_of_figs/temporal_citation_count_diversity_xys.json','w').write(json.dumps(group_xys))

    plt.xlabel('published year')
    plt.ylabel('average citation count diversity')
    plt.legend(loc=4)
    plt.tight_layout()
    plt.savefig('pdf/temporal_citation_count_diversity.jpg',dpi=400)
    logging.info('saved to pdf/temporal_citation_count_diversity.jpg')


    ## subject diversity
    group_year_subj = defaultdict(lambda:defaultdict(list))
    for pid in wos_subject_diversity.keys():
        cc = com_IDs_cc.get(pid,0)
        year = int(com_ids_year.get(pid,-1))
        if year==-1:
            continue

        if cc< 64:
            group='low'
        elif cc<985:
            group='medium'
        else:
            group='high'


        subj_gini = wos_subject_diversity[pid]

        group_year_subj[group][year].append(subj_gini)
        group_year_subj['all'][year].append(subj_gini)

    group_xys={}

    plt.figure(figsize=(6,4))
    for i,group in enumerate(group_year_subj.keys()):
        year_subj = group_year_subj[group]
        xs = []
        ys = []
        for year in sorted(year_subj.keys()):
            xs.append(year)
            ys.append(np.mean(year_subj[year]))

        plt.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)

        group_xys[group] = [xs,ys]

    open('data/data_of_figs/temporal_subject_diversity_xys.json','w').write(json.dumps(group_xys))

    plt.xlabel('published year')
    plt.ylabel('average subject diversity')
    plt.legend(loc=4)
    
    plt.tight_layout()
    plt.savefig('pdf/temporal_subject_diversity.jpg',dpi=400)
    logging.info('saved to pdf/temporal_subject_diversity.jpg')

    ## year diversity
    group_year_year = defaultdict(lambda:defaultdict(list))
    for pid in wos_year_differences_diversity.keys():
        cc = com_IDs_cc.get(pid,0)
        year = int(com_ids_year.get(pid,-1))
        if year==-1:
            continue

        if cc< 64:
            group='low'
        elif cc<985:
            group='medium'
        else:
            group='high'


        year_gini = wos_year_differences_diversity[pid]

        group_year_year[group][year].append(year_gini)
        group_year_year['all'][year].append(year_gini)

    plt.figure(figsize=(6,4))
    group_xys= {}
    for i,group in enumerate(group_year_year.keys()):
        year_year = group_year_year[group]
        xs = []
        ys = []
        for year in sorted(year_year.keys()):
            xs.append(year)
            ys.append(np.mean(year_year[year]))

        plt.plot(xs,ys,c=color_sequence[i],linewidth=2,label=group)

        group_xys[group] =[xs,ys]

    open('data/data_of_figs/temporal_year_differences_diversity_xys.json','w').write(json.dumps(group_xys))


    plt.xlabel('published year')
    plt.legend(loc=4)
    plt.ylabel('average year differences diversity')
    plt.tight_layout()
    plt.savefig('pdf/temporal_year_difference_diversity.jpg',dpi=400)
    logging.info('saved to pdf/temporal_year_difference_diversity.jpg')


def plot_diversity(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path,selected_IDs_references_num_path):


    logging.info('loading data from diversity files ...')
    wos_cc_diversity = json.loads(open(wos_cc_diversity_path).read())
    wos_subject_diversity = json.loads(open(wos_subject_diversity_path).read())
    wos_year_differences_diversity = json.loads(open(wos_year_differences_diversity_path).read())

    cc_diversity_values = [i for i in wos_cc_diversity.values() if i>0]
    subject_diversity_values = [i for i in wos_subject_diversity.values() if i>0]
    year_differences_diversity_values = [i for i in wos_year_differences_diversity.values() if i > 0]

    logging.info('Size of cc diversity:{:}, Size of subject diversity:{:}, Size year differences diversity:{:} . '.format(len(cc_diversity_values),len(subject_diversity_values),len(year_differences_diversity_values)))

    logging.info('plotting figures ...')
    
    fig_data = {}

    fig_data['cc'] = cc_diversity_values
    fig_data['subject'] = subject_diversity_values
    fig_data['year'] = year_differences_diversity_values
    open('data/data_of_figs/three_diversity_values.json','w').write(json.dumps(fig_data))


    plt.figure(figsize=(6,4))
    plt.hist(cc_diversity_values,bins=30)   
    plt.xlabel('impact diversity')
    plt.ylabel('number of papers')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/impact_diversity_dis.pdf',dpi=200)

    plt.figure(figsize=(6,4))
    plt.hist(subject_diversity_values,bins=30)    
    plt.xlabel('subject diversity')
    plt.ylabel('number of papers')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/subject_diversity_dis.pdf',dpi=200)

    plt.figure(figsize=(6,4))
    plt.hist(year_differences_diversity_values,bins=30)   
    plt.xlabel('year diversity')
    plt.ylabel('number of papers')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/year_differences_diversity_dis.pdf',dpi=200)

    logging.info('done ...')



def diversity_impact(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path,selected_IDs_cc_path):

    logging.info('loading id->citation count')
    com_ids_cc = json.loads(open(selected_IDs_cc_path).read())
    logging.info('loading wos cc diversity ..')
    wos_cc_diversity = json.loads(open(wos_cc_diversity_path).read())
    wos_subject_diversity = json.loads(open(wos_subject_diversity_path).read())
    wos_year_differences_diversity = json.loads(open(wos_year_differences_diversity_path).read())

    dvs_imp_fig_data = {}
    logging.info('plot citation count vs. impact diversity ...')
    ccbin_cd = defaultdict(list)

    cd_cc = defaultdict(list)

    cc_bins = []

    for pid in wos_cc_diversity.keys():
        cc_diversity  = wos_cc_diversity[pid]

        cc = com_ids_cc.get(pid,0)

        if cc<=0:
            continue

        # cc_bin = int(np.log(cc)/np.log(10))
        cc_bin = cc

        ccbin_cd[cc_bin].append(cc_diversity)

        cc_diversity = float('{:.1f}'.format(cc_diversity))

        cd_cc[cc_diversity].append(cc)

    # cc_bins = []
    # cc_cd = defaultdict(list)
    # for cc in sorted(ccbin_cd.keys()):
    #     if len(cc_bins)>10:
    #         cc_bins = []
        
    #     cc_bins.append(cc)

    #     cc_cd[cc_bins[0]].extend(ccbin_cd[cc])


    xs = []
    ys = []

    for cc in sorted(ccbin_cd.keys()):

        xs.append(cc)
        ys.append(np.mean(ccbin_cd[cc]))


    avg_ys = movingaverage(ys,20)

    t_ys = ys[:len(ys)-len(avg_ys)]
    t_ys.extend(avg_ys)

    t_zs = [i for i in zip(*lowess(t_ys,np.log(xs),frac= 0.08))[1]]

    dvs_imp_fig_data['cc_cd'] = [xs,ys]
    plt.figure()
    plt.plot(xs,t_ys,c=color_sequence[0])
    plt.plot(xs,t_zs,'--',c='r')

    plt.xlabel('citation count')
    plt.ylabel('average impact diversity')

    plt.xscale('log')

    plt.tight_layout()
    plt.savefig('pdf/citation_diversity_impact.pdf',dpi=200)

    xs = []
    ys = []

    for cd in sorted(cd_cc.keys()):

        xs.append(cd)
        ys.append(np.mean(cd_cc[cd]))


    dvs_imp_fig_data['cd_cc'] = [xs,ys]

    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])

    plt.xlabel('impact diversity')
    plt.ylabel('average citation count')

    # plt.xscale('log')

    plt.tight_layout()
    plt.savefig('pdf/cd_cc.pdf',dpi=200)

    logging.info('plot subject diversity vs. impact diversity ...')

    ccbin_sd = defaultdict(list)
    sd_cc = defaultdict(list)
    for pid in wos_subject_diversity.keys():
        cc_diversity  = wos_subject_diversity[pid]

        cc = com_ids_cc.get(pid,0)

        if cc<=0:
            continue

        # cc_bin = int(np.log(cc)/np.log(10))
        cc_bin = cc
        
        ccbin_sd[cc_bin].append(cc_diversity)

        cc_diversity = float('{:.1f}'.format(cc_diversity))

        sd_cc[cc_diversity].append(cc)


    cc_bins = []
    cc_sd = defaultdict(list)
    for cc in sorted(ccbin_sd.keys()):
        if len(cc_bins)>10:
            cc_bins = []
        
        cc_bins.append(cc)

        cc_sd[cc_bins[0]].extend(ccbin_sd[cc])


    xs = []
    ys = []

    for cc in sorted(cc_sd.keys()):
        xs.append(cc)
        ys.append(np.mean(cc_sd[cc]))

    dvs_imp_fig_data['cc_sd'] = [xs,ys]

    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])

    plt.xlabel('citation count')
    plt.ylabel('average subject diversity')

    plt.xscale('log')

    plt.tight_layout()
    plt.savefig('pdf/impact_diversity_subject.pdf',dpi=200)


    xs = []
    ys = []

    for sd in sorted(sd_cc.keys()):
        xs.append(sd)
        ys.append(np.mean(sd_cc[sd]))

    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])

    plt.xlabel('subject diversity')
    plt.ylabel('average citation count')

    # plt.xscale('log')
    dvs_imp_fig_data['sd_cc'] = [xs,ys]

    plt.tight_layout()
    plt.savefig('pdf/sd_cc.pdf',dpi=200)


    logging.info('plot year diversity vs. impact diversity ...')

    ccbin_yd = defaultdict(list)
    yd_cc = defaultdict(list)
    for pid in wos_year_differences_diversity.keys():
        cc_diversity  = wos_year_differences_diversity[pid]

        cc = com_ids_cc.get(pid,0)

        if cc<=0:
            continue

        # cc_bin = int(np.log(cc)/np.log(10))
        cc_bin = cc

        ccbin_yd[cc_bin].append(cc_diversity)

        cc_diversity = float('{:.1f}'.format(cc_diversity))

        yd_cc[cc_diversity].append(cc)


    cc_bins = []
    cc_yd = defaultdict(list)
    for cc in sorted(ccbin_yd.keys()):
        if len(cc_bins)>10:
            cc_bins = []
        
        cc_bins.append(cc)

        cc_yd[cc_bins[0]].extend(ccbin_yd[cc])

    xs = []
    ys = []

    for cc in sorted(cc_yd.keys()):
        xs.append(cc)
        ys.append(np.mean(cc_yd[cc]))

    dvs_imp_fig_data['cc_yd'] = [xs,ys]

    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])

    plt.xlabel('citation count')
    plt.ylabel('average year diversity')

    plt.xscale('log')

    plt.tight_layout()
    plt.savefig('pdf/impact_diversity_year.pdf',dpi=200)


    xs = []
    ys = []

    for yd in sorted(yd_cc.keys()):
        xs.append(yd)
        ys.append(np.mean(yd_cc[yd]))

    plt.figure()
    plt.plot(xs,ys,c=color_sequence[0])

    plt.ylabel('average citation count')
    plt.xlabel('year diversity')

    # plt.xscale('log')
    dvs_imp_fig_data['ys_cc'] = [xs,ys]

    plt.tight_layout()
    plt.savefig('pdf/yd_cc.pdf',dpi=200)

    open('data/data_of_figs/diversity_impact_data.json','w').write(json.dumps(dvs_imp_fig_data))

    logging.info('Done ...')


def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma


if __name__ == '__main__':
    
    com_ids_cc_path = 'data/com_ids_cc.json'
    selected_ids_references_path ='data/selected_IDs_references.txt'
    com_ids_subjects_path = 'data/com_ids_subjects.json'
    year_differences_path = 'data/statistics/year_differences.json'
    com_IDs_year_path = 'data/com_ids_year.json'
    subject_sim_path = 'data/subject_sim.json'
    # cal_diversity(com_ids_cc_path,com_ids_subjects_path,selected_ids_references_path,year_differences_path,com_IDs_year_path,subject_sim_path)

    wos_cc_diversity_path = 'data/wos_cc_diversity.json'
    wos_subject_diversity_path = 'data/wos_subject_diversity.json'
    wos_year_differences_diversity_path = 'data/wos_year_differences_diversity.json'
    selected_IDs_references_num_path = 'data/selected_IDs_references_num.json'
    # plot_diversity(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path,selected_IDs_references_num_path)

    selected_IDs_cc_path = 'data/selected_IDs_cc.json'
    diversity_impact(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path,selected_IDs_cc_path)

    # plot_diversity_over_year(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path,com_ids_cc_path,com_IDs_year_path)







