#coding:utf-8
'''
    Visualizing data from web of science through following steps:
    1. plot number of papers in Physics published over published year   
    2. Distribution of number of citations of Physics papers
    3. average number of citation over year
    3. Reference Number distribution of Physics Papers
    4. year difference distribution of Physics papers
    5. Subjects distribution-- todo

'''

from basic_config import *

def plot_statistics(selected_IDs_path,com_IDs_year_path,com_IDs_cc_path,selected_IDs_references_path,com_IDs_subjects_path):
    ## selected Ids
    logging.info("loads selected IDs from {:} ...".format(selected_IDs_path))
    selected_IDs = [line.strip() for line in open(selected_IDs_path)]

    ## ID_year
    logging.info('loads year dict from {:} ...'.format(com_IDs_year_path))
    com_IDs_year = json.loads(open(com_IDs_year_path).read())

    ## ID_cc
    logging.info('loads citation count from {:} ...'.format(com_IDs_cc_path))
    com_IDs_cc = json.loads(open(com_IDs_cc_path).read())

    ## ID_references
    logging.info('loads reference list from {:} ...'.format(selected_IDs_references_path))
    selected_IDs_references = json.loads(open(selected_IDs_references_path).read())

    ## ID_subjects
    # logging.info('loads subjects from {:} ...'.format(com_IDs_subjects_path))
    # com_IDs_subjects = json.loads(open(com_IDs_subjects_path).read())

    logging.info('starting to generate statistics data ...')
    # fig,axes = plt.subplots(4,1,figsize = (6,24))

    ## t1: number of papers VS. published year
    ax = axes[0]

    year_numbers  = defaultdict(int)
    
    cc_count = defaultdict(int)
    uncited_count = 0

    year_cc = defaultdict(list)

    ref_num_count = defaultdict(int)

    # subjects_list = defaultdict(list)

    for pid in selected_IDs:

        published_year = com_IDs_year[pid]
        cc = com_IDs_cc[pid]


        year_numbers[published_year]+=1
        if cc>0:
            cc_count[cc]+=1
        else:
            uncited_count+=1


        year_cc[year].append(cc)

        ref_num = len(selected_IDs_references[pid])
        ref_num_count[ref_num]+=1


    open('data/statistics/year_numbers.json','w').write(json.dumps(year_numbers))
    open('data/statistics/cc_count.json','w').write(json.dumps(cc_count))
    open('data/statistics/year_cc.json','w').write(json.dumps(year_cc))
    open('data/statistics/ref_num_count','w').write(json.dumps(ref_num_count))

    # xs = []
    # ys = []

    # for year in sorted([int(year) for year in year_numbers.keys()]):

    #     xs.append(year)
    #     ys.append(year_numbers[str(year)])


    # ax.plot(xs,ys,label='number of papers')
    # ax.set_xlabel('published year')
    # ax.set_ylabel('number of papers')
    # ax.legend()

    # ## t2: number of papers VS. number of citations
    # ax1 = axes[1]


    # xs = []
    # ys = []

    # for 

if __name__ == '__main__':

    selected_IDs_path = 'data/selected_IDs_from_physics.txt'
    com_IDs_year_path = 'data/com_ids_year.json'
    com_IDs_cc_path = 'data/com_ids_cc.json'
    selected_IDs_references_path ='data/selected_IDs_references.json'
    com_IDs_subjects_path = 'data/com_ids_subjects.json'
    plot_statistics(selected_IDs_path,com_IDs_year_path,com_IDs_cc_path,selected_IDs_references_path,com_IDs_subjects_path)














