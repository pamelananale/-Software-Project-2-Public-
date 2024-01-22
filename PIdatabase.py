import tkinter as tk
from tkinter import ttk, filedialog
import csv
import json

class PersonalInformation:
    def __init__(self, perinfo):
        self.perinfo = perinfo
        self.perinfo.title("Personal Information")
        self.data = []
        self.perinfo.configure(bg="#ffc0cb")
        self.perinfo.geometry("1200x300")
        self.gui()

    def gui(self):
        
        #labels
        tk.Label(self.perinfo, text="Entry Number").grid(row=0, column=0, pady=5)
        tk.Label(self.perinfo, text="First Name").grid(row=1, column=0, pady=5)
        tk.Label(self.perinfo, text="Last Name").grid(row=2, column=0, pady=5)
        tk.Label(self.perinfo, text="Age").grid(row=3, column=0, pady=5)
        tk.Label(self.perinfo, text="Pronoun").grid(row=4, column=0, pady=5)
        tk.Label(self.perinfo, text="Marital Status").grid(row=5, column=0, pady=5)

        #widgets
        self.entry_no_entry = tk.Spinbox(self.perinfo, from_=0, to=100)
        self.entry_no_entry.grid(row=0, column=1, padx=5, pady=5)

        self.first_name_entry = tk.Entry(self.perinfo)
        self.first_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.last_name_entry = tk.Entry(self.perinfo)
        self.last_name_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.age_entry = tk.Spinbox(self.perinfo, from_=0, to=100)
        self.age_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.pronoun_var = tk.StringVar()
        pronoun_dropdown = ttk.Combobox(self.perinfo, textvariable=self.pronoun_var,
                                            values=["Prefer not to say", "She/Her", "He/Him", "They/Them"])
        pronoun_dropdown.grid(row=4, column=1, padx=5, pady=5)
        
        self.marital_status_var = tk.StringVar()
        marital_status_dropdown = ttk.Combobox(self.perinfo, textvariable=self.marital_status_var,
                                                    values=["Single", "Married", "Widowed", "Separated"])
        marital_status_dropdown.grid(row=5, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(self.perinfo, text="Add Entry", command=self.add_entry).grid(row=0, column=15, columnspan=5, pady=10)
        tk.Button(self.perinfo, text="Update Entry", command=self.update_entry).grid(row=0, column=20, columnspan=5, pady=10)
        tk.Button(self.perinfo, text="Delete Entry", command=self.delete_entry).grid(row=0, column=25, columnspan=5, pady=10)
        tk.Button(self.perinfo, text="Export to CSV", command=self.export_to_csv).grid(row=1, column=15, columnspan=5, pady=10)
        tk.Button(self.perinfo, text="Import from CSV", command=self.import_from_csv).grid(row=1, column=20, columnspan=5, pady=10)
        tk.Button(self.perinfo, text="Export to JSON", command=self.export_to_json).grid(row=2, column=15, columnspan=5, pady=10)

        # Treeview for real-time tabular view
        self.tree = ttk.Treeview(self.perinfo, columns=("Entry Number", "First Name", "Last Name", "Age", "Pronoun", "Marital Status"), show="headings")
        self.tree.grid(row=0, column=2, rowspan=12, padx=10, pady=10)

        # Set column headings
        for col in ["Entry Number", "First Name", "Last Name", "Age", "Pronoun", "Marital Status"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Populate tree with data
        self.update_tree()

        # Treeview event binding
        self.tree.bind("<ButtonRelease-1>", self.select_item)

    def add_entry(self):
        entry_no = int(self.entry_no_entry.get())
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        age = int(self.age_entry.get())
        pronoun = self.pronoun_var.get()
        marital_status = self.marital_status_var.get()

        if entry_no and first_name and last_name and age and pronoun and marital_status:
            self.data.append([entry_no, first_name, last_name, age, pronoun, marital_status])
            self.update_tree()

            self.entry_no_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.pronoun_var.set("")
            self.marital_status_var.set("")

    def update_entry(self):
        selected_item = self.tree.selection()
        if selected_item:
            entry_no = int(self.entry_no_entry.get())
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            age = int(self.age_entry.get())
            pronoun = self.pronoun_var.get()
            marital_status = self.marital_status_var.get()

            if entry_no and first_name and last_name and age and pronoun and marital_status:
                selected_index = self.tree.index(selected_item)
                self.data[selected_index] = [entry_no, first_name, last_name, age, pronoun, marital_status]
                self.update_tree()

    def delete_entry(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_index = self.tree.index(selected_item)
            del self.data[selected_index]
            self.update_tree()

    def update_tree(self):
        # Clear existing data in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Populate tree with updated data
        for row in self.data:
            self.tree.insert("", tk.END, values=row)

    def select_item(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            selected_index = self.tree.index(selected_item)
            entry_data = self.data[selected_index]

            self.entry_no_entry.delete(0, tk.END)
            self.entry_no_entry.insert(0, entry_data[0])

            self.first_name_entry.delete(0, tk.END)
            self.first_name_entry.insert(0, entry_data[1])
            
            self.last_name_entry.delete(0, tk.END)
            self.last_name_entry.insert(0, entry_data[2])

            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, entry_data[3])

            self.pronoun_var.set(entry_data[4])

            self.marital_status_var.set(entry_data[5])

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(self.data)

    def export_to_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as json_file:
                json.dump(self.data, json_file)

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.load_data_from_csv(file_path)
            self.update_tree()

    def load_data_from_csv(self, file_path):
        try:
            with open(file_path, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                self.data = [row for row in csv_reader]
        except FileNotFoundError:
            pass  


if __name__ == "__main__":
    perinfo = tk.Tk()
    app = PersonalInformation(perinfo)
    perinfo.mainloop()
