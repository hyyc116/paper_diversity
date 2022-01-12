#coding:utf-8

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



if __name__ == "__main__":
    filter_4_star_journal()