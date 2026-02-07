import tkinter as tk
from tkinter import messagebox
MIN_SYMPTOMS = 2
MAX_SYMPTOMS = 6

def diagnose(symptoms: dict) -> str:
    
    fever = bool(symptoms.get("fever"))
    cough = bool(symptoms.get("cough"))
    chest_pain = bool(symptoms.get("chest_pain"))
    breathless = bool(symptoms.get("breathless"))
    nose = bool(symptoms.get("nose"))
    runny = (symptoms.get("runny") or "").strip().lower()
    cough_type = (symptoms.get("cough_type") or "").strip().lower()
    sore = bool(symptoms.get("sore"))
    sneezing = bool(symptoms.get("sneezing"))
    fatigue = bool(symptoms.get("fatigue"))
    body_ache = bool(symptoms.get("body_ache"))
    headache = bool(symptoms.get("headache"))
    dry_mouth = bool(symptoms.get("dry_mouth"))
    dizziness = bool(symptoms.get("dizziness"))
    vomiting = bool(symptoms.get("vomiting"))
    diarrhea = bool(symptoms.get("diarrhea"))

    # ---------- Fever branch ----------
    if fever:
        # Specific pneumonia/cardiac checks FIRST
        if cough and chest_pain and breathless and nose and runny == "coloured":
            return "Pneumonia pattern"
        if cough and chest_pain and breathless:
            return "Viral bronchitis / flu-like illness"

        # General fever + cough + sore throat
        if cough and sore:
            return "Viral upper respiratory infection (common cold/flu-like)"
        if cough and nose and sneezing:
            return "Common cold / Viral upper respiratory infection"
        if cough and not chest_pain and not breathless:
            if cough_type == "wet" and fatigue:
                return "Respiratory infection"
            else:
                return "Early viral infection / mild respiratory illness"
        if sore:
            return "Early throat inflammation / viral fever pattern"
        if headache and fatigue:
            if dry_mouth or dizziness:
                return "Dehydration"
            else:
                return "Mild viral illness"
        if fatigue and body_ache:
            return "Influenza / flu-like illness"
        if headache and body_ache:
            return "Viral fever / flu onset"
        if body_ache:
            return "Viral fever"
        if diarrhea:
            return "Viral gastrointestinal illness"
        return "Fever of unclear origin"

    # ---------- Non-fever branch ----------
    else:
        if cough and sore:
            return "Throat irritation / mild upper respiratory infection"
        if cough_type == "dry" and runny == "clear" and sneezing:
            return "Allergy pattern (nasal)"
        if cough and sneezing and runny == "clear":
            return "Nasal irritation / early allergy"
        if sneezing and cough and fatigue and nose:
            return "RSV (Respiratory Syncytial Virus)"
        if breathless and cough and not chest_pain:
            return "Bronchial irritation / possible bronchitis"
        if runny == "coloured" and fatigue and cough:
            return "Upper respiratory irritation"
        if diarrhea and vomiting:
            if fatigue:
                return "Food poisoning"
            else:
                return "Gastrointestinal upset (stomach infection/food irritation)"
        if dry_mouth and dizziness and fatigue:
            return "Dehydration"
        if dizziness and headache:
            return "Low energy / dehydration"
        # Cardiac flow sentinel if GUI needs to ask follow-ups
        if chest_pain and breathless and cough:
            return "CARDIAC_PROMPT"
        return "Symptoms are nonspecific / unclear."


def check_symptoms():  
    symptoms = {
        "fever": varfever.get(),
        "cough": varcough.get(),
        "chest_pain": varchestpain.get(),
        "breathless": varbreath.get(),
        "nose": varnose.get(),
        "runny": runny_type.get(),
        "cough_type": cough_type.get(),
        "sore": varsore.get(),
        "sneezing": varsneezing.get(),
        "fatigue": varfatigue.get(),
        "body_ache": varbodyache.get(),
        "headache": varheadache.get(),
        "dry_mouth": vardrymouth.get(),
        "dizziness": vardizziness.get(),
        "vomiting": varvomiting.get(),
        "diarrhea": vardiarrhea.get(),
    }
    symptom_count = 0
    for value in symptoms.values():
        if isinstance(value, bool) and value:
            symptom_count += 1


    if symptom_count < MIN_SYMPTOMS:
        messagebox.showwarning("Too few symptoms", f"Please select at least {MIN_SYMPTOMS} symptoms.")
        return

    if symptom_count > MAX_SYMPTOMS:
        messagebox.showwarning("Too many symptoms",f"Please select no more than {MAX_SYMPTOMS} symptoms.\n")
        return
    base_diag = diagnose(symptoms)

    # If cardiac , ask follow-ups 
    if base_diag == "CARDIAC_PROMPT":
        swelling_resp = messagebox.askyesno("Swelling", "Is there swelling of ankle or leg?")
        if swelling_resp:
            final_diag = "Cardiac involvement (possible heart failure)"
            print("Diagnosis ->", final_diag)
            messagebox.showinfo("Symptom Checker Result", final_diag)
            return final_diag

        exertion_resp = messagebox.askyesno("Pain Pattern", "Does the pain worsen with exertion and improve with rest?")
        if exertion_resp:
            final_diag = "Cardiac pattern (possible angina/ischemia)"
            print("Diagnosis ->", final_diag)
            messagebox.showinfo("Symptom Checker Result", final_diag)
            return final_diag

        orthopnea_resp = messagebox.askyesno("Breathing Pattern", "Do you have difficulty breathing when lying flat (orthopnea)?")
        if orthopnea_resp:
            final_diag = "Cardiac involvement (possible heart failure)"
            print("Diagnosis ->", final_diag)
            messagebox.showinfo("Symptom Checker Result", final_diag)
            return final_diag

        # Fallback if no cardiac red flags
        final_diag = "Respiratory irritation / nonspecific"
        print("Diagnosis ->", final_diag)
        messagebox.showinfo("Symptom Checker Result", final_diag)
        return final_diag

    # Otherwise, display base diagnosis
    print("Diagnosis ->", base_diag)
    messagebox.showinfo("Symptom Checker Result", base_diag)
    return base_diag
