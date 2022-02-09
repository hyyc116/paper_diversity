#coding:utf-8

import sys
sys.path.append('src')
from basic_config import *

from diversity_cal import cal_subj_div
from gini import *

'''
一共117本ABS四星以上期刊，一共找到91本，放在了data/abs.used_journal.txt

91本期刊中一种374,838篇论文。

198,927
1,433,193

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
1. Topic Diversity --- DIV citing角度的，Raw sIRLING是哪个？，计算两个领域之间的相似度
2. Freshness Diverisity --- year difference diversity，每一个参考文献的发表年份
3. Impact Diversity
    3.1 参考文献的被引次数的gini系数，每一个参考文献的c10
    3.2 参考文献 d10的gini系数, 每一篇论文的d10
    3.3 参考文献期刊影响因子gini系数，只能瞎算，有的可能引用期刊或者会议
    3.4 归一化影响一字，这个比较难算了就，顶多一起归一化。

    TODO: 期刊影响因子计算

'''
def paper_independent_variables():
    # 一共多少主题、这个reference有多少主题
    # 主题的GINI
    # 主题和主题之间的相似度的平均值

    # 使用所有的id的参考文献 + 参考文献
    pids = set([line.strip() for line in open('data/abs_pids.txt')])

    pid_pubyear = json.loads(
        open('../MAG_data_processing/data/pid_pubyear.json').read())

    paper_c10 = json.loads(open('data/ABS.paper_c10.json').read())

    paper_dn = json.loads(open('data/ABS.paper_dn.json').read())
    # 一篇论文对应的主题列表
    paper_subjs = json.loads(open('data/pid_subjs.json').read())
    # 主题之间的互相引用
    subj_subj_refnum = json.loads(open('data/subj_subj_refnum.json').read())
    # 主题数量
    total_subjnum = len(subj_subj_refnum.keys())
    # 每一个学科被引总次数
    citnum_total = defaultdict(int)
    for subj in subj_subj_refnum.keys():
        for subj2 in subj_subj_refnum[subj].keys():
            citnum_total[subj2] += subj_subj_refnum[subj][subj2]

    logging.info(f'total number of abs ids is {len(pids)}')
    # 获得ABS参考文献的id
    query_op = dbop()
    sql = "select paper_id,paper_reference_id from mag_core.paper_references"
    pid_refs = defaultdict(list)
    for pid,ref_pid in query_op.query_database(sql):
        if pid in pids:
            pid_refs[pid].append(ref_pid)

    pid_attrs = {}

    # 计算diversity
    for pid in pid_refs.keys():
        pyear = pid_pubyear.get(pid,None)
        if pyear is None:
            continue

        pyear = int(pyear)

        # freshness diversity
        freshenesses = []
        c10s = []
        d10s = []

        all_subjs = []

        # 每一个参考文献
        for ref in pid_refs[pid]:

            refyear = pid_pubyear.get(ref, None)
            if refyear is None:
                continue

            freshness = int(pyear - int(refyear))

            freshenesses.append(freshness)

            c10s.append(paper_c10.get(ref,0))

            dns = paper_dn.get(ref,[0,0,0])
            d10s.append(dns[2])

            all_subjs.extend(paper_subjs.get(ref,[]))

        subj_div,variety,balance,disparsity = cal_subj_div(all_subjs, subj_subj_refnum, total_subjnum,
                                citnum_total)
        freshness_diversity = gini(freshenesses)
        c10_diversity = gini(c10s)
        d10_diversity = gini(d10s)

        pid_attrs[pid] = [
            freshness_diversity, c10_diversity, d10_diversity, subj_div,
            variety, balance, disparsity
        ]

    open('data/ABS_independent.json','w').write(json.dumps(pid_attrs))
    logging.info('data saved  to data/ABS_independent.json.')


# 需要对论文的领域进行计算
# subject用几级的field标签
# journal的期刊影响因子需要每年都计算
def paper_journal_subjects():
    # 每一个论文的二级领域
    # 每一篇论文的journal ALL_pids.txt
    # 二级领域之间的引用次数
    # 根据引用关系计算领域之间的相似度

    sql = 'select A.paper_id,A.field_of_study_id,B.level from mag_core.paper_fields_of_study as A, mag_core.fields_of_study as B where A.field_of_study_id = B.field_of_study_id and B.level = 1'
    paper_subjs = defaultdict(list)
    query_op = dbop()
    for pid,fid,_ in query_op.query_database(sql):

        paper_subjs[pid].append(fid)

    sql = "select paper_id,paper_reference_id from mag_core.paper_references"
    query_op.query_database(sql)

    subj_subj_refnum = defaultdict(lambda:defaultdict(int))
    for pid,ref_pid in query_op.query_database(sql):

        subjs = paper_subjs[pid]
        ref_subjs = paper_subjs[ref_pid]

        for s1 in subjs:
            for s2 in ref_subjs:
                subj_subj_refnum[s1][s2]+=1

    open('data/pid_subjs.json','w').write(json.dumps(paper_subjs))

    open('data/subj_subj_refnum.json','w').write(json.dumps(subj_subj_refnum))

    logging.info('data saved to data/subj_subj_refnum.json.')


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

    # 使用所有的id的参考文献 + 参考文献
    pids = set([line.strip() for line in open('data/ABS.ALL_pids.txt')])

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
3. Novelty相关 n_2,n_5,n_10  需要计算n年前参考文献的共被引次数， 目前不计算

