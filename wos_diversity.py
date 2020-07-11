#coding:utf-8

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


## 根据引用来计算来计算每一篇论文的diversity
def cal_wos_paper_divs():

    pid_pubyear,pid_subjects,pid_topsubjs,pid_teamsize = load_basic_data()
    ## pid c5
    pid_c5 = json.loads(open('../WOS_data_processing/data/pid_c5.json').read())
    ## pid_c10
    pid_c10 = json.loads(open('../WOS_data_processing/data/pid_c10.json').read())
    ## subject subject sim
    subj_subj_sim  = json.loads(open('../WOS_data_processing/data/subj_subj_sim.json').read())

    subj_totalnum = float(len(subj_subj_sim.keys()))
    
    pid_divs = {}
    for line in open('../WOS_data_processing/data/pid_teamsize.json'):

        line = line.strip()

        pid_refs = json.loads(line)

        for pid in pid_refs.keys():

            if len(pid_refs[pid])<4:

                continue

            puyear = int(paper.get(pid,9999))

            ## 1950年 到 如果年份大于2004则舍弃
            if pubyear>2004 or pubyear<1950:
                continue

            ## 对于每一篇文章来讲 需要计算三个

            ## year differences
            ## subject diversity
            ## c5 diversity
            ## c10 diversity
            yds = []
            subjs = []
            subj_nums = []
            c5s = []
            c10s = []
            for ref_id in pid_refs:

                yds.append(abs(int(pid_pubyear[ref_id])-pubyear))

                c5s.append(pid_c5[ref_id])

                c10s.append(pid_c10[ref_id])

                subj_nums.append(len(pid_subjects.get(ref_id,[])))

                subjs.extend(pid_subjects[ref_id])


            ## 通过上面的值计算每篇论文reference的diversity


            yd_div = gini(yds)
            c5_div = gini(c5s)
            c10_div = gini(c10s)

            subjs = list(set(subjs))

            subj_div = cal_subj_div(subj_nums,subjs,subj_subj_sim)

            pid_divs[pid] = [yd_div,subj_div,c5_div,c10_div]

    open('data/pid_divs.json','w').write(json.dumps(pid_divs))
    logging.info('{} papers div data saved to data/pid_divs.json'.format(len(pid_divs.keys())))



def cal_subj_div(subj_nums,subjs,subj_subj_sim):

    variety = len(subjs)/float(subj_totalnum)

    balance = gini(subj_num)

    disparsity = cal_disparsity(subjs,subj_subj_sim)


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
    cal_wos_paper_divs()









