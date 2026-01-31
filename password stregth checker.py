import math
import string
import tkinter as tk
from tkinter import *
root=tk.Tk()
root.title("Password strength checker")
root.resizable(False,False)
root.configure(bg="#2B2B2B")
root.columnconfigure(0, weight=1)
Title=tk.Label(root,text="Password Strength Analyzer",bg="#1F2933",fg="#F9FAFB",font=("Caliber",16,"bold"))
Title.grid(row=0,column=0,pady=10)
e=Entry(root,width=30,borderwidth=5,bg= "#111827",fg="#E5E7EB",font=("Arial",12,"bold"),show="*")
e.grid(row=1,column=0,sticky="we")
check=Button(root,text="Check Strength",bg="#F59E0B",fg="#111827",activebackground="#D97706",font=("Arial",12,"bold"),command=lambda:password_analyze(e.get()))
check.grid(row=3,column=0,pady=10)
COMMON_PASSWORD=["password","123456","123456789","qwerty","abc123"]
show_pass=tk.BooleanVar()
show_check=tk.Checkbutton(root,text="Show  password",bg="#2B2B2B",fg="#E5E7EB",variable=show_pass,font=("Arial",10),relief="flat",command=lambda:toggle(),activeforeground="#E5E7EB",activebackground="#2B2B2B")
show_check.grid(row=2,column=0,sticky="w",padx=5)
def toggle():
    if show_pass.get():
        e.config(show="")
    else:
        e.config(show="*")
def password_analyze(password):
    score, strength, feedback=calculate_password_strength(password)
    score_label=tk.Label(root,text=f"Password Strength Score: {score}/100",bg= "#2B2B2B",fg="#E5E7EB",font=("Caliber",12))
    score_label.grid(row=4,column=0,pady=5)
    strength_label=tk.Label(root,text=f"Password  Strength Level: {strength}",bg="#534B4B",fg="white",font=("Caliber",12,"bold"))
    strength_label.grid(row=5,column=0,pady=5)
    feedback_box=tk.Text(root,height=10,width=50,bg="#111827",fg="#FBBF24",font=("Arial",12,"bold","italic"))
    feedback_box.grid(row=6,column=0,pady=10)
    if feedback:
        for f in feedback:
            feedback_box.insert(tk.END, f"• {f}\n")
    else:
        feedback_box.insert(tk.END, "Good password. No major weaknesses detected.")

    # Color coding
    colors = {
        "Very Weak": "red",
        "Weak": "orange",
        "Moderate": "gold",
        "Strong": "green",
        "Very Strong": "dark green"
    }
    strength_label.config(fg=colors.get(strength, "black"))
def calculate_password_strength(password :str):
    score=0
    feedback=[]
    length = len(password)
    #checking the length of the password
    if length==0:
        return 0,"Invalid",["Password cannot be empty"]
    if length<6:
        feedback.append("Password is too  short")
    elif 6<=length<=7:
        score+=10
    elif 8<=length<=9:
        score+=15
    elif 10<=length<=12:
        score+=20
    else:
        score+=30
    #checking the variety of letters
    has_lower=any(c.islower() for c in password)
    has_upper=any(c.isupper() for  c in password)
    has_digit=any(c.isdigit() for c in password)
    has_special=any(c in string.punctuation for c in password)

    variety_count=sum([has_lower, has_upper, has_digit, has_special])
    if variety_count<3:
        feedback.append("Use a mix of upper,lower,digits and special characters")
    score+=variety_count*6.25

    #repetitions
    for i in range(len(password)-2):
        if password[i]==password[i+1]==password[i+2]:
            feedback.append("Avoid repeating characters")
            score-=5
            break
    #checking sequences
    seq="abcdefghijklmnopqrstuvwxyz0123456789"
    if password.lower() in seq or password.lower()[::-1] in seq[::-1]:
        feedback.append("Sequential pattern detected")
        score-=10
    #checking common passwords
    if password.lower() in COMMON_PASSWORD:
        feedback.append("Password is too common")
        score-=10    

    #checking entropy
    char_set=0
    if has_lower:char_set+=26
    if has_upper:char_set+=26
    if has_digit:char_set+=10
    if has_special:char_set+=len(string.punctuation)
    entropy=length*math.log2(char_set)
    entropy_score=min(entropy/60*20,20)
    score+=entropy_score


    #Checking the score   
    score=max(0,min(100,int(score)))
    strength=""
    if score<40:
        strength="Weak"
    elif 40<=score<75:
        strength="Moderate"
    else:
        strength="Strong"
    return (score, strength, feedback)
pw=input("Enter your password:")
score, strength, feedback=calculate_password_strength(pw)
print(f"Password Strength Score: {score}/100")
print(f"Password Strength Level: {strength}")
if feedback:
    print("Feedback to improve your password:")
    for f in feedback:
        print(f"- {f}")
root.update_idletasks()
w_w=root.winfo_width()
w_h=root.winfo_height()
s_w=root.winfo_screenwidth()
s_h=root.winfo_screenheight()
window_x=int((s_w/2)-(w_w/2))
window_y=int((s_h/2)-(w_h/2))
root.geometry(f"{w_w}x{w_h}+{window_x}+{window_y}")
root.mainloop()