from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
import requests
from request import *
from andOr import *

import getSiderSQL as sider


def capitalize_response(words):
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)

def capitalize_inputs(words):
    capitalized_words = [word.capitalize() for word in words]
    return capitalized_words


# Main window
window = Tk()
window.geometry("800x650")
window.title("GMD application")
window.configure(bg="#282828")



def get_result():

    # Request
    user_input = text_entry.get("1.0", END)
    user_input = user_input.rstrip()
    list_args = user_input.split(";")
    list_args = capitalize_inputs(list_args)

    # Mode
    mode = mode_var.get()


    # AND request
    if(mode == "AND") and len(list_args) > 1:
        response_disease, response_treatment, response_side_effect = fetch_results_and(list_args)

    # OR request
    if(mode == "OR") and len(list_args) > 1:
        response_disease, response_treatment, response_side_effect = fetch_results_or(list_args)


    
    # ## Diseases
    # response_disease = sider.get_cui_by_concept_name(sider.connexion_sql("bd/sider.db")[1], list_args[0])

    # ## Side effects
    # response_side_effect = sider.get_cui_by_concept_name(sider.connexion_sql("bd/sider.db")[1], list_args[0])

    # ## Treatment
    # response_treatment = sider.get_cui_by_concept_name(sider.connexion_sql("bd/sider.db")[1], list_args[0])
    
    # Single symptom request
    if (len(list_args) == 1):
        response_disease, response_treatment, response_side_effect = handle_request_single_symptom(list_args[0])
    
    if len(response_disease) > 2:
        response_disease = response_disease[:2]
    if len(response_treatment) > 2:
        response_treatment = response_treatment[:2]
    if len(response_side_effect) > 2:
        response_side_effect = response_side_effect[:2]

    # Print response
    output_diseases_entry.config(text=response_disease)
    output_side_effect_entry.config(text=response_side_effect)
    output_treatment_entry.config(text=response_treatment)




# Widgets
title_label = Label(window, text="DataBase treatment", font=("Arial", 28), height=3, bg="#282828", fg="#ffffff")
text_entry = Text(window, wrap='word', height=2, width=70, bg="#808080", fg="#ffffff")
text_entry.configure(font=("Arial", 12))
output_diseases_label = Label(window, text="Diseases with these symptoms:", font=("Arial", 11), bg="#282828", fg="#ffffff")
output_diseases_entry = Label(window, width=95, bg="#282828", fg="#ffffff")
output_side_effect_label = Label(window, text="Drugs with these side effects:", font=("Arial", 11), bg="#282828", fg="#ffffff")
output_side_effect_entry = Label(window, width=95, bg="#282828", fg="#ffffff")
output_treatment_label = Label(window, text="Drugs to heal these symptoms:", font=("Arial", 11), bg="#282828", fg="#ffffff")
output_treatment_entry = Label(window, width=95, bg="#282828", fg="#ffffff")
submit_button = Button(window, text="Submit", command=get_result, height=3, width=10, font=("Arial", 12))

radio_frame = Frame(window, bg="#282828")
mode_var = StringVar()
mode_var.set("AND")
text_label = Label(radio_frame, text="Symptoms: (separated by ';')", font=("Arial", 15), bg="#282828", fg="#ffffff")
text_label.pack(side=LEFT)
et_radiobutton = Radiobutton(radio_frame, text="AND", variable=mode_var, value="AND")
et_radiobutton.pack(side=LEFT, padx=5, pady=5)
ou_radiobutton = Radiobutton(radio_frame, text="OR", variable=mode_var, value="OR")
ou_radiobutton.pack(side=LEFT, padx=5, pady=5)





# Put widget in window
title_label.pack()

spacer_frame = Frame(window, height=5, bg="#282828")
spacer_frame.pack()

radio_frame.pack()
text_entry.pack()

spacer_frame = Frame(window, height=20, bg="#282828")
spacer_frame.pack()

output_diseases_label.pack()
output_diseases_entry.pack()

spacer_frame = Frame(window, height=10, bg="#282828")
spacer_frame.pack()

output_side_effect_label.pack()
output_side_effect_entry.pack()

spacer_frame = Frame(window, height=10, bg="#282828")
spacer_frame.pack()

output_treatment_label.pack()
output_treatment_entry.pack()

spacer_frame = Frame(window, height=20, bg="#282828")
spacer_frame.pack()

submit_button.pack()

radio_frame.pack(fill="x", padx=50, pady=(30, 10))



style = ThemedStyle(window)
style.set_theme("black")


# Show window
window.mainloop()
