#coding:utf-8
import sys 
sys.path.append('src')
from basic_config import *

'''
一共117本ABS四星以上期刊，一共找到91本，放在了data/abs.used_journal.txt

91本期刊中一种374,838篇论文。

'''

def filter_4_star_journal():
    journal_names = ['jname==star']
    for line in open('data/abs.journal.txt'):
        if '==4' in line:
            line = line.strip()

            field,jname,issn,star =line.split("==")

            if '4' in jname:

                jname = field
            
            journal_names.append(f'{jname}=={star}')
    
    open('data/ABS4star.journal.txt','w').write('\n'.join(journal_names))


def search_abs_journal_paper():
    jnames = set([line.strip().split('==')[0].lower().replace(',','') for line in open('data/ABS4star.journal.txt')])
    # jnames = set([line.strip().split('==')[0]
                #  for line in open('data/ABS4star.journal.txt')])

    query_op = dbop()
    jids = []

    founded_jnames = []
    sql = 'select journal_id,normalized_name,display_name from mag_core.journals'
    for jid, jname, display_name in query_op.query_database(sql):

        if jname in jnames:
            jids.append(jid)
            founded_jnames.append(display_name)
    
    open('data/abs_jid.txt','w').write('\n'.join(jids))
    open('data/abs.used_journal.txt','w').write('\n'.join(founded_jnames))

    logging.info(f'{len(jnames)} journals in total, found {len(jids)} journals in MAG.')

# 获得ABS对应的期刊论文
def get_abs_paper_ids():
    jids  = set([line.strip() for line in open('data/abs_jid.txt')])

    query_op = dbop()
    sql = 'select paper_id,journal_id from mag_core.papers'
    pid_jid = {}
    pids = []

    for pid,jid in query_op.query_database(sql):
        if str(jid) in jids:
            pid_jid[pid] = jid
            pids.append(pid)

    open('data/abs.paper_jid.json','w').write(json.dumps(pid_jid))

    open('data/abs_pids.txt','w').write('\n'.join(pids))

    logging.info(f'{len(pids)} abs papers founded.')



# 自变量计算
'''
1. Topic Diversity --- DIV citing角度的，Raw sIRLING是哪个？
2. Freshness Diverisity --- year difference diversity
3. Impact Diversity
    3.1 参考文献的被引次数的gini系数
    3.2 参考文献 d10的gini系数
    3.3 参考文献期刊影响因子gini系数，只能瞎算，有的可能引用期刊或者会议
    3.4 归一化影响一字，这个比较难算了就，顶多一起归一化。

'''
def paper_independent_variables():

    pass


#ABS期刊论文的控制变量
'''
控制变量包括
1. 团队大小
2. 作者学术年龄 均值和std
3. 机构ranking  均值和std
4. 论文发表年份
5. 论文所在期刊

'''
def paper_control_variables():

    pids = set([line.strip() for line in open('data/abs_pids.txt')])

    # 团队大小
    pid_authors = defaultdict(list)
    pid_affs = defaultdict(list)
    pid_year = {}
    pid_jid = {}

    auids = []

    query_op = dbop()
    sql = 'select A.paper_id,A.author_id,A.affiliation_id,B.rank,C.year,C.journal_id from mag_core.paper_author_affiliations as A, mag_core.affiliations as B, mag_core.papers as C where C.paper_id = A.paper_id and A.affiliation_id = B.affiliation_id'
    for pid,auid,affid,affrank,pubyear,pubjournal in query_op.query_database(sql):
        if pid not in pids:
            continue

        pid_authors[pid].append(auid)
        pid_affs[pid].append(affrank)
        pid_year[pid] = int(pubyear)
        pid_jid[pid] = pubjournal

        auids.append(auid)
    
    logging.info(f'{len(pid_year)} papers author are read.')

    #获得作者发表论文的年份
    auids = set(auids)
    auid_pyears = defaultdict(list) 
    auid_cns = defaultdict(list)
    sql = 'select A.paper_id, A.year,A.citation_count,B.author_id from mag_core.papers as A, mag_core.paper_author_affiliations as B where A.paper_id = B.paper_id'
    for pid, year, cn, auid in query_op.query_database(sql):
        if auid in auids:
            auid_pyears[auid].append(int(year))
            auid_cns[auid].append(int(cn))
    
    logging.info(f'{len(auid_pyears)} papers author are read.')

    
    # 计算论文这一年作者的研究年龄，作者论文数量，作者已发表论文平均引用
    # 这里的引用次数是所有的引用次数，后面可以改为c2 c5 c10
    pid_author_ages = defaultdict(list)
    pid_author_pnums = defaultdict(list)
    pid_author_cns = defaultdict(list)

    for pid in pid_authors.keys():
        pyear= pid_year[pid]
        for auid in pid_authors[pid]:
            years = auid_pyears[auid]
            cns = auid_cns[auid]
            #作者的研究年龄 
            age = pyear - np.min(years)
            pid_author_ages[pid].append(age)
            # 作者已发表论文数量
            pnum = 0
            cn = 0
            for i,y in enumerate(years):
                if y<=pyear:
                    pnum+=1
                    cn+=cns[i]
            # 作者在此之前发表的论文数量及获得的引用总次数
            pid_author_pnums[pid].append(pnum)
            pid_author_cns[pid].append(cn)
    
    logging.info(f'{len(pid_author_ages)} papers age attrs are read.')

    
    lines= ['paper_id,year,journal id,teamsize,age mean,age std,pnum mean,pnum std,cn mean,cn_std,rank mean,rank std']
    
    for pid in pid_year.keys():

        # 团队大小
        teamsize = len(pid_author_ages[pid])
        # 作者研究年龄
        ages = pid_author_ages[pid]
        age_mean = np.mean(ages)
        age_std = np.std(ages)
        # 作者已发表论文数量
        pnums = pid_author_pnums[pid]
        pnum_mean = np.mean(pnums)
        pnum_std = np.std(pnums)
        # 作者已发表论文的引用次数
        cns = pid_author_cns[pid]
        cn_mean = np.mean(cns)
        cn_std = np.std(cns)
        # 机构ranking
        ranks = pid_affs[pid]
        rank_mean = np.mean(ranks)
        rank_std = np.std(ranks)
        # journal 
        jid = pid_jid[pid]
        # year 
        year = pid_year[pid]

        lines.append(f'{pid},{year},{jid},{teamsize},{age_mean},{age_std},{pnum_mean},{pnum_std},{cn_mean},{cn_std},{rank_mean},{rank_std}')
    
    open('data/ABS.controlVariables.csv','w').write('\n'.join(lines))
    logging.info(f'{len(lines)} paper control variables are saved.')

# 因变量计算
'''
1. citation相关 c_2,c_5,c_10
2. Disruption相关 d_2,d_5,d_10
3. Novelty相关 n_2,n_5,n_10

'''
def paper_dependent_variables():

    pass



if __name__ == "__main__":
    # filter_4_star_journal()
    # search_abs_journal_paper()
    # get_abs_paper_ids()

    paper_control_variables()
