import customtkinter as ctk
# import customtkinter as ctk
app = ctk.CTk()
app.geometry("500x400")
app.title("My App")

label = ctk.CTkLabel(app, text="Hello World", font=("Arial", 24))
label.pack(pady=30)

button = ctk.CTkButton(app, text="Click Me")
button.pack()

app.mainloop()