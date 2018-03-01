#coding:utf-8
'''
    
    select papers of a specific domain from mag.
    
    Input: All papers of  MAG

    Output: papers of specific papers

'''
from basic_config import *

def gen_paper_attrs(papers,ref_papers):
    '''
        draw paper distribution over year of papers.
        draw citation distribution of papers

    '''
    
    pid_attrs={}
    progress=1
    for line in open(papers):

        progress+=1
        if progress%100000==1:
            logging.info('paper progress {:} ...'.format(progress))


        line = line.strip()
        pObj = json.loads(line)
        pid = pObj['id']
        year = pObj.get('year',-1)
        refs =pObj.get('references',[])
        ## if there is no n_citation keywords, return 0
        n_citation = pObj.get('n_citation',0)
        ## fos
        fos = pObj.get('fos',[])
        pid_attrs[pid]['year']=year
        pid_attrs[pid]['fos']=fos
        pid_attrs[pid]['refs']=refs
        pid_attrs[pid]['n_citation']=n_citation

    ref_pid_attrs = {}
    progress=0
    for line in open(ref_papers):
        progress+=1
        if progress%100000==1:
            logging.info('ref paper progress {:} ...'.format(progress))
        line = line.strip()
        pObj = json.loads(line)
        pid = pObj['id']
        year = pObj.get('year',-1)
        refs =pObj.get('references',[])
        ## if there is no n_citation keywords, return 0
        n_citation = pObj.get('n_citation',0)
        ## fos
        fos = pObj.get('fos',[])

        ref_pid_attrs[pid]['year']=year
        ref_pid_attrs[pid]['fos']=fos
        ref_pid_attrs[pid]['refs']=refs
        ref_pid_attrs[pid]['n_citation']=n_citation

    open('data/paper_attrs.json','w').write(json.dumps(pid_attrs))
    open('data/ref_paper_attrs.json','w').write(json.dumps(ref_pid_attrs))

def plot_distributions(paper_attrs_path,ref_paper_attrs_path):

    paper_attrs = json.loads(open(paper_attrs_path).read())
    ref_paper_attrs = json.loads(open(ref_paper_attrs_path).read())

    year_paper_count = defaultdict(int)
    citation_dis = defaultdict(int)
    refs_dis = defaultdict(int)
    citation_age_dis = defaultdict(int)

    for pid in paper_attrs.keys():
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
            pObj = ref_paper_attrs.get(ref,-1)
            if pObj!=-1:
                ref_years.append(pObj.get('year',-1))
        if year!=-1:
            citation_age = np.max(ref_years)-year
            citation_age_dis[citation_age]+=1


    fig,axes = plt.subplots(1,4,figsize=(20,5))
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
    ax.set_xlim(1825,2017)

    ## plot citation distribution

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

    ## reference num distribution
    xs = []
    ys = []
    for ref in sorted(refs_dis.keys()):
        xs.append(ref)
        ys.append(refs_dis[ref])

    ax = axes[2]
    ax.plot(xs,ys,'o',fillstyle=None)
    ax.set_xlabel('Citation Count')
    ax.set_ylabel('Number of Papers')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ## citation age distribution



    plt.tight_layout()
    plt.savefig('figs/paper_distribution.pdf',dpi=200)





if __name__ == '__main__':
    gen_paper_attrs(sys.argv[1],sys.argv[2])
    # citation_distribution(sys.argv[1])