'''
def paper_dependent_variables():
    pid_pubyear = json.loads(
        open('../MAG_data_processing/data/pid_pubyear.json').read())

    # 获得abs论文及其参考文献每一年的引用次数
    abs_pids = set([line.strip() for line in open('data/abs_pids.txt')])

    abs_pid_c2 = defaultdict(int)
    abs_pid_c5 = defaultdict(int)
    abs_pid_c10 = defaultdict(int)

    logging.info(f'total number of abs ids is {len(abs_pids)}')
    # 获得ABS参考文献的id
    query_op = dbop()
    sql = "select paper_id,paper_reference_id from mag_core.paper_references"

    all_ids = []
    # 获得ABS的论文参考文献
    for pid,ref_id in query_op.query_database(sql):
        if pid in abs_pids:
            all_ids.append(pid)
            all_ids.append(ref_id)

    all_ids = set(all_ids)
    # 还需要获得参考文献的参考文献
    for pid, ref_id in query_op.query_database(sql):
        if pid in all_ids:
            all_ids.add(pid)
            all_ids.add(ref_id)

    # 记录所有需要记录的文章的参考文献
    abs_pid_refs = defaultdict(list)
    for pid, ref_id in query_op.query_database(sql):
        if pid in all_ids:
            abs_pid_refs[pid].append(ref_id)


    all_ids = set(all_ids)
    # 存储所有的id
    open('data/ABS.ALL_pids.txt','w').write('\n'.join(list(all_ids)))

    logging.info(f'total number of ids is {len(all_ids)}')

    # 获得每一篇参考文献每年的引用次数
    paper_year_cits = defaultdict(lambda:defaultdict(list))

    for pid, ref_id in query_op.query_database(sql):
        if ref_id in all_ids:
            pid_year = int(pid_pubyear[pid])
            paper_year_cits[ref_id][pid_year].append(pid)

            pyear = pid_pubyear[pid]
            refyear = pid_pubyear[ref_id]

            if ref_id in abs_pids:

                if int(pyear)-int(refyear) < 2:
                    abs_pid_c2[ref_id]+=1

                if int(pyear)-int(refyear) < 5:
                    abs_pid_c5[ref_id]+=1

                if int(pyear)-int(refyear) < 10:
                    abs_pid_c10[ref_id] += 1

    open('data/ABS.paper_c2.json', 'w').write(json.dumps(abs_pid_c2))
    open('data/ABS.paper_c5.json', 'w').write(json.dumps(abs_pid_c5))
    open('data/ABS.paper_c10.json', 'w').write(json.dumps(abs_pid_c10))

    # open('data/ABS.ALLid.year_citnum.json','w').write(json.dumps(paper_year_cits))

    logging.info('data saved.')

    pid_dn = {}

    progress = 0
    # 计算每一篇论文的dn
    for pid in list(abs_pids):

        progress+=1

        if progress%10000==0:
            logging.info(f'progress {progress}...')

        # 这篇论文
        year_cits = paper_year_cits[pid]

        years = [int(y) for y in year_cits.keys()]

        if len(years)==0:
            continue

        min_year = np.min(years)

        pid2_cits, pid5_cits, pid10_cits = get_c2510_papers(min_year, year_cits)

        refs = abs_pid_refs[pid]

        ref2_cits = []
        ref5_cits = []
        ref10_cits = []
        for ref in refs:

            ref_year_cits = paper_year_cits[ref]

            refc2papers, refc5papers, refc10papers = get_c2510_papers(
                min_year, ref_year_cits)

            ref2_cits.extend(refc2papers)
            ref5_cits.extend(refc5papers)
            ref10_cits.extend(refc10papers)

        d2 = cal_dn(pid2_cits,ref2_cits)
        d5 = cal_dn(pid5_cits,ref5_cits)
        d10 = cal_dn(pid10_cits,ref10_cits)

        pid_dn[pid] = [d2,d5,d10]

    open('data/ABS.paper_dn.json',
         'w').write(json.dumps(pid_dn))

    logging.info('data saved to data/ABS.paper_dn.json.')



def cal_dn(pid_cits, ref_cits):

    pid_cits = set(pid_cits)
    ref_cits = set(ref_cits)

    i = float(len(pid_cits - ref_cits))
    j = float(len(ref_cits & pid_cits))
    k = float(len(ref_cits - pid_cits))

    if i + j + k == 0:
        return 0

    return float(i - j) / float((i + j + k))


def get_c2510_papers(start_year,year_cits):
    c2papers = []
    c5papers = []
    c10papers = []

    for i in range(11):

        if i<=2:
            c2papers.extend(year_cits.get(start_year+i, []))

        if i<=5:
            c5papers.extend(year_cits.get(start_year+i, []))

        if i <= 10:
            c10papers.extend(year_cits.get(start_year+i, []))

    return c2papers,c5papers,c10papers


if __name__ == "__main__":
    # filter_4_star_journal()
    # search_abs_journal_paper()
    # get_abs_paper_ids()


    # paper_dependent_variables()

    # paper_control_variables()

    # paper_journal_subjects()

    paper_independent_variables()
