### select data
python data_selection.py select_papers /public/data/Aminer_MAG/MAG/txt/ physics

### output reference papers
python data_selection.py out_ref_papers /public/data/Aminer_MAG/MAG/txt/ data/physics-ref-ids.txt  physics

### citing relation
python data_selection.py citing_relation /public/data/Aminer_MAG/MAG/txt/ data/physics-paper-ids.txt

### out paper attrs
python data_selection.py out_paper_attrs data/physics-papers.txt

### out reference attrs
python data_selection.py out_ref_attrs data/physics-ref-papers.txt


##### plot paper distributions
python paper_dis.py data/paper_attrs.json data/paper_citation.json

