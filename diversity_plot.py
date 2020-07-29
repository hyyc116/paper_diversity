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

        attrs.append([paper_c10[pid],paper_c5[pid],paper_cn[pid],year_div,subj_div,c10_div])

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
        general_t_divs['subj'].append(subj_div)
        general_t_divs['impact'].append(c10_div)



    plot_dis_over_attr('publication year',(year_div_dis,subj_div_dis,c10_div_dis),(1980,2005))

    plot_dis_over_attr('team size',(ts_year_dis,ts_subj_dis,ts_c10_dis),(0,10))

    # plot_dis_over_attr('field',(fos_year_dis,fos_subj_dis,fos_c10_dis))

    ## 几个领域的分布图

    fig,axes  = plt.subplots(3,1,figsize=(5,12))

    ax = axes[0]
    for subj in sorted(fos_year_dis.keys()):

        xs,ys = dataHist(fos_year_dis[subj])

        ax.plot(xs,ys,label=subj)

    ax.set_xlabel('year diversity')
    ax.set_ylabel('CDF')

    ax.legend(fontsize=6,ncol=2)


    ax = axes[1]
    for subj in sorted(fos_subj_dis.keys()):

        xs,ys = dataHist(fos_subj_dis[subj])

        ax.plot(xs,ys,label=subj)

    ax.set_xlabel('subject diversity')
    ax.set_ylabel('CDF')

    ax.legend(fontsize=6,ncol=2)


    ax = axes[2]
    for subj in sorted(fos_c10_dis.keys()):

        xs,ys = dataHist(fos_c10_dis[subj])

        ax.plot(xs,ys,label=subj)

    ax.set_xlabel('impact diversity')
    ax.set_ylabel('CDF')

    ax.legend(fontsize=6,ncol=2)

    plt.tight_layout()

    plt.savefig('fig/subject_div_dis.png',dpi=400)

    logging.info("fig saved to fig/subject_div_dis.png")


    fig,axes = plt.subplots(3,1,figsize=(5,12))

    for i,t in enumerate(general_t_divs.keys()):

        ax = axes[i]

        xs,ys = dataHist(general_t_divs[t])

        ax.plot(xs,ys,label=t)

        ax.set_xlabel('diversity')
        ax.set_ylabel('CDF')

    plt.tight_layout()

    plt.savefig('fig/general_div_Dis.png',dpi=400)

    logging.info("fig saved to fig/general_div_Dis.png.")

    c10s,c5s,cns,year_divs,subj_divs,c10_divs = zip(*attrs)

    ## 画散点图
    samples = np.random.choice(np.arange(len(c10s)),size=1000)

    fig,axes = plt.subplots(3,1,figsize=(5,12))

    xs = [c10s[i] for i in samples]

    ax = axes[0]

    ys = [year_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('year diversity')

    ax = axes[1]

    ys = [subj_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('subject diversity')

    ax = axes[2]

    ys = [c10_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('impact diversity')


    plt.tight_layout()

    plt.savefig('fig/diversity_citation_c10_scatter.png',dpi=200)

    logging.info("fig saved to fig/diversity_citation_c10_scatter.png.")



    ## 画散点图
    # samples = np.random.choice(np.arange(len(c5s)),size=1000)

    fig,axes = plt.subplots(3,1,figsize=(5,12))

    xs = [c5s[i] for i in samples]

    ax = axes[0]

    ys = [year_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('year diversity')

    ax = axes[1]

    ys = [subj_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('subject diversity')

    ax = axes[2]

    ys = [c10_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('impact diversity')


    plt.tight_layout()

    plt.savefig('fig/diversity_citation_c5_scatter.png',dpi=200)

    logging.info("fig saved to fig/diversity_citation_c5_scatter.png.")



    fig,axes = plt.subplots(3,1,figsize=(5,12))

    xs = [cns[i] for i in samples]

    ax = axes[0]

    ys = [year_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('year diversity')

    ax = axes[1]

    ys = [subj_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('subject diversity')

    ax = axes[2]

    ys = [c10_divs[i] for i in samples]

    ax.plot(xs,ys,'o')

    ax.set_xlabel('$c_{10}$')
    ax.set_ylabel('impact diversity')


    plt.tight_layout()

    plt.savefig('fig/diversity_citation_cn_scatter.png',dpi=200)

    logging.info("fig saved to fig/diversity_citation_cn_scatter.png.")



def plot_dis_over_attr(attrName,data,xlim=None):

    # logging.info("start to plotting {}, length of data {} ....".format(attrName,len(data)))

    # print(data.keys())

    year_div_dis,subj_div_dis,c10_div_dis = data

    fig,axes = plt.subplots(3,1,figsize=(5,12))

    ax = axes[0]
    xs = []
    ys_mean = []
    ys_median = []
    for year in sorted(year_div_dis.keys()):
        xs.append(year)
        ys_mean.append(np.mean(year_div_dis[year]))
        ys_median.append(np.median(year_div_dis[year]))

    ax.plot(xs,ys_mean,'-.',label = 'mean')
    ax.plot(xs,ys_median,'-.',label ='median')

    ax.set_xlabel('{}'.format(attrName))
    ax.set_ylabel('year diversity')
    ax.set_title('year diversity')

    if xlim is not None:
        ax.set_xlim(xlim[0],xlim[1])


    ax = axes[1]
    xs = []
    ys_mean = []
    ys_median = []
    for year in sorted(subj_div_dis.keys()):
        xs.append(year)
        ys_mean.append(np.mean(subj_div_dis[year]))
        ys_median.append(np.median(subj_div_dis[year]))


    ax.plot(xs,ys_mean,'-.',label = 'mean')
    ax.plot(xs,ys_median,'-.',label = 'median')

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
        ys_mean.append(np.mean(c10_div_dis[year]))
        ys_median.append(np.median(c10_div_dis[year]))


    ax.plot(xs,ys_mean,'-.',label = 'mean')
    ax.plot(xs,ys_median,'-.',label = 'median')

    ax.set_xlabel('{}'.format(attrName))
    ax.set_ylabel('impact diversity')

    ax.set_title('impact diversity')

    if xlim is not None:
        ax.set_xlim(xlim[0],xlim[1])


    plt.tight_layout()

    plt.savefig('fig/diversity_over_{}.png'.format(attrName.replace(' ','_')),dpi=400)
    logging.info("fig saved to fig/diversity_over_{}.png.".format(attrName.replace(' ','_')))



def dataHist(data):

    hists,bins_edges = np.histogram(data,bins=500)

    centers = np.array(bins_edges[:-1]+bins_edges[1:])/float(2)

    t = np.sum(hists)

    hists = [np.sum(hists[:i+1])/float(t) for i in range(len(hists))]

    return centers,hists


## 随领域的分布
def subject_div():

    pass


## 与citation count之间的关系
def impact_div():

    pass



if __name__ == '__main__':
    year_div()