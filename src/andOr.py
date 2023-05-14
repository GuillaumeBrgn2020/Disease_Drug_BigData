from request import *

def fetch_results_and(symptoms_list):
  results_disease, results_treatment, results_side_effect = handle_request_single_symptom(symptoms_list[0])
  
  while len(symptoms_list) > 1:
    results_disease, results_treatment, results_side_effect = [list(set(lst) & set(other_lst)) for lst, other_lst in zip((results_disease, results_treatment, results_side_effect), handle_request_single_symptom(symptoms_list[1]))]
    symptoms_list = symptoms_list[1:]
  print("Diseases :\n")
  print(results_disease)
  print("\n\nTreatments :\n")
  print(results_treatment)
  print("\n\nSide effects :\n")
  print(results_side_effect)
  return results_disease, results_treatment, results_side_effect


def fetch_results_or(symptoms_list):
  results_disease, results_treatment, results_side_effect = handle_request_single_symptom(symptoms_list[0])
  
  while len(symptoms_list) > 1:
    results_disease, results_treatment, results_side_effect = [list(set(lst + ajout_lst)) for lst, ajout_lst in zip((results_disease, results_treatment, results_side_effect), handle_request_single_symptom(symptoms_list[1]))]
    symptoms_list = symptoms_list[1:]
  
  print("Diseases :\n")
  print(results_disease)
  print("\n\nTreatments :\n")
  print(results_treatment)
  print("\n\nSide effects :\n")
  print(results_side_effect)
  return results_disease, results_treatment, results_side_effect