#Récupération de l'ID et du CUI pour chaque ligne du fichier

import csv

#get_CUI_by_ID_onim_onto_CSV = lambda id: get_CUI_onim_onto_CSV()[get_ID_onim_onto_CSV().index(id)]

#get_ID_by_CUI_onim_onto_CSV = lambda cui: get_ID_onim_onto_CSV()[get_CUI_onim_onto_CSV().index(cui)]

def get_ID_onim_onto_CSV ():
  """Gets all the disease id in the omim_onto.csv database

  Returns:
      id_list: list of all the disease id in the omim_onto.csv database
  """
  
  id_list = []
  
  with open("bd/omim_onto.csv", newline = '') as fichier:
        file_reader = csv.reader(fichier)
        
        for row in file_reader:
          split_id = row[0].split('/')
          length = len(split_id)
          if split_id[length-2] == "OMIM":
            id_list.append(split_id[length-1])
          
  return id_list


def get_CUI_onim_onto_CSV ():
  """Gets all the disease CUI in the omim_onto.csv database

  Returns:
      cui_list: list of all the disease CUI in the omim_onto.csv database
  """
  
  cui_list = []
  
  with open("bd/omim_onto.csv", newline = '') as fichier:
        file_reader = csv.reader(fichier, quotechar = '"', delimiter = ',')
        
        for row in file_reader:
          cui_list.append(row[5])
          
  return cui_list

def get_CUI_by_ID_onim_onto_CSV(id):
  IDs = get_ID_onim_onto_CSV()
  if id in IDs:
    return [get_CUI_onim_onto_CSV()[IDs.index(id)]]
  return []

def get_ID_by_CUI_onim_onto_CSV(cui):
  return get_ID_onim_onto_CSV()[get_CUI_onim_onto_CSV().index(cui)]

#print(get_ID_onim_onto_CSV())
