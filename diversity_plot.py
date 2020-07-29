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

    paper_year,paper_topsubjs,paper_ts = load_basic_data(['year','topsubj','teamsize'])

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


    progress = 0 
    

    line = line.strip()
    pid_div_vs = json.loads(open("data/pid_divs.json").read())
    for pid in pid_div_vs.keys():

        progress+=1

        if progress%100000==0:

            logging.info("progress {} ....".format(progresss))


        year = int(paper_year.get(pid,9999))

        ts = int(paper_ts.get(pid,-1))

        subjs = paper_topsubjs.get(pid,None)

        if year>2004:
            continue


        # year_div,c5_div,c10_div,subj_div = pid_div_vs[pid]

        year_div,subj_div,c5_div,c10_div = pid_div_vs[pid]

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


    plot_dis_over_attr('publication year',(year_div_dis,subj_div_dis,c10_div_dis))

    plot_dis_over_attr('team size',(ts_year_dis,ts_subj_dis,ts_c10_dis))

    # plot_dis_over_attr('field',(fos_year_dis,fos_subj_dis,fos_c10_dis))

def plot_dis_over_attr(attrName,data):

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


    plt.tight_layout()

    plt.savefig('fig/diversity_over_{}.png'.format(attrName.replace(' ','_')),dpi=400)
    logging.info("fig saved to fig/diversity_over_{}.png.".format(attrName.replace(' ','_')))



## 随领域的分布
def subject_div():

    pass


## 与citation count之间的关系
def impact_div():

    pass



if __name__ == '__main__':
    year_div()