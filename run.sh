### select data
python data_selection.py select_papers /public/data/Aminer_MAG/MAG/txt/ physics

### output reference papers
python data_selection.py out_papers /public/data/Aminer_MAG/MAG/txt/ data/physics-paper-ids.txt data/physics-ref-ids.txt  physics

### citing relation
python data_selection.py citing_relation /public/data/Aminer_MAG/MAG/txt/ data/physics-paper-ids.txt

### out paper attrs
python data_selection.py export_paper_attrs data/physics-all-papers.txt data/physics-paper-ids.txt data/physics-ref-ids.txt

##### plot paper distributions
python paper_dis.py data/paper_attrs.json data/paper_citation.json

