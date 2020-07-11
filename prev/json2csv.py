#coding:utf-8

import json
from collections import defaultdict

def json2csv():

    data = json.loads(open('data/subject_sim.json').read())

    s1_s2_sim = defaultdict(dict)
    for key in data.keys():

        s1,s2 = key.split('\t')

        s1_s2_sim[s1][s2] = data[key]

    lines = ['subject1, subject2, similarity']
    for s1 in sorted(s1_s2_sim.keys()):

        for s2 in sorted(s1_s2_sim[s1].keys(),key=lambda x:s1_s2_sim[s1][x],reverse=True):

            sim = s1_s2_sim[s1][s2]
            line = '{:},{:},{:.10f}'.format(s1,s2,sim)


            lines.append(line)

    open('data/subject_similarity.csv','w').write('\n'.join(lines))

if __name__ == '__main__':
    json2csv()















