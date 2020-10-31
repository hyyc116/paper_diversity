#coding:utf-8
'''
Total paper num: 16531796 ,total num of citation links: 284895705
reserved paper num: 13561705 ,reserved num of citation links: 259070878

[description]
'''


## 数据使用 1950-2004年的数据
from basic_config import *

from gini import gini

def load_basic_data(isStat=False):

    logging.info('======== LOADING BASIC DATA =============')
    logging.info('======== ================== =============')


    logging.info('loading paper pubyear ...')
    pid_pubyear = json.loads(open('../WOS_data_processing/data/pid_pubyear.json').read())
    logging.info('{} papers has year label.'.format(len(pid_pubyear.keys())))

    logging.info('loading paper subjects ...')
    pid_subjects = json.loads(open('../WOS_data_processing/data/pid_subjects.json').read())
    logging.info('{} papers has subject label.'.format(len(pid_subjects.keys())))

    logging.info('loading paper top subjects ...')
    pid_topsubjs = json.loads(open('../WOS_data_processing/data/pid_topsubjs.json').read())
    logging.info('{} papers has top subject label.'.format(len(pid_topsubjs.keys())))

    logging.info('loading paper teamsize ...')
    pid_teamsize = json.loads(open('../WOS_data_processing/data/pid_teamsize.json').read())
    logging.info('{} papers has teamsize label.'.format(len(pid_teamsize.keys())))

    if isStat:
        interset = set(pid_pubyear.keys())&set(pid_teamsize.keys())&set(pid_topsubjs.keys())&set(pid_topsubjs.keys())
        logging.info('{} papers has both four attrs.'.format(len(interset)))

    logging.info('======== LOADING BASIC DATA DONE =============')
    logging.info('======== ======================= =============')

    return pid_pubyear,pid_subjects,pid_topsubjs,pid_teamsize


def nums_to_percentile_dict(nums):
    num_counter = Counter(nums)
    
    total=len(nums)
    num_t = 0

    num_percentile = {}
    for num in sorted(num_counter.keys()):
        num_t+=num
        percentile = int(num_t*100/total)

        num_percentile[num] = percentile

    num_percentile[0] = 0

    return num_percentile

