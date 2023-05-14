import sqlite3
from xml.etree import ElementTree
import pandas as pd


def read_xml_file(file_path):
    xml = ElementTree.parse(file_path)
    root = xml.getroot()

    for element in root.iter():
        #print(element.tag)
        

#read_xml_file("bd/drugbank.xml")


def read_sql_file(file_path):
    con = sqlite3.connect(file_path)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    #print(cursor.description)
    cursor.execute("SELECT * FROM phenotype_annotation")
    rows = cursor.fetchone()
    names = rows.keys()
    #print(names)
    
    names = []
    for row in rows:
        if (row[0] not in names):
            names.append(row[0])
    #print(names)
    #print(len(names))

    con.close() 


#read_sql_file("bd/hpo_annotations.sqlite")


def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    #print(df["CUI"])

#read_csv_file("bd/omim_onto.csv")


def read_keg_file(file_path):
    df = pd.read_csv(file_path, delimiter="\t", header=None, comment="#")
    #print(df.shape)

#read_keg_file("bd/br08303.keg")


def read_tsv_file(file_path):
    df = pd.read_table(file_path, sep='\t')
    #print(df.shape)
    #print(df)

#read_tsv_file("bd/chemical.sources.v5.0.tsv")


def read_tsv_file_line(file_path):
    cpt = 0
    cap = 40
    for row in open(file_path, "r"):
        if cpt >= cap:
            break
        #print(row)
        cpt += 1
    #print(cpt)

#read_tsv_file_line("bd/chemical.sources.v5.0.tsv")


def read_txt_file(file_path):

    import os
    from whoosh import index
    from whoosh.fields import Schema, TEXT
    from whoosh.analysis import SimpleAnalyzer

    # Définir un schéma pour les documents
    schema = Schema(title=TEXT(stored=True), content=TEXT(analyzer=SimpleAnalyzer()))

    # Créer un nouvel index ou ouvrir un index existant
    if not os.path.exists("myindexdir"):
        os.mkdir("myindexdir")
        ix = index.create_in("myindexdir", schema)
    else:
        ix = index.open_dir("myindexdir")

    # Ajouter des documents à l'index
    writer = ix.writer()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            title, content = line.strip().split("\n\n")
            writer.add_document(title=title, content=content)
    writer.commit()



read_txt_file("bd/omim.txt")

