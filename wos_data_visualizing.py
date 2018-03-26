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

def statistics_data(selected_IDs_path,com_IDs_year_path,com_IDs_cc_path,selected_IDs_references_path,com_IDs_subjects_path):
    ## selected Ids
    logging.info("loads selected IDs from {:} ...".format(selected_IDs_path))
    selected_IDs = list(set([line.strip() for line in open(selected_IDs_path)]))

    ## ID_year
    logging.info('loads year dict from {:} ...'.format(com_IDs_year_path))
    com_IDs_year = json.loads(open(com_IDs_year_path).read())

    ## ID_cc
    logging.info('loads citation count from {:} ...'.format(com_IDs_cc_path))
    com_IDs_cc = json.loads(open(com_IDs_cc_path).read())

    ## ID_references
    logging.info('loads reference list from {:} ...'.format(selected_IDs_references_path))
    # selected_IDs_references = json.loads(open(selected_IDs_references_path).read())
    selected_IDs_references= defaultdict(list)
    for line in open(selected_IDs_references_path):
        line = line.strip()
        pid,ref_id = line.split("\t")
        selected_IDs_references[pid].append(ref_id)

    ## ID_subjects
    # logging.info('loads subjects from {:} ...'.format(com_IDs_subjects_path))
    # com_IDs_subjects = json.loads(open(com_IDs_subjects_path).read())

    logging.info('starting to generate statistics data ...')
    # fig,axes = plt.subplots(4,1,figsize = (6,24))

    # ax = axes[0]
    uncited_count = 0
    used_paper_count = 0


    year_numbers  = defaultdict(int)
    
    cc_count = defaultdict(int)

    year_cc = defaultdict(list)

    ref_num_count = defaultdict(int)

    year_differences = defaultdict(list)

    # subjects_list = defaultdict(list)
    progress = 0
    total_num = len(selected_IDs)
    for pid in selected_IDs:

        progress+=1
        if progress%100000:
            logging.info('processing progress {:}/{:} ...'.format(progress,total_num))

        published_year = com_IDs_year.get(pid,-1)
        cc = com_IDs_cc.get(pid,0)
        refs = selected_IDs_references.get(pid,[])

        if published_year==-1 or len(refs)==0:
            continue

        used_paper_count+=1

        year_numbers[published_year]+=1
        if cc>0:
            cc_count[cc]+=1
        else:
            uncited_count+=1

        year_cc[published_year].append(cc)

        ref_num = len(refs)
        ref_num_count[ref_num]+=1

        for ref in refs:
            ref_year = com_IDs_year.get(ref,-1)
            if ref_year!=-1:
                year_differences[pid].append(int(published_year)-int(ref_year))

    logging.info('data saved to directory data/statistics ..')
    open('data/statistics/year_numbers.json','w').write(json.dumps(year_numbers))
    open('data/statistics/cc_count.json','w').write(json.dumps(cc_count))
    open('data/statistics/year_cc.json','w').write(json.dumps(year_cc))
    open('data/statistics/ref_num_count.json','w').write(json.dumps(ref_num_count))
    open('data/statistics/year_differences.json','w').write(json.dumps(year_differences))



def plot_statistics(cc_count_path,year_numbers_path,year_cc_path,ref_num_count_path):

    fig,axes = plt.subplots(3,1,figsize=(6,12))
    logging.info('Plotting number of papers VS. number of citation ...')
    ### number of papers VS. number of citation
    ax1 = axes[0]
    cc_count = json.loads(open(cc_count_path).read())

    xs = []
    ys = []

    for cc in sorted([int(c) for c in cc_count.keys()]):
        xs.append(cc)
        ys.append(cc_count[str(cc)])

    ax1.plot(xs,ys,'o',fillstyle='none',c=color_sequence[0], linewidth=2)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('number of citations')
    ax1.set_ylabel('number of papers')
    ax1.set_xlim(0.1,10**5)
    ax1.set_ylim(0.1,10**6)

    ## t1: number of papers VS. published year
    ax2 = axes[1]
    logging.info('Plotting number of papers VS. published year ...')

    year_numbers = json.loads(open(year_numbers_path).read())
    xs = []
    ys = []

    for year in sorted([int(year) for year in year_numbers.keys()]):

        xs.append(year)
        ys.append(year_numbers[str(year)])

    l2 = ax2.plot(xs,ys,label='number of papers',c=color_sequence[0], linewidth=2)
    ax2.set_xlabel('published year')
    ax2.set_ylabel('number of papers')
    ax2.set_yscale('log')

    ## average citation count VS. published year
    ax3 = ax2.twinx()

    xs = []
    ys = []

    year_cc = json.loads(open(year_cc_path).read())

    for year in sorted([int(y) for y in year_cc.keys()]):
        xs.append(year)
        ys.append(np.mean(year_cc[str(year)]))

    l3 = ax3.plot(xs,ys,label='average citation',c='r', linewidth=2)
    ax3.set_ylabel('average citation count')
    ax3.set_yscale('log')

    ls = l2+l3
    labels = [l.get_label() for l in ls]

    ax2.legend(ls,labels)

    # ## t2: number of papers VS. number of references
    ax4 = axes[2]
    logging.info('Plotting number of papers VS. number of references ...')

    ref_num_count = json.loads(open(ref_num_count_path).read())

    xs = []
    ys = []

    for ref_num in sorted([int(rn) for rn in ref_num_count.keys()]):
        xs.append(ref_num)
        ys.append(ref_num_count[str(ref_num)])

    ax4.plot(xs,ys,c=color_sequence[0], linewidth=2)
    ax4.set_xlabel('number of references')
    ax4.set_ylabel('number of papers')
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.set_xlim(0.1,10**5)
    ax4.set_ylim(0.1,10**6)


    plt.tight_layout()
    plt.savefig('pdf/wos_statistics.pdf',dpi=200)
    logging.info('saved to pdf/wos_statistics.pdf ...')



def stats():
    selected_IDs_path = 'data/selected_IDs_from_physics.txt'
    com_IDs_year_path = 'data/com_ids_year.json'
    com_IDs_cc_path = 'data/com_ids_cc.json'
    selected_IDs_references_path ='data/selected_IDs_references.txt'
    com_IDs_subjects_path = 'data/com_ids_subjects.json'
    statistics_data(selected_IDs_path,com_IDs_year_path,com_IDs_cc_path,selected_IDs_references_path,com_IDs_subjects_path)


def plot_stats():
    year_numbers_path = 'data/statistics/year_numbers.json'
    cc_count_path = 'data/statistics/cc_count.json'
    year_cc_path = 'data/statistics/year_cc.json'
    ref_num_count_path = 'data/statistics/ref_num_count.json'
    plot_statistics(cc_count_path,year_numbers_path,year_cc_path,ref_num_count_path)

if __name__ == '__main__':
    # stats()
    plot_stats()














