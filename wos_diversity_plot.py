#coding:utf-8


from basic_config import *

def load_basic_data(attrs=['year','subj','topsubj','teamsize','doctype','cn'],isStat=False):

    logging.info('======== LOADING BASIC DATA =============')
    logging.info('======== ================== =============')

    results = {}

    if 'year' in attrs:

        logging.info('loading paper pubyear ...')
        pid_pubyear = json.loads(open('../WOS_data_processing/data/pid_pubyear.json').read())
        logging.info('{} papers has year label.'.format(len(pid_pubyear.keys())))

        results['year']=pid_pubyear

    if 'subj' in attrs:
        logging.info('loading paper subjects ...')
        pid_subjects = json.loads(open('../WOS_data_processing/data/pid_subjects.json').read())
        logging.info('{} papers has subject label.'.format(len(pid_subjects.keys())))

        results['subj'] = pid_subjects

    if 'topsubj' in attrs:
        logging.info('loading paper top subjects ...')
        pid_topsubjs = json.loads(open('../WOS_data_processing/data/pid_topsubjs.json').read())
        logging.info('{} papers has top subject label.'.format(len(pid_topsubjs.keys())))
        
        results['topsubj']=pid_topsubjs


    if 'teamsize' in attrs:

        logging.info('loading paper teamsize ...')
        pid_teamsize = json.loads(open('../WOS_data_processing/data/pid_teamsize.json').read())
        logging.info('{} papers has teamsize label.'.format(len(pid_teamsize.keys())))

        results['teamsize'] = pid_teamsize

    if 'doctype'  in attrs:

        logging.info('loading paper doctype ...')
        pid_doctype = json.loads(open('../WOS_data_processing/data/pid_doctype.json').read())
        logging.info('{} papers has doctype label.'.format(len(pid_doctype.keys())))

        results['doctype'] = pid_doctype

    if 'cn' in attrs:

        logging.info('loading paper citation count ...')
        pid_cn = json.loads(open('../WOS_data_processing/data/pid_cn.json').read())
        logging.info('{} papers has citation count label.'.format(len(pid_cn.keys())))

        results['cn']=pid_cn

    if 'c5' in attrs:

        logging.info('loading paper citation c5 ...')
        pid_cn = json.loads(open('../WOS_data_processing/data/pid_c5.json').read())
        logging.info('{} papers has c5 label.'.format(len(pid_cn.keys())))

        results['c5']=pid_cn

    if 'c2' in attrs:

        logging.info('loading paper citation c2 ...')
        pid_cn = json.loads(open('../WOS_data_processing/data/pid_c2.json').read())
        logging.info('{} papers has c2 label.'.format(len(pid_cn.keys())))

        results['c2']=pid_cn

    if 'c10' in attrs:

        logging.info('loading paper citation c10 ...')
        pid_cn = json.loads(open('../WOS_data_processing/data/pid_c10.json').read())
        logging.info('{} papers has c10 label.'.format(len(pid_cn.keys())))

        results['c10']=pid_cn

    if isStat:
        interset = set(pid_pubyear.keys())&set(pid_teamsize.keys())&set(pid_topsubjs.keys())&set(pid_topsubjs.keys())
        logging.info('{} papers has both four attrs.'.format(len(interset)))

    logging.info('======== LOADING BASIC DATA DONE =============')
    logging.info('======== ======================= =============')


    if len(attrs)>=1:
        
        return [results[attr] for attr in attrs]

    else:
        return None



def data2Hist(data,log=False):

    if log:
        edges = np.logspace(np.log(np.min(data)),np.log(np.max(data)),200)
    else:
        edges = np.linspace(np.min(data),np.max(data),200)

    hists,bins_edges = np.histogram(data,bins=edges)

    centers = np.array(bins_edges[:-1]+bins_edges[1:])/float(2)

    t = np.sum(hists)

    cdf = [np.sum(hists[:i+1])/float(t) for i in range(len(hists))]

    pdf = np.array(hists)/float(t)

    return centers,pdf,cdf


#  画出给定的图

def PDF_CDF_all(attrs,subjs,attr_name,save_name):

    logging.info(f'plotting PDF CDF on attr {attr_name} ...')

    subj_attrs = defaultdict(list)
    for i in range(len(attrs)):

        for subj in subjs[i]:

            subj_attrs[subj].append(attrs[i])

        subj_attrs['ALL'].append(attrs[i])

    PDF_CDF(subj_attrs,attr_name,save_name)


