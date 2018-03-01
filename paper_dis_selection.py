#coding:utf-8
'''
    
    select papers of a specific domain from mag.
    
    Input: All papers of  MAG

    Output: papers of specific papers

'''
from basic_config import *

def citation_distribution(papers):
    '''
        draw paper distribution over year of papers.
        draw citation distribution of papers

    '''
    year_paper_count = defaultdict(int)
    citation_dis = defaultdict(int)
    for line in open(papers):
        line = line.strip()
        pObj = json.loads(line)

        year = pObj.get('year',-1)
        if year !=-1:
            year_paper_count[year]+=1

        ## if there is no n_citation keywords, return 0
        n_citation = pObj.get('n_citation',0)
        citation_dis[n_citation]+=1


    fig,axes = plt.subplots(2,1,figsize=(10,10))
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

    plt.tight_layout()
    plt.savefig('figs/paper_distribution.pdf',dpi=200)




if __name__ == '__main__':
    citation_distribution(sys.argv[1])







