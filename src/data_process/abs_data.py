#coding:utf-8
import sys 
sys.path.append('src')
from basic_config import *

'''
一共117本ABS四星以上期刊，一共找到91本，放在了data/abs.used_journal.txt



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


if __name__ == "__main__":
    # filter_4_star_journal()
    # search_abs_journal_paper()
    get_abs_paper_ids()