'''
    @param subj_attrs: 每一个学科对应的属性数组,所有的对应组别ALL

'''
def PDF_CDF(subj_attrs,attr_name,save_name):

    fig,axes = plt.subplots(2,1,figsize=(7,10))
    # 一个PDF与CDF画在一起的图

    if attr_name.startswith('c'):
        log=True
    else:
        log=False

    ax = axes[0]
    xs,pdf,cdf = data2Hist(subj_attrs['ALL'],log)
    color = '#1f77b4'
    ax.set_xlabel(attr_name)
    ax.set_ylabel('PDF', color=color)
    ax.plot(xs,pdf,label='PDF', color=color)
    ax.tick_params(axis='y', labelcolor=color)

    ax1 = ax.twinx()
    color = '#e377c2'
    ax1.set_ylabel('CDF', color=color)
    ax1.plot(xs,cdf,label='CDF', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    if attr_name.startswith('c'):
        ax.set_xscale('log')

    #一个各学科CDF一起的图
    ax = axes[1]
    for subj in sorted(subj_attrs.keys()):

        xs,_,ys = data2Hist(subj_attrs[subj],log)

        ax.plot(xs,ys,label=subj)

    ax.set_xlabel(attr_name)
    ax.set_ylabel('CDF')
    if attr_name.startswith('c'):
        ax.set_xscale('log')

    ax.legend(fontsize=6,ncol=2)


    plt.tight_layout()
    # 保存的图
    plt.savefig(f'fig/{save_name}_PDF_CDF.png',dpi=400)
    logging.info(f'fig saved to fig/{save_name}_PDF_CDF.png')


#  一种属性随着另一种属性的变化，
def attr1_over_attr2(attr1,attr2,all_subjs,attr_name_1,attr_name_2,save_name,axrange=[1,10],xscale='linear'):

    logging.info(f'plotting {attr_name_1} changes over {attr_name_2} ...')

    assert len(attr1)==len(attr2)

    # 获得attr1的最大值 最小值 
    attr_min = np.min(attr1)
    attr_max = np.max(attr1)

    subj_attr2_attr1list = defaultdict(lambda:defaultdict(list))

    for i in range(len(attr1)):

        if not axrange is None:
            if attr2[i]<axrange[0] or attr2[i]>axrange[1]:
                continue

        subjs = all_subjs[i]

        for subj in subjs:

            subj_attr2_attr1list[subj][attr2[i]].append(attr1[i])

        subj_attr2_attr1list['ALL'][attr2[i]].append(attr1[i])


    N = len(subj_attr2_attr1list.keys())

    fig,axes = plt.subplots(N,1,figsize=(7,5*N))

    for i,subj in enumerate(sorted(subj_attr2_attr1list.keys())):

        ax = axes[i]

        ax.set_title(subj)

        attr2_attr1list = subj_attr2_attr1list[subj]

        # 根据统计的结果进行画图
        xs = []
        ys_mean = []
        ys_median = []
        for a2 in sorted(attr2_attr1list.keys()):
            xs.append(a2)
            ys = attr2_attr1list[a2]
            ys = (np.array(ys)-attr_min)/(attr_max-attr_min)

            ys_mean.append(np.mean(ys))
            ys_median.append(np.median(ys))

        # 根据lowess对结果进行归一化
        # selected_ixes= np.random.choice(range(len(attr1)),size=5000)
        # pred_x,lowess,ll,ul = loess_data([attr2[ix] for ix in selected_ixes],[attr1[ix] for ix in selected_ixes])
        #  一种是用moving average
        window = 5
        if xscale=='log':  
            window=50
        ax.plot(xs,smooth(ys_mean,window),'--',label='mean')
        ax.plot(xs,smooth(ys_median,window),'-.',label='median')
        #  先不进行平滑
        # ax.plot(xs,ys_mean,label='mean')
        # ax.plot(xs,ys_median,label='median')

        ax.set_xscale(xscale)

        ax.set_xlabel(attr_name_2)
        ax.set_ylabel(attr_name_1)

        ax.legend()

    plt.tight_layout()

    plt.savefig(f'fig/{save_name}_dis.png',dpi=400)

    logging.info(f'fig saved to fig/{save_name}_dis.png')

def plot_div():

    paper_year,paper_topsubjs,paper_ts,paper_c10,paper_c5,paper_c2,paper_cn,pid_doctype= load_basic_data(['year','topsubj','teamsize','c10','c5','c2','cn','doctype'])

    ## 属性列表
    attrs = []
    progress = 0 
    logging.info("loading paper divsity files ....")
    pid_div_vs = json.loads(open("data/pid_divs.json").read())
    for pid in pid_div_vs.keys():

        progress+=1
        if progress%100000==0:
            logging.info("progress {} ....".format(progress))

        year = int(paper_year.get(pid,9999))
        ts = int(paper_ts.get(pid,-1))
        subjs = paper_topsubjs.get(pid,None)

        if  year<1980 or year>2004:
            continue

        # 属性列表的进行
        yd_div,subj_div,c2_div,c5_div,c10_div,\
        yd_mean,yd_std,\
        c2_mean,c2_std,c5_mean,c5_std,c10_mean,c10_std,\
        c2p_div,c5p_div,c10p_div,\
        c2p_mean,c2p_std,c5p_mean,c5p_std,c10p_mean,c10p_std = pid_div_vs[pid]

        c2,c5,c10,cn = paper_c2.get(pid,0),paper_c5.get(pid,0),paper_c10.get(pid,0),paper_cn.get(pid,0)
        subjs = paper_topsubjs[pid]

        did = 0
        doctype = pid_doctype.get(pid,'Article')
        if doctype=='Article':
            did = 0
        elif doctype =='Review':
            did = 1
        else:
            did =2

        attrs.append([c2,c5,c10,cn,year,ts,subjs,did,\
            yd_div,subj_div,c2_div,c5_div,c10_div,\
            yd_mean,yd_std,c2_mean,c2_std,c5_mean,c5_std,c10_mean,c10_std,\
            c2p_div,c5p_div,c10p_div,c2p_mean,c2p_std,c5p_mean,c5p_std,c10p_mean,c10p_std])

    logging.info('data loaded,start to plotting ...')

    # 根据attrs进行计算
    c2s,c5s,c10s,cns,years,tss,subjs,dids,\
    yd_divs,subj_divs,c2_divs,c5_divs,c10_divs,\
    yd_means,yd_stds,c2_means,c2_stds,c5_means,c5_stds,c10_means,c10_stds,\
    c2p_divs,c5p_divs,c10p_divs,c2p_means,c2p_stds,c5p_means,c5p_stds,c10p_means,c10p_stds = zip(*attrs)
  
    # ============== Year div ===============
    plot_single_attr(yd_divs,'year diversity','YD',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(yd_means,'yd_mean','YD_mean',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(yd_stds,'yd_std','YD_std',subjs,years,tss,c2s,c5s,c10s,cns)

    ## =================== subj div ===============
    plot_single_attr(subj_divs,'subject diversity','SD',subjs,years,tss,c2s,c5s,c10s,cns)

    # ===================== IMPACT DIV ==============
    plot_single_attr(c10_divs,'impact diversity','ID',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(c10p_divs,'impact diversity (percentile)','IDP',subjs,years,tss,c2s,c5s,c10s,cns)

    plot_single_attr(c2_means,'c2_mean','c2_mean',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(c2_stds,'c2_std','c2_std',subjs,years,tss,c2s,c5s,c10s,cns)

    plot_single_attr(c2p_means,'c2p_mean','c2p_mean',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(c2p_stds,'c2p_std','c2p_std',subjs,years,tss,c2s,c5s,c10s,cns)
    
    plot_single_attr(c5_means,'c5_mean','c5_mean',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(c5_stds,'c5_std','c5_std',subjs,years,tss,c2s,c5s,c10s,cns)

    plot_single_attr(c5p_means,'c5p_mean','c5p_mean',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(c5p_stds,'c5p_std','c5p_std',subjs,years,tss,c2s,c5s,c10s,cns)

    plot_single_attr(c10_means,'c10_mean','c10_mean',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(c10_stds,'c10_std','c10_std',subjs,years,tss,c2s,c5s,c10s,cns)

    plot_single_attr(c10p_means,'c10p_mean','c10p_mean',subjs,years,tss,c2s,c5s,c10s,cns)
    plot_single_attr(c10p_stds,'c10p_std','c10p_std',subjs,years,tss,c2s,c5s,c10s,cns)

    of = open('data/ALL_attrs.txt','w')

    of.write('c2,c5,c10,cn,year,ts,subjs,did,yd_div,subj_div,c2_div,c5_div,c10_div,yd_mean,yd_std,c2_mean,c2_std,c5_mean,c5_std,c10_mean,c10_std,c2p_div,c5p_div,c10p_div,c2p_mean,c2p_std,c5p_mean,c5p_std,c10p_mean,c10p_std\n')

    lines = []

    for attr in attrs:

        c2,c5,c10,cn,year,ts,subjs,did,\
        yd_div,subj_div,c2_div,c5_div,c10_div,\
        yd_mean,yd_std,c2_mean,c2_std,c5_mean,c5_std,c10_mean,c10_std,\
        c2p_div,c5p_div,c10p_div,c2p_mean,c2p_std,c5p_mean,c5p_std,c10p_mean,c10p_std = attr
        if ts==-1:
            continue

        # 随机选择一个subj
        attr[6] = np.random.choice(subjs,size=1)[0]

        lines.append(','.join([str(a) for a in attr]))

    of.write('\n'.join(lines)+'\n')

    of.close()

    logging.info('data saved to data/ALL_attrs.txt.')




def plot_single_attr(attrs,attr_name,saveID,subjs,years,tss,c2s,c5s,c10s,cns):
    PDF_CDF_all(attrs,subjs,attr_name,f'{saveID}')
    # 随时间的变化
    attr1_over_attr2(attrs,years,subjs,attr_name,'year',f'{saveID}_over_year',axrange=[1980,2004],xscale='linear')
    # 随着teamsize的变化
    attr1_over_attr2(attrs,tss,subjs,attr_name,'team size',f'{saveID}_over_ts',axrange=[1,10],xscale='linear')
    # 随着c2 c5 c10 cn
    attr1_over_attr2(attrs,c2s,subjs,attr_name,'$c_2$',f'{saveID}_over_c2',axrange=None,xscale='log')
    attr1_over_attr2(attrs,c5s,subjs,attr_name,'$c_5$',f'{saveID}_over_c5',axrange=None,xscale='log')
    attr1_over_attr2(attrs,c10s,subjs,attr_name,'$c_{10}$',f'{saveID}_over_c10',axrange=None,xscale='log')
    attr1_over_attr2(attrs,cns,subjs,attr_name,'number of citations',f'{saveID}_over_cn',axrange=None,xscale='log')



## 几种diversity随时间的变化
def year_div():

    paper_year,paper_topsubjs,paper_ts,paper_c10,paper_c5,paper_cn,pid_doctype = load_basic_data(['year','topsubj','teamsize','c10','c5','cn','doctype'])

    year_div_dis = defaultdict(list)
    c10_div_dis = defaultdict(list)
    subj_div_dis = defaultdict(list)

    ## team size
    ts_year_dis = defaultdict(list)
    ts_c10_dis = defaultdict(list)
    ts_subj_dis = defaultdict(list)

    ## field of study
    fos_year_dis = defaultdict(list)
    fos_c10_dis = defaultdict(list)
    fos_subj_dis = defaultdict(list)

    ## 整体分布
    general_t_divs = defaultdict(list)

    ## 
    attrs = []

    progress = 0 

    # logging.info('sorting ....')

    # totalnum = len(pid_div_vs.keys())

    # pid_si = {}

    # for i,pid in enumerate(sorted(pid_div_vs.keys(),key= lambda x:pid_div_vs[x][1])):

    #     pid_si[pid] = i/float(totalnum)

    # pid_yi = {}
    # for i,pid in enumerate(sorted(pid_div_vs.keys(),key= lambda x:pid_div_vs[x][0])):

    #     pid_yi[pid] = i/float(totalnum)

    # pid_ii = {}
    # for i,pid in enumerate(sorted(pid_div_vs.keys(),key= lambda x:pid_div_vs[x][3])):

    #     pid_ii[pid] = i/float(totalnum)

    # logging.info('sorted done')


    pid_div_vs = json.loads(open("data/pid_divs.json").read())
    for pid in pid_div_vs.keys():

        progress+=1

        if progress%100000==0:

            logging.info("progress {} ....".format(progress))


        year = int(paper_year.get(pid,9999))

        ts = int(paper_ts.get(pid,-1))

        subjs = paper_topsubjs.get(pid,None)

        if  year<1980 or year>2004:
            continue


        # year_div,c5_div,c10_div,subj_div = pid_div_vs[pid]

        yd_div,subj_div,c2_div,c5_div,c10_div,\
        yd_mean,yd_std,\
        c2_mean,c2_std,c5_mean,c5_std,c10_mean,c10_std,\
        c2p_div,c5p_div,c10p_div,\
        c2p_mean,c2p_std,c5p_mean,c5p_std,c10p_mean,c10p_std = pid_div_vs[pid]

        subj = subjs[0]
        did = 0

        doctype = pid_doctype.get(pid,'Article')

        if doctype=='Article':
            did = 0
        elif doctype =='Review':
            did = 1
        else:
            did =2

        attrs.append([paper_c10.get(pid,0),paper_c5.get(pid,0),paper_cn.get(pid,0),year,ts,year_div,subj_div,c10_div,subj,did])

        # year_div = pid_yi[pid]
        # c10_div = pid_ii[pid]
        # subj_div = pid_si[pid]

        year_div_dis[year].append(year_div)
        c10_div_dis[year].append(c10_div)
        subj_div_dis[year].append(subj_div)

        if ts!=-1:
            ts_year_dis[ts].append(year_div)
            ts_subj_dis[ts].append(subj_div)
            ts_c10_dis[ts].append(c10_div)

        if subjs is None:
            continue

        for subj in subjs:
            fos_year_dis[subj].append(year_div)
            fos_subj_dis[subj].append(subj_div)
            fos_c10_dis[subj].append(c10_div)


        general_t_divs['year'].append(year_div)
        general_t_divs['subject'].append(subj_div)
        general_t_divs['impact'].append(c10_div)


    # max_yd,min_yd = np.max(general_t_divs['year']),np.min(general_t_divs['year'])
    # max_sd,min_sd = np.max(general_t_divs['subject']),np.min(general_t_divs['subject'])
    # max_id,min_id = np.max(general_t_divs['impact']),np.min(general_t_divs['impact'])

    max_yd,min_yd = 1,0
    max_sd,min_sd = 1,0
    max_id,min_id = 1,0



    plot_dis_over_attr('publication year',(year_div_dis,subj_div_dis,c10_div_dis,max_yd,min_yd,max_sd,min_sd,max_id,min_id),(1979,2005))

    plot_dis_over_attr('team size',(ts_year_dis,ts_subj_dis,ts_c10_dis,max_yd,min_yd,max_sd,min_sd,max_id,min_id),(0,10))

    of = open('data/ALL_attrs.txt','w')

    of.write('c10,c5,cn,year,teamsize,year div,subj div,impact div\n')

    lines = []

    for attr in attrs:
        if attr[4]==-1:
            continue
        lines.append(','.join([str(a) for a in attr]))

    of.write('\n'.join(lines)+'\n')

    of.close()

    logging.info('data saved to data/ALL_attrs.txt.')

    # plot_dis_over_attr('field',(fos_year_dis,fos_subj_dis,fos_c10_dis))

    ## 几个领域的分布图

    fig,axes  = plt.subplots(3,1,figsize=(5,12))

    ax = axes[0]
    for subj in sorted(fos_year_dis.keys()):

        xs,_,ys = dataHist(fos_year_dis[subj])

        ax.plot(xs,ys,label=subj)

    ax.set_xlabel('year diversity')
    ax.set_ylabel('CDF')

    ax.legend(fontsize=6,ncol=2)


    ax = axes[1]
    for subj in sorted(fos_subj_dis.keys()):

        xs,_,ys = dataHist(fos_subj_dis[subj])

        ax.plot(xs,ys,label=subj)

    ax.set_xlabel('subject diversity')
    ax.set_ylabel('CDF')

    ax.legend(fontsize=6,ncol=2)


    ax = axes[2]
    for subj in sorted(fos_c10_dis.keys()):

        xs,_,ys = dataHist(fos_c10_dis[subj])

        ax.plot(xs,ys,label=subj)

    ax.set_xlabel('impact diversity')
    ax.set_ylabel('CDF')

    ax.legend(fontsize=6,ncol=2)

    plt.tight_layout()

    plt.savefig('fig/subject_div_dis.png',dpi=400)

    logging.info("fig saved to fig/subject_div_dis.png")


    fig,axes = plt.subplots(3,1,figsize=(6,12))

    for i,t in enumerate(general_t_divs.keys()):

        ax = axes[i]
        xs,pdf,cdf = dataHist(general_t_divs[t])

        color = '#1f77b4'
        ax.set_xlabel('{} diversity'.format(t))
        ax.set_ylabel('PDF', color=color)
        ax.plot(xs,pdf,label='PDF', color=color)
        ax.tick_params(axis='y', labelcolor=color)

        ax1 = ax.twinx()
        color = '#e377c2'
        ax1.set_ylabel('CDF', color=color)
        ax1.plot(xs,cdf,label='CDF', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        

    plt.tight_layout()

    plt.savefig('fig/general_div_CDF_Dis.png',dpi=400)

    logging.info("fig saved to fig/general_div_Dis.png.")

    c10s,c5s,cns,years,tses,year_divs,subj_divs,c10_divs,_subjs,docs = zip(*attrs)

    c10_attrs= defaultdict(lambda:defaultdict(list))
    c5_attrs= defaultdict(lambda:defaultdict(list))

    for i in range(len(c10s)):

        c10_attrs[c10s[i]]['year'].append(year_divs[i])
        c10_attrs[c10s[i]]['subj'].append(subj_divs[i])
        c10_attrs[c10s[i]]['impact'].append(c10_divs[i])

        c5_attrs[c5s[i]]['year'].append(year_divs[i])
        c5_attrs[c5s[i]]['subj'].append(subj_divs[i])
        c5_attrs[c5s[i]]['impact'].append(c10_divs[i])


    ## 画散点图
    fig,axes = plt.subplots(3,1,figsize=(5,12))


    ax = axes[0]

    xs = []
    ys_mean = []
    ys_median = []


    for c10 in sorted(c10_attrs.keys()):
        xs.append(c10)
        ys = c10_attrs[c10]['year']
        ys = (np.array(ys)-min_yd)/(max_yd-min_yd)

        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))


    ax.plot(xs,smooth(ys_mean,99),'--',label='mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label='median')
    ax.set_xscale('log')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('year diversity')

    ax = axes[1]
    
    xs = []
    ys_mean = []
    ys_median = []


    for c10 in sorted(c10_attrs.keys()):
        xs.append(c10)
        ys = c10_attrs[c10]['subj']
        ys = (np.array(ys)-min_sd)/(max_sd-min_sd)

        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))


    ax.plot(xs,smooth(ys_mean,99),'--',label='mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label='median')
    ax.set_xscale('log')


    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('subject diversity')

    ax = axes[2]

    xs = []
    ys_mean = []
    ys_median = []


    for c10 in sorted(c10_attrs.keys()):
        xs.append(c10)
        ys = c10_attrs[c10]['impact']
        ys = (np.array(ys)-min_id)/(max_id-min_id)

        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))


    ax.plot(xs,smooth(ys_mean,99),'--',label='mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label='median')
    ax.set_xscale('log')



    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('impact diversity')


    plt.tight_layout()

    plt.savefig('fig/diversity_citation_c10_scatter.png',dpi=200)

    logging.info("fig saved to fig/diversity_citation_c10_scatter.png.")



    ## 画散点图
    # samples = np.random.choice(np.arange(len(c5s)),size=1000)

    fig,axes = plt.subplots(3,1,figsize=(5,12))

    ax = axes[0]

    xs = []
    ys_mean = []
    ys_median = []


    for c5 in sorted(c5_attrs.keys()):
        xs.append(c5)
        ys = c5_attrs[c5]['year']
        ys = (np.array(ys)-min_yd)/(max_yd-min_yd)

        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))


    ax.plot(xs,smooth(ys_mean,99),'--',label='mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label='median')
    ax.set_xscale('log')

    ax.set_xlabel('$c_{5}$')
    ax.set_ylabel('year diversity')

    ax = axes[1]
    
    xs = []
    ys_mean = []
    ys_median = []


    for c5 in sorted(c5_attrs.keys()):
        xs.append(c5)
        ys = c5_attrs[c5]['subj']
        ys = (np.array(ys)-min_sd)/(max_sd-min_sd)

        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))


    ax.plot(xs,smooth(ys_mean,99),'--',label='mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label='median')
    ax.set_xscale('log')


    ax.set_xlabel('$c_{5}$')
    ax.set_ylabel('subject diversity')

    ax = axes[2]

    xs = []
    ys_mean = []
    ys_median = []


    for c5 in sorted(c5_attrs.keys()):
        xs.append(c5)
        ys = c5_attrs[c5]['impact']
        ys = (np.array(ys)-min_id)/(max_id-min_id)

        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))


    ax.plot(xs,smooth(ys_mean,99),'--',label='mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label='median')
    ax.set_xscale('log')


    ax.set_xlabel('$c_{5}$')
    ax.set_ylabel('impact diversity')


    plt.tight_layout()

    plt.savefig('fig/diversity_citation_c5_scatter.png',dpi=200)

    logging.info("fig saved to fig/diversity_citation_c5_scatter.png.")



    # fig,axes = plt.subplots(3,1,figsize=(5,12))

    # xs = [cns[i] for i in samples]

    # ax = axes[0]

    # ys = [year_divs[i] for i in samples]

    # ax.plot(xs,ys,'o')
    # ax.set_xscale('log')


    # ax.set_xlabel('$c_{10}$')
    # ax.set_ylabel('year diversity')

    # ax = axes[1]

    # ys = [subj_divs[i] for i in samples]

    # ax.plot(xs,ys,'o')
    # ax.set_xscale('log')


    # ax.set_xlabel('$c_{10}$')
    # ax.set_ylabel('subject diversity')

    # ax = axes[2]

    # ys = [c10_divs[i] for i in samples]

    # ax.plot(xs,ys,'o')
    # ax.set_xscale('log')


    # ax.set_xlabel('$c_{10}$')
    # ax.set_ylabel('impact diversity')


    # plt.tight_layout()

    # plt.savefig('fig/diversity_citation_cn_scatter.png',dpi=200)

    # logging.info("fig saved to fig/diversity_citation_cn_scatter.png.")

def smooth(a,WSZ):
  # # a:原始数据，NumPy 1-D array containing the data to be smoothed
  # # 必须是1-D的，如果不是，请使用 np.ravel()或者np.squeeze()转化 
  # # WSZ: smoothing window size needs, which must be odd number,
  # # as in the original MATLAB implementation
  # # out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ
  # # r = np.arange(1,WSZ-1,2)
  # # start = np.cumsum(a[:WSZ-1])[::2]/r
  # # stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
  # # return np.concatenate(( start , out0, stop ))

  # return [np.mean(a[:i+1]) for i in range(len(a))]

  # 使用savgol滤波器进行平滑线
    return scipy.signal.savgol_filter(a,WSZ,2)

def plot_dis_over_attr(attrName,data,xlim=None):

    # logging.info("start to plotting {}, length of data {} ....".format(attrName,len(data)))

    # print(data.keys())

    year_div_dis,subj_div_dis,c10_div_dis,max_yd,min_yd,max_sd,min_sd,max_id,min_id = data

    fig,axes = plt.subplots(3,1,figsize=(5,12))

    ax = axes[0]
    xs = []
    ys_mean = []
    ys_median = []
    for year in sorted(year_div_dis.keys()):
        xs.append(year)
        ys = (np.array(year_div_dis[year])-min_yd)/(max_yd-min_yd)
        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))

    ax.plot(xs,smooth(ys_mean,99),'--',label = 'mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label ='median')

    # ax.set_ylim()

    ax.set_xlabel('{}'.format(attrName))
    ax.set_ylabel('year diversity')
    ax.set_title('year diversity')

    if xlim is not None:
        ax.set_xlim(xlim[0],xlim[1])

    ax.legend()


    ax = axes[1]
    xs = []
    ys_mean = []
    ys_median = []
    for year in sorted(subj_div_dis.keys()):
        xs.append(year)
        ys = (np.array(subj_div_dis[year])-min_sd)/(max_sd-min_sd)

        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))


    ax.plot(xs,smooth(ys_mean,99),'--',label = 'mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label = 'median')

    ax.set_xlabel('{}'.format(attrName))
    ax.set_ylabel('subject diversity')

    ax.set_title('subject diversity')

    if xlim is not None:
        ax.set_xlim(xlim[0],xlim[1])

    ax.legend()


    ax = axes[2]
    xs = []
    ys_mean = []
    ys_median = []
    for year in sorted(c10_div_dis.keys()):
        xs.append(year)

        ys = (np.array(c10_div_dis[year])-min_id)/(max_id-min_id)

        ys_mean.append(np.mean(ys))
        ys_median.append(np.median(ys))


    ax.plot(xs,smooth(ys_mean,99),'--',label = 'mean')
    ax.plot(xs,smooth(ys_median,99),'-.',label = 'median')

    ax.set_xlabel('{}'.format(attrName))
    ax.set_ylabel('impact diversity')

    ax.set_title('impact diversity')

    if xlim is not None:
        ax.set_xlim(xlim[0],xlim[1])

    ax.legend()


    plt.tight_layout()

    plt.savefig('fig/diversity_over_{}.png'.format(attrName.replace(' ','_')),dpi=400)
    logging.info("fig saved to fig/diversity_over_{}.png.".format(attrName.replace(' ','_')))



def dataHist(data):

    hists,bins_edges = np.histogram(data,bins=500)

    centers = np.array(bins_edges[:-1]+bins_edges[1:])/float(2)

    t = np.sum(hists)

    cdf = [np.sum(hists[:i+1])/float(t) for i in range(len(hists))]

    pdf = np.array(hists)/float(t)

    return centers,pdf,cdf



## 几种diversity随时间的变化
def percentile_div():

    paper_year,paper_topsubjs,paper_ts,paper_c10,paper_c5,paper_cn = load_basic_data(['year','topsubj','teamsize','c10','c5','cn'])

    pid_div_vs = json.loads(open("data/pid_divs.json").read())


    year_div_dis = defaultdict(list)
    c10_div_dis = defaultdict(list)
    subj_div_dis = defaultdict(list)

    ## team size
    ts_year_dis = defaultdict(list)
    ts_c10_dis = defaultdict(list)
    ts_subj_dis = defaultdict(list)

    ## field of study
    fos_year_dis = defaultdict(list)
    fos_c10_dis = defaultdict(list)
    fos_subj_dis = defaultdict(list)

    ## 整体分布
    general_t_divs = defaultdict(list)

    ## 
    attrs = []

    progress = 0 

    logging.info('sorting ....')

    totalnum = len(pid_div_vs.keys())

    pid_si = {}

    for i,pid in enumerate(sorted(pid_div_vs.keys(),key= lambda x:pid_div_vs[x][1])):

        pid_si[pid] = i/float(totalnum)

    pid_yi = {}
    for i,pid in enumerate(sorted(pid_div_vs.keys(),key= lambda x:pid_div_vs[x][0])):

        pid_yi[pid] = i/float(totalnum)

    pid_ii = {}
    for i,pid in enumerate(sorted(pid_div_vs.keys(),key= lambda x:pid_div_vs[x][3])):

        pid_ii[pid] = i/float(totalnum)

    logging.info('sorted done')


    for pid in pid_div_vs.keys():

        progress+=1

        if progress%100000==0:

            logging.info("progress {} ....".format(progress))


        year = int(paper_year.get(pid,9999))

        ts = int(paper_ts.get(pid,-1))

        subjs = paper_topsubjs.get(pid,None)

        if  year<1980 or year>2004:
            continue

        year_div = pid_yi[pid]*100
        c10_div = pid_ii[pid]*100
        subj_div = pid_si[pid]*100

        attrs.append([paper_c10.get(pid,0),paper_c5.get(pid,0),paper_cn.get(pid,0),year,ts,year_div,subj_div,c10_div])


    c10s,c5s,cns,years,tses,yds,sds,ids = zip(*attrs)
    ## 随着year的变化
    plot_attrs(years,yds,'year','percentile of year diversity','fig/year_yd.png')
    plot_attrs(years,sds,'year','percentile of subject diversity','fig/year_sd.png')
    plot_attrs(years,ids,'year','percentile of impact diversity','fig/year_id.png')


    c10s,c10_yds,c10_sds,c10_ids = zip(*[[c10s[ix],yds[ix],sds[ix],ids[ix]] for ix in range(len(c10s)) if c10s[ix]!=0])
    plot_attrs(c10s,c10_yds,'$c_{10}$','percentile of year diversity','fig/c10_yd.png',logX=True)
    plot_attrs(c10s,c10_sds,'$c_{10}$','percentile of subject diversity','fig/c10_sd.png',logX=True)
    plot_attrs(c10s,c10_ids,'$c_{10}$','percentile of impact diversity','fig/c10_id.png',logX=True)

    c5s,c5_yds,c5_sds,c5_ids = zip(*[[c5s[ix],yds[ix],sds[ix],ids[ix]] for ix in range(len(c5s)) if c5s[ix]!=0])
    plot_attrs(c5s,c5_yds,'$c_5$','percentile of year diversity','fig/c5_yd.png',logX=True)
    plot_attrs(c5s,c5_sds,'$c_5$','percentile of subject diversity','fig/c5_sd.png',logX=True)
    plot_attrs(c5s,c5_ids,'$c_5$','percentile of impact diversity','fig/c5_id.png',logX=True)

    cns,cn_yds,cn_sds,cn_ids = zip(*[[cns[ix],yds[ix],sds[ix],ids[ix]] for ix in range(len(cns)) if cns[ix]!=0])
    plot_attrs(cns,cn_yds,'$c_n$','percentile of year diversity','fig/cn_yd.png',logX=True)
    plot_attrs(cns,cn_sds,'$c_n$','percentile of subject diversity','fig/cn_sd.png',logX=True)
    plot_attrs(cns,cn_ids,'$c_n$','percentile of impact diversity','fig/cn_id.png',logX=True)

    tses,ts_yds,ts_sds,ts_ids = zip(*[[tses[ix],yds[ix],sds[ix],ids[ix]] for ix in range(len(tses)) if tses[ix]!=-1 and tses[-1]<13])
    plot_attrs(tses,ts_yds,'teamsize','percentile of year diversity','fig/teamsize_yd.png')
    plot_attrs(tses,ts_sds,'teamsize','percentile of subject diversity','fig/teamsize_sd.png')
    plot_attrs(tses,ts_ids,'teamsize','percentile of impact diversity','fig/teamsize_id.png')


def plot_attrs(x,y,xlabel,ylabel,saved_path,logX=False):

    logging.info('plot {} vs {} figs ...'.format(xlabel,ylabel))

    fig,axes = plt.subplots(2,1,figsize=(5,8))

    ax = axes[0]

    selected_ixes= np.random.choice(range(len(x)),size=5000)

    pred_x,lowess,ll,ul = loess_data([x[ix] for ix in selected_ixes],[y[ix] for ix in selected_ixes])

    # pred_x,lowess,ll,ul = loess_data(x,y)

    ax.plot(pred_x,lowess)
    ax.fill_between(pred_x,ll,ul,alpha=.3,color='#ff9896')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.set_ylim(0,100)

    if logX:
        ax.set_xscale('log')


    logging.info('haha')

    ax = axes[1]

    xs,ys_mean,ll,ul = average_with_95_confidence(x,y)

    ax.plot(xs,ys_mean)
    ax.fill_between(xs,ll,ul,alpha=.3,color='#ff9896')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if logX:
        ax.set_xscale('log')

    ax.set_ylim(0,100)


    plt.tight_layout()

    plt.savefig(saved_path,dpi=400)

    logging.info('fig saved to {}.'.format(saved_path))



## 随领域的分布
def subject_div():

    pass


## 与citation count之间的关系
def impact_div():

    pass



if __name__ == '__main__':
    # year_div()

    # percentile_div()

    plot_div()