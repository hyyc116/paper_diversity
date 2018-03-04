### select data
python data_selection.py select_papers /public/data/Aminer_MAG/MAG/txt/ physics
#2018-03-04 11:22:58,376 : INFO : Number of paper in this field:4,129,888
#2018-03-04 11:24:10,741 : INFO : Number of references paper in this field:11,257,060

### output reference papers
python data_selection.py out_papers /public/data/Aminer_MAG/MAG/txt/ data/physics-paper-ids.txt data/physics-ref-ids.txt  physics
##  INFO : Number of reference papers in this field:12,387,827

### citing relation
python data_selection.py citing_relation /public/data/Aminer_MAG/MAG/txt/ data/physics-paper-ids.txt

### out paper attrs
python data_selection.py export_paper_attrs data/physics-all-papers.txt data/physics-paper-ids.txt data/physics-ref-ids.txt

##### plot paper distributions
python paper_dis.py data/paper_attrs.json data/paper_citation.json

