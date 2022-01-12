#coding:utf-8
import sys 
sys.path.append('src')
from basic_config import *

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
    query_op = dbop()
    jids = []
    sql = 'select journal_id,normalized_name,display_name from mag_core.journals'
    for jid, jname, display_name in query_op.query_database(sql):

        if jname in jnames:
            jids.append(jid)
    
    open('data/abs_jid.txt','w').write('\n'.join(jids))

    logging.info(f'{len(jnames)} journals in total, found {len(jids)} journals in MAG.')



if __name__ == "__main__":
    # filter_4_star_journal()
    search_abs_journal_paper()
