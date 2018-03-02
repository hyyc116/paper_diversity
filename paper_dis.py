#coding:utf-8
'''
    
    select papers of a specific domain from mag.
    
    Input: All papers of  MAG

    Output: papers of specific papers

'''
from basic_config import *

def plot_distributions(paper_attrs_path,ref_paper_attrs_path):

    logging.info('paper attrs ...')
    paper_attrs = json.loads(open(paper_attrs_path).read())
    papers_ids = [pid for pid in paper_attrs.keys()]
    logging.info('ref paper attrs ...')
    progress = 0
    ref_paper_atrrs = {}
    for line in open(ref_paper_attrs_path):
        logging.info('progress {:} ...'.format(progress))
        progress+=1
        line = line.strip()
        obj = json.loads(line)
        ref_paper_atrrs.update(obj)

    year_paper_count = defaultdict(int)
    citation_dis = defaultdict(int)
    refs_dis = defaultdict(int)
    year_citation_age_dis = defaultdict(list)
    logging.info('Generate data ...')
    progress = 0
    length = len(paper_attrs.keys())
    for pid in papers_ids:
        progress+=1
        if progress%10000==1:
            logging.info('Generate progress {:}/{:} ...'.format(progress,length))
        year = paper_attrs[pid]['year']
        refs = paper_attrs[pid]['refs']
        n_citation = paper_attrs[pid]['n_citation']
        # fos = paper_attrs[pid]['fos']
        if year!=-1:
            year_paper_count[year]+=1
        citation_dis[n_citation]+=1
        refs_dis[len(refs)]+=1

        ref_years = []
        for ref in refs:
            pObj = ref_paper_atrrs.get(ref,-1)
            if pObj!=-1:
                ref_years.append(pObj.get('year',-1))
        if year!=-1:
            citation_age = np.max(ref_years)-year
            year_citation_age_dis[year].append(citation_age)


    fig,axes = plt.subplots(1,4,figsize=(20,5))
    logging.info('Plotting distribution over year ...')
    ## plot paper distribution over years
    xs = []
    ys = []
    for year in sorted(year_paper_count.keys()):
        xs.append(year)
        ys.append(year_paper_count[year])

    ax = axes[0]
    ax.plot(xs,ys)
    ax.set_title('Paper distribution over publication year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of papers')
    ax.set_yscale('log')
    ax.set_xlim(1825,2020)

    ## plot citation distribution
    logging.info('Plotting citation count distribution ... ')
    xs = []
    ys = []
    for citation in sorted(citation_dis.keys()):
        xs.append(citation)
        ys.append(citation_dis[citation])

    ax = axes[1]
    ax.plot(xs,ys,'o',fillstyle=None)
    ax.set_xlabel('Citation Count')
    ax.set_ylabel('Number of Papers')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title('Citation Count Distribution')

    logging.info('Plotting reference number distribution ... ')
    ## reference num distribution
    xs = []
    ys = []
    for ref in sorted(refs_dis.keys()):
        xs.append(ref)
        ys.append(refs_dis[ref])

    ax = axes[2]
    ax.plot(xs,ys,'o',fillstyle=None)
    ax.set_xlabel('Reference Number')
    ax.set_ylabel('Number of Papers')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title('Reference Number Distribution')
    
    logging.info('Plotting citation age distribution ... ')
    ## citation age over year
    xs = []
    ys = []
    for year in sorted(year_citation_age_dis.keys()):
        xs.append(year)
        ys.append(np.mean(year_citation_age_dis[year]))

    ax = axes[3]
    ax.plot(xs,ys)
    ax.set_xlabel('Year')
    ax.set_ylabel('Average citation age')
    ax.set_title('Citation Age distribution Over Publication Year')

    plt.tight_layout()
    plt.savefig('figs/paper_distribution.pdf',dpi=200)
    logging.info('figures saved to figs/paper_distribution.pdf.')





if __name__ == '__main__':
    plot_distributions(sys.argv[1],sys.argv[2])