# Tkinter GUI

root = tk.Tk()
import tkinter.font as tkFont

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12)   
root.option_add("*Font", default_font)

heading = tk.Label( root,text="Symptom Checker",font=("Arial", 20, "bold"),fg="purple")
heading.pack(pady=10)

root.title("Symptom Checker")
root.geometry("640x540")
root.resizable(True,True)
padx = 8
pady = 6

# Tk variables 
varfever = tk.BooleanVar()
varcough = tk.BooleanVar()
varchestpain = tk.BooleanVar()
varbreath = tk.BooleanVar()
varnose = tk.BooleanVar()
varsore = tk.BooleanVar()
varsneezing = tk.BooleanVar()
varfatigue = tk.BooleanVar()
varbodyache = tk.BooleanVar()
varheadache = tk.BooleanVar()
vardrymouth = tk.BooleanVar()
vardizziness = tk.BooleanVar()
varvomiting = tk.BooleanVar()
vardiarrhea = tk.BooleanVar()

# StringVars for option fields
runny_type = tk.StringVar(value="")   # "", "clear", "coloured"
cough_type = tk.StringVar(value="")   # "", "wet", "dry"

# Layout frames
top_frame = tk.Frame(root)
top_frame.pack(fill="x", padx=padx, pady=(pady, 0))

tk.Label(top_frame, text="Select symptoms that apply:", font=("TkDefaultFont", 12, "bold")).pack(anchor="w")

symp_frame = tk.Frame(root)
symp_frame.pack(fill="both", expand=False, padx=padx, pady=pady)

# Add checkboxes in two columns
left_col = tk.Frame(symp_frame)
left_col.grid(row=0, column=0, sticky="nw", padx=(0,20))
right_col = tk.Frame(symp_frame)
right_col.grid(row=0, column=1, sticky="nw")

# Left column checkbuttons
tk.Checkbutton(left_col, text="Fever", variable=varfever).pack(anchor="w")
tk.Checkbutton(left_col, text="Cough", variable=varcough).pack(anchor="w")
tk.Checkbutton(left_col, text="Chest pain", variable=varchestpain).pack(anchor="w")
tk.Checkbutton(left_col, text="Breathlessness", variable=varbreath).pack(anchor="w")
tk.Checkbutton(left_col, text="Nasal congestion / runny nose", variable=varnose).pack(anchor="w")
tk.Checkbutton(left_col, text="Sore throat", variable=varsore).pack(anchor="w")
tk.Checkbutton(left_col, text="Sneezing", variable=varsneezing).pack(anchor="w")

# Right column checkbuttons
tk.Checkbutton(right_col, text="Fatigue", variable=varfatigue).pack(anchor="w")
tk.Checkbutton(right_col, text="Body aches", variable=varbodyache).pack(anchor="w")
tk.Checkbutton(right_col, text="Headache", variable=varheadache).pack(anchor="w")
tk.Checkbutton(right_col, text="Dry mouth", variable=vardrymouth).pack(anchor="w")
tk.Checkbutton(right_col, text="Dizziness", variable=vardizziness).pack(anchor="w")
tk.Checkbutton(right_col, text="Vomiting", variable=varvomiting).pack(anchor="w")
tk.Checkbutton(right_col, text="Diarrhea", variable=vardiarrhea).pack(anchor="w")

# Options for runny_type and cough_type
opts_frame = tk.Frame(root)
opts_frame.pack(fill="x", padx=padx, pady=pady)

tk.Label(opts_frame, text="Runny nose type:").grid(row=0, column=0, sticky="w")
runny_menu = tk.OptionMenu(opts_frame, runny_type, "", "clear", "coloured")
runny_menu.grid(row=0, column=1, sticky="w", padx=6)

tk.Label(opts_frame, text="Cough type:").grid(row=1, column=0, sticky="w", pady=(6,0))
cough_menu = tk.OptionMenu(opts_frame, cough_type, "", "wet", "dry")
cough_menu.grid(row=1, column=1, sticky="w", padx=6, pady=(6,0))

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(fill="x", padx=padx, pady=(12, 8))

def on_check():
    # call the GUI wrapper
    check_symptoms()

def on_clear():
    # Reset all fields
    varfever.set(False)
    varcough.set(False)
    varchestpain.set(False)
    varbreath.set(False)
    varnose.set(False)
    varsore.set(False)
    varsneezing.set(False)
    varfatigue.set(False)
    varbodyache.set(False)
    varheadache.set(False)
    vardrymouth.set(False)
    vardizziness.set(False)
    varvomiting.set(False)
    vardiarrhea.set(False)
    runny_type.set("")
    cough_type.set("")

tk.Button(btn_frame, text="Check Symptoms", command=on_check, width=18).pack(side="left", padx=(0,8))
tk.Button(btn_frame, text="Clear", command=on_clear, width=12).pack(side="left")

# Run the app
if __name__ == "__main__":
    root.mainloop()
