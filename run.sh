### select data
python data_selection.py select_papers /public/data/Aminer_MAG/MAG/txt/ physics

### output reference papers
python data_selection.py out_ref_papers /public/data/Aminer_MAG/MAG/txt/ data/physics-ref-ids.txt  physics

### out paper attrs
python data_selection.py out_paper_attrs data/physics-papers.txt

### out reference attrs
python out_ref_attrs.py out_paper_attrs data/physics-ref-papers.txt
