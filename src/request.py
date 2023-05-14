from getStitchATC import get_ATC_id, search_index_tsv
from hpoOBO import *
from getHPOAnnotationsSQLite import *
from getOmimTXT import *
from drugBankXML import *
from atcKEG import *
from getOnimCSV import *
from getSiderSQL import *

def handle_request_single_symptom(symptom):
    diseases = []
    drugs_indication = []
    drugs_toxicity = []
    
    # 1. Get the symptom's synonyms
    synonyms = get_synonyms(symptom) # from hpoOBO
    
    ## Going through all the synonyms
    for (sign_id, syn) in synonyms:
        
        # 2. Get diseases : sign_id -> idOmim
        idOmim_list = get_disease_id_by_sign_id(sign_id) # from getHPOAnnotationSQLite
        
        list_cui = []
        
        ## Going through all the idOmims
        for idOmim in idOmim_list:
            
            ## Get diseases names : idOmim -> *FIELD* TI
            diseases_names = search_index_txt(idOmim, syn) # from getOmimTXT
            
            ## Adding all the diseases' names to the return value
            for name in diseases_names:
                diseases.append(name)
            
            ## Searching for : sign_id -> CUI
            IDs = get_ID_onim_onto_CSV() # from getOmimCSV
            CUIs = get_CUI_onim_onto_CSV() # from getOmimCSV
            if id in IDs:
                list_cui.append(CUIs[IDs.index(id)])

        # 3. Get drugs (indication and toxicity)

        # 3.1
        ## Searching for (idDrug, atc) matching syn as indication or toxicity in the xml : idDrug -> idStitch
        ids_drug_indication, ids_drug_toxicity = search_index_xml(syn) # from drugBankXML

        ## Building the dictionary of {idStitch : labels} ie {atc : labels} (?)
        dico_idStitch_label = get_atc_stitch_ids_labels_dico() # from atcKEG
        
        ## Get drug labels from atc keg : idStitch -> label
        
        ### For synonym as indication
        for drug in ids_drug_indication:
            if drug[1] != None:
                for atc_code in drug[1]:
                    if atc_code in dico_idStitch_label.keys():
                        drugs_indication.append(dico_idStitch_label[atc_code])

        ### For synonym as toxicity
        for drug in ids_drug_toxicity:
            if drug[1] != None:
                for atc_code in drug[1]:
                    if atc_code in dico_idStitch_label.keys():
                        drugs_toxicity.append(dico_idStitch_label[atc_code])

        # 3.2
        
        ## Get : CUI -> idStitch
        list_id_stitch_from_sider_ind = []
        list_id_stitch_from_sider_se = []
        for cui in list_cui:
            IND = get_id_stitch_by_CUI_ind(connexion_sql("bd/sider.db")[1], cui)  # from getSiderSQL
            for ind in IND:
                list_id_stitch_from_sider_ind.append(ind)
            
            SE = get_id_stitch_by_CUI_se(connexion_sql("bd/sider.db")[1], cui)# from getSiderSQL
            for se in SE:
                list_id_stitch_from_sider_se.append(se)
        
        ## Get atc from idStitch for indications : idStitch -> atc (CID)
        ### For synonym as indication
        list_atc_from_id_stitch_ind = []
        for idStitch in list_id_stitch_from_sider_ind:
            list_atc = search_index_tsv(idStitch) # from getStitchATC
            for atc in list_atc:
                list_atc_from_id_stitch_ind.append(atc)
                
        ### For synonym as toxicity
        list_atc_from_id_stitch_se = []
        for idStitch in list_id_stitch_from_sider_se:
            list_atc = search_index_tsv(idStitch) # from getStitchATC
            for atc in list_atc:
                list_atc_from_id_stitch_se.append(atc)
        
        ## Get drug names : atc (CID) -> label
        
        ### For synonym as indication
        for atc in list_atc_from_id_stitch_ind :
            if atc in dico_idStitch_label.keys():
                drugs_indication.append(dico_idStitch_label[atc])
        
        ### For synonym as toxicity
        for atc in list_atc_from_id_stitch_se :
            if atc in dico_idStitch_label.keys():
                drugs_toxicity.append(dico_idStitch_label[atc])

    return diseases, drugs_indication, drugs_toxicity

#print(get_synonyms("Syndactyly"))
#print(handle_request_single_symptom("Headache"))