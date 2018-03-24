#     filtering data from web of science through following steps"
#     1. from wos_subjects filter out IDs of specified field as selected_IDs ====》 12,295,793 unique 5,679,611 
python wos_data_filtering.py t1 physics

#     2. from wos_references get reference list of these selected_IDs and get list of cited papers as cited_IDs  5,127,374/5,679,611， 25,416,227
#     3. combine selected_IDs and cited_IDs and get set COM_IDs ===> 27,239,210
#     4. use COM_IDs to stats the citation count of each paper from wos_references and saved as com_ids_cc.json {(id:number of cc)}, cc = citation count ===>25,776,340 have citations
#     5. use COM_IDs to get pubyear from wos_summray saved as com_ids_year.json {(id:pubyear)} ===>11,202,957
#     6. use COM_IDs to get subjects from wos_subjects saved as com_ids_subjects.json {id:[list of subjects]}
