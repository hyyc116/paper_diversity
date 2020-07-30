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


## 几种diversity随时间的变化
def year_div():

    paper_year,paper_topsubjs,paper_ts,paper_c10,paper_c5,paper_cn = load_basic_data(['year','topsubj','teamsize','c10','c5','cn'])

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

        year_div,subj_div,c5_div,c10_div = pid_div_vs[pid]

        attrs.append([paper_c10.get(pid,0),paper_c5.get(pid,0),paper_cn.get(pid,0),year_div,subj_div,c10_div])

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


    max_yd,min_yd = np.max(general_t_divs['year']),np.min(general_t_divs['year'])
    max_sd,min_sd = np.max(general_t_divs['subject']),np.min(general_t_divs['subject'])
    max_id,min_id = np.max(general_t_divs['impact']),np.min(general_t_divs['impact'])


    plot_dis_over_attr('publication year',(year_div_dis,subj_div_dis,c10_div_dis,max_yd,min_yd,max_sd,min_sd,max_id,min_id),(1979,2005))

    plot_dis_over_attr('team size',(ts_year_dis,ts_subj_dis,ts_c10_dis,max_yd,min_yd,max_sd,min_sd,max_id,min_id),(0,10))

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

    c10s,c5s,cns,year_divs,subj_divs,c10_divs = zip(*attrs)

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


    ax.plot(xs,ys_mean,'--',label='mean')
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


    ax.plot(xs,ys_mean,'--',label='mean')
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
  # a:原始数据，NumPy 1-D array containing the data to be smoothed
  # 必须是1-D的，如果不是，请使用 np.ravel()或者np.squeeze()转化 
  # WSZ: smoothing window size needs, which must be odd number,
  # as in the original MATLAB implementation
  out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ
  r = np.arange(1,WSZ-1,2)
  start = np.cumsum(a[:WSZ-1])[::2]/r
  stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
  return np.concatenate(( start , out0, stop ))

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


## 随领域的分布
def subject_div():

    pass


## 与citation count之间的关系
def impact_div():

    pass



if __name__ == '__main__':
    year_div()