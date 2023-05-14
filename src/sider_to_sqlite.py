import pandas as pd
import sqlite3
from sqlite3 import Error


meddra = pd.read_table("bd/meddra.tsv", sep='\t', names=["cui", "concept_type", "meddra_id", "label"])
meddra_all_ind = pd.read_table("bd/meddra_all_indications.tsv", sep='\t', names=["stitch_compound_id", "cui", "method_of_detection", "concept_name", "meddra_concept_type", "cui_of_meddra_term", "meddra_concept_name"])
meddra_all_se = pd.read_table("bd/meddra_all_se.tsv", sep='\t', names=["stitch_compound_id1", "stitch_compound_id2", "cui", "meddra_concept_type", "cui_of_meddra_term", "side_effect_name"])


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

create_connection("sider.db")
con = sqlite3.connect("sider.db")
cursor = con.cursor()

#cursor.execute("CREATE TABLE meddra_all_indications (idStich INT NOT NULL, CUI VARCHAR NOT NULL, indication VARCHAR NOT NULL)")

print("meddra_all_indications table is created....")

#cursor.execute("CREATE TABLE meddra_all_se (idStitch1 INT NOT NULL, idStitch2 INT NOT NULL, CUI VARCHAR NOT NULL, sideEffect VARCHAR NOT NULL)")

print("meddra_all_se table is created....")

sql = "INSERT INTO meddra_all_indications VALUES (?,?,?)"
df_ind = pd.DataFrame(meddra_all_ind, columns=["stitch_compound_id", "cui", "concept_name"])
print(df_ind)
df_ind.to_sql(con=con, name="meddra_all_indications")

sql = "INSERT INTO meddra_se VALUES (?,?,?,?)"
df_se = pd.DataFrame(meddra_all_se, columns=["stitch_compound_id1", "stitch_compound_id2", "cui", "side_effect_name"])
print(df_se)
df_se.to_sql(con=con, name="meddra_all_se")


cursor.execute("ALTER TABLE meddra_all_indications DROP COLUMN index")
cursor.execute("ALTER TABLE meddra_all_se DROP COLUMN index")

con.commit()

con.close()