## 根据引用来计算来计算每一篇论文的diversity
def cal_wos_paper_divs():

    pid_pubyear,pid_subjects,pid_topsubjs,pid_teamsize = load_basic_data()
    ## pid c2
    pid_c2 = json.loads(open('../WOS_data_processing/data/pid_c2.json').read())
    ## pid c5
    pid_c5 = json.loads(open('../WOS_data_processing/data/pid_c5.json').read())
    ## pid_c10
    pid_c10 = json.loads(open('../WOS_data_processing/data/pid_c10.json').read())
    ## subject subject sim
    subj_subj_sim  = json.loads(open('../WOS_data_processing/data/subj_subj_sim.json').read())

    #  计算c2 c5 c10的percentile
    c2_percentile = nums_to_percentile_dict(pid_c2.values())
    c5_percentile = nums_to_percentile_dict(pid_c5.values())
    c10_percentile = nums_to_percentile_dict(pid_c10.values())


    subj_totalnum = float(len(subj_subj_sim.keys()))
    
    pid_divs = {}

    progress = 0

    sub_progress = 0

    total_paper_num = 0

    total_cit_num = 0

    selected_paper_num = 0

    selected_cit_num = 0

    cn_dis = defaultdict(int)

    ref_nums = defaultdict(int)

    for line in open('../WOS_data_processing/data/pid_refs.txt'):

        line = line.strip()

        progress+=1

        pid_refs = json.loads(line)

        for pid in pid_refs.keys():

            sub_progress+=1

            if sub_progress%1000000==0:
                logging.info('progress:{},sub progress {} ...'.format(progress,sub_progress))

            pubyear = int(pid_pubyear.get(pid,9999))

            ## 1980年 到 如果年份大于2004则舍弃
            if pubyear>2004 or pubyear<1980:
                continue

            total_paper_num+=1

            total_cit_num+=len(pid_refs[pid])

            ref_nums[len(pid_refs[pid])]+=1

            if len(pid_refs[pid])<4 or len(pid_refs[pid])>100:
                continue


            selected_cit_num+=len(pid_refs[pid])
            selected_paper_num+=1

            ## 对于每一篇文章来讲 需要计算三个
            ## year differences
            ## subject diversity
            ## c5 diversity
            ## c10 diversity
            yds = []
            subjs = []
            subj_nums = []
            c2s = []
            c5s = []
            c10s = []


            c2ps = []
            c5ps = []
            c10ps = []

            for ref_id in pid_refs[pid]:

                yds.append(abs(int(pid_pubyear[ref_id])-pubyear))

                c2s.append(pid_c2.get(ref_id,0))

                c5s.append(pid_c5.get(ref_id,0))

                c10s.append(pid_c10.get(ref_id,0))

                c2ps.append(c2_percentile[pid_c2.get(ref_id,0)])

                c5ps.append(c5_percentile[pid_c5.get(ref_id,0)])

                c10ps.append(c10_percentile[pid_c10.get(ref_id,0)])

                subj_nums.append(len(pid_subjects.get(ref_id,[])))

                subjs.extend(pid_subjects[ref_id])

                cn_dis[ref_id]+=1


            ## 通过上面的值计算每篇论文reference的diversity
            yd_div = gini(yds)
            c2_div = gini(c2s)
            c5_div = gini(c5s)
            c10_div = gini(c10s)
            # 均值以及std
            yd_mean = np.mean(yds)
            yd_std = np.std(yds)
            #
            c2_mean = np.mean(c2s)
            c2_std = np.std(c2s)
            #
            c5_mean = np.mean(c5s)
            c5_std = np.std(c5s)
            #
            c10_mean = np.mean(c10s)
            c10_std = np.std(c10s)

            c2p_div = gini(c2ps)
            c5p_div = gini(c5ps)
            c10p_div = gini(c10ps)

            c2p_mean = np.mean(c2ps)
            c2p_std = np.std(c2ps)
            #
            c5p_mean = np.mean(c5ps)
            c5p_std = np.std(c5ps)
            #
            c10p_mean = np.mean(c10ps)
            c10p_std = np.std(c10ps)


            subjs = list(set(subjs))

            if len(subjs)<=1:
                subj_div = 0

            else:
                subj_div = cal_subj_div(subj_totalnum,subj_nums,subjs,subj_subj_sim)


            pid_divs[pid] = [yd_div,subj_div,c2_div,c5_div,c10_div,yd_mean,yd_std,c2_mean,c2_std,c5_mean,c5_std,c10_mean,c10_std,c2p_div,c5p_div,c10p_div,c2p_mean,c2p_std,c5p_mean,c5p_std,c10p_mean,c10p_std]

    open('data/pid_divs.json','w').write(json.dumps(pid_divs))
    logging.info('{} papers div data saved to data/pid_divs.json'.format(len(pid_divs.keys())))

    # 将现有的需要统计的指标进行列出来
    print('===============================')
    print('Total paper num:',total_paper_num,',total num of citation links:',total_cit_num)
    print('reserved paper num:',selected_paper_num,',reserved num of citation links:',selected_cit_num)

    # 将保留的引用次数分布画出来
    cc_counter = Counter(cn_dis.values())

    xs = []
    ys = []
    for cc in sorted(cc_counter.keys()):

        if cc==100:
            print('Number of papers cited 100 times:',cc_counter[cc])

        xs.append(cc)
        ys.append(cc_counter[cc])

    plt.figure(figsize=(7,5))

    plt.plot(xs,ys,'o',fillstyle='none')

    plt.xscale('log')

    plt.yscale('log')

    plt.xlabel('number of citations')

    plt.ylabel('number of publications')

    plt.tight_layout()

    plt.savefig('fig/citation_distritbuion.png',dpi=400)

    # 将refnum_distribution进行画出来

    xs = []
    ys = []
    for rn in sorted(ref_nums.keys()):

        if rn>100 :
            continue

        xs.append(rn)
        ys.append(ref_nums[rn])

    plt.figure(figsize=(7,5))
    plt.plot(xs,ys)
    
    plt.xlabel('number of references')
    plt.ylabel('number of publications')

    plt.xscale('log')

    plt.yscale('log')

    plt.tight_layout()

    plt.savefig('fig/refnum_distribution.png',dpi=400)    

    print('DONE')


def cal_subj_div(subj_totalnum,subj_nums,subjs,subj_subj_sim):

    variety = len(subjs)/float(subj_totalnum)

    balance = gini(subj_nums)

    disparsity = cal_disparsity(subjs,subj_subj_sim)

    return variety*balance*disparsity


def cal_disparsity(subjs,subj_subj_sim):
    subjs = list(subjs)
    all_dij = []
    for i in range(len(subjs)):
        for j in range(i+1,len(subjs)):
            if i==j:
                continue
            subj1 = subjs[i]
            subj2 = subjs[j]
            dij = 1-subj_subj_sim[subj1].get(subj2,0)
            all_dij.append(dij)

    return np.mean(all_dij)


if __name__ == '__main__':
    # cal_wos_paper_divs()

    ## pid c2
    pid_c2 = json.loads(open('../WOS_data_processing/data/pid_c2.json').read())

    print(nums_to_percentile_dict(pid_c2.values()))









