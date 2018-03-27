#coding:utf-8
'''
    calculate diversity of papers.

'''
from basic_config import *


def cal_diversity(com_ids_cc_path,com_ids_subjects_path,selected_IDs_references_path,year_differences_path):

    logging.info('loading com_ids_cc ...')
    com_ids_cc = json.loads(open(com_ids_cc_path).read())

    logging.info('loading com_ids_subjects ...')
    com_ids_subjects = json.loads(open(com_ids_subjects_path).read())

    logging.info('loading papers and references ...')
    selected_IDs_references = defaultdict(list)
    for line in open(selected_IDs_references_path):
        line = line.strip()
        pid,ref_id = line.split("\t")
        selected_IDs_references[pid].append(ref_id)


    cc_pid_diversity=defaultdict(float)
    subject_pid_diversity = defaultdict(float)

    selected_IDs = selected_IDs_references.keys()
    length = len(selected_IDs)

    for i,pid in enumerate(selected_IDs):

        if (i+1)%100000==0:
            logging.info('progress {:}/{:} ...'.format((i+1),length))


        cc_list = []
        subject_list = []

        for ref_id in selected_IDs_references[pid]:

            if '.' in ref_id:
                continue

            cc = com_ids_cc.get(ref_id,0)

            subjects = com_ids_subjects.get(ref_id,[])

            cc_list.append(cc)
            subject_list.extend(subjects)

        # print cc_list
        if len(cc_list)>0:
            cc_gini = gini(cc_list)
            cc_pid_diversity[pid] = cc_gini

        if len(subject_list)>0:
            subject_gini = gini(Counter(subject_list).values())
            subject_pid_diversity[pid] = subject_gini



    open('data/wos_cc_diversity.json','w').write(json.dumps(cc_pid_diversity))
    logging.info("saved to data/wos_cc_diversity.json.")

    open('data/wos_subject_diversity.json','w').write(json.dumps(subject_pid_diversity))
    logging.info('saved to data/wos_subject_diversity.json')

    year_differences = json.loads(open(year_differences_path).read())

    yd_pid_diversity = defaultdict(float)
    for pid in year_differences.keys():
        yd_pid_diversity[pid]=gini(year_differences[pid])

    open('data/wos_year_differences_diversity.json','w').write(json.dumps(yd_pid_diversity))
    logging.info('saved to data/wos_year_differences_diversity.json')


def plot_diversity(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path):
    logging.info('loading data from diversity files ...')
    wos_cc_diversity = json.loads(open(wos_cc_diversity_path).read())
    wos_subject_diversity = json.loads(open(wos_subject_diversity_path).read())
    wos_year_differences_diversity = json.loads(open(wos_year_differences_diversity_path).read())

    cc_diversity_values = [i for i in wos_cc_diversity.values() if i>0]
    subject_diversity_values = [i for i in wos_subject_diversity.values() if i>0]
    year_differences_diversity_values = [i for i in wos_year_differences_diversity.values() if i > 0]

    logging.info('Size of cc diversity:{:}, Size of subject diversity:{:}, Size year differences diversity:{:} . '.format(len(cc_diversity_values),len(subject_diversity_values),len(year_differences_diversity_values)))

    logging.info('plotting figures ...')
    
    plt.figure(figsize=(6,4))
    plt.hist(cc_diversity_values,bins=30)   
    plt.xlabel('impact diversity')
    plt.ylabel('number of papers')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/impact_diversity_dis.pdf',dpi=200)

    plt.figure(figsize=(6,4))
    plt.hist(subject_diversity_values,bins=30)    
    plt.xlabel('subject diversity')
    plt.ylabel('number of papers')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/subject_diversity_dis.pdf',dpi=200)

    plt.figure(figsize=(6,4))
    plt.hist(year_differences_diversity_values,bins=30)   
    plt.xlabel('year diversity')
    plt.ylabel('number of papers')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('pdf/year_differences_diversity_dis.pdf',dpi=200)

    logging.info('done ...')


def diversity_impact(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path,com_ids_cc_path):

    logging.info('loading id->citation count')
    com_ids_cc = json.loads(open(com_ids_cc_path).read())
    logging.info('loading wos cc diversity ..')
    wos_cc_diversity = json.loads(open(wos_cc_diversity_path).read())

    xs = []
    ys = []
    for pid in wos_cc_diversity.keys():
        cc_diversity  = wos_cc_diversity[pid]

        cc = com_ids_cc.get(pid,0)

        ys.append(cc)
        xs.append(cc_diversity)

    plt.figure()
    plt.scatter(xs,ys,c=color_sequence[0])

    plt.xlabel('impact diversity')
    plt.ylabel('citation count')

    plt.tight_layout()
    plt.savefig('pdf/impact_diversity_impact.pdf',dpi=200)



if __name__ == '__main__':
    
    com_ids_cc_path = 'data/com_ids_cc.json'
    # selected_ids_references_path ='data/selected_IDs_references.txt'
    # com_ids_subjects_path = 'data/com_ids_subjects.json'
    # year_differences_path = 'data/statistics/year_differences.json'
    # cal_diversity(com_ids_cc_path,com_ids_subjects_path,selected_ids_references_path,year_differences_path)

    wos_cc_diversity_path = 'data/wos_cc_diversity.json'
    wos_subject_diversity_path = 'data/wos_subject_diversity.json'
    wos_year_differences_diversity_path = 'data/wos_year_differences_diversity.json'

    # plot_diversity(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path)

    diversity_impact(wos_cc_diversity_path,wos_subject_diversity_path,wos_year_differences_diversity_path,com_ids_cc_path)









