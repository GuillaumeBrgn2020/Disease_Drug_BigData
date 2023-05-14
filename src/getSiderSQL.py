import sqlite3


def read_sql_file(file_path):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM phenotype_annotation")
    rows = cursor.fetchone()
    names = rows.keys()
    
    names = []
    for row in rows:
        if (row[0] not in names):
            names.append(row[0])

    con.close() 


def connexion_sql(file_path):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()
    return con, cursor


def get_cui_from_meddra_all_se(cursor):
    cursor.execute("SELECT cui FROM meddra_all_se")
    rows = cursor.fetchall()
    cui_l = []
    for row in rows:
        cui_l.append(row[0])
    return cui_l


def get_cui_from_meddra_all_indications(cursor):
    cursor.execute("SELECT cui FROM meddra_all_indications")
    rows = cursor.fetchall()
    cui_l = []
    for row in rows:
        cui_l.append(row[0])
    return cui_l

def get_side_effect_name(cursor):
    cursor.execute("SELECT side_effect_name FROM meddra_all_se")
    rows = cursor.fetchall()
    side_effect_l = []
    for row in rows:
        side_effect_l.append(row[0])
    return side_effect_l

def get_stitch_id(cursor):
    cursor.execute("SELECT stitch_compound_id FROM meddra_all_indications")
    rows = cursor.fetchall()
    side_effect_l = []
    for row in rows:
        side_effect_l.append(row[0])
    return side_effect_l


def get_concept_name(cursor):
    cursor.execute("SELECT concept_name FROM meddra_all_indications")
    rows = cursor.fetchall()
    side_effect_l = []
    for row in rows:
        side_effect_l.append(row[0])
    return side_effect_l

def get_concept_name_by_cui(cursor, cui):
    cursor.execute("SELECT concept_name FROM meddra_all_indications WHERE cui = ?", (cui,))
    rows = cursor.fetchall()
    side_effect_l = []
    for row in rows:
        side_effect_l.append(row[0])
    res = None 
    try : 
        res = side_effect_l[0]
    except IndexError:
        pass
    return res

def get_side_effect_name_by_cui(cursor, cui):
    cursor.execute("SELECT concept_name FROM meddra_all_se WHERE cui = ?", (cui,))
    rows = cursor.fetchall()
    side_effect_l = []
    for row in rows:
        side_effect_l.append(row[0])
    res = None 
    try : 
        res = side_effect_l[0]
    except IndexError:
        pass
    return res

def get_cui_by_concept_name(cursor, concept_name):
    cursor.execute("SELECT cui FROM meddra_all_indications WHERE concept_name = ?", (concept_name,))
    rows = cursor.fetchall()
    cui_l = []
    for row in rows:
        cui_l.append(row[0])
    res = None 
    try : 
        res = cui_l[0]
    except IndexError:
        pass
    return res


def get_id_stitch_by_CUI_ind(cursor, cui):
    cursor.execute("SELECT stitch_compound_id FROM meddra_all_indications WHERE cui = ?", (cui,))
    rows = cursor.fetchall()
    cui_l = []
    for row in rows:
        cui_l.append(row[0])
    return cui_l


def get_id_stitch_by_CUI_se(cursor, cui):
    cursor.execute("SELECT stitch_compound_id1 FROM meddra_all_se WHERE cui = ?", (cui,))
    rows1 = cursor.fetchall()
    cursor.execute("SELECT stitch_compound_id2 FROM meddra_all_se WHERE cui = ?", (cui,))
    rows2 = cursor.fetchall()
    cui_l = []
    for row in rows1:
        cui_l.append(row[0])
    for row in rows2:
        cui_l.append(row[0])
    return cui_l


#res1 = get_id_stitch_by_CUI_ind(connexion_sql("bd/sider.db")[1], "C0022661")
#print(res1)
#print(len(res1))
#res2 = get_id_stitch_by_CUI_se(connexion_sql("bd/sider.db")[1], "C0022661")
#print(res2)
#print(len(res2))

#print(res1==res2)
