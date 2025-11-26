import tkinter as tk
from tkinter import messagebox, ttk
import os  # <-- Finding files quickly

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager Pro - Admin Edition")
        self.root.geometry("1000x650")

        # --- 1. PATH SETUP --- 
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.filename = os.path.join(self.base_dir, "StudentMarks.txt")
        self.logo_path = os.path.join(self.base_dir, "my logo.png")

        # Data storage
        self.student_data = []

        # Setup UI
        self.setup_styles()
        self.setup_icon()
        self.create_menu()
        self.create_controls()
        self.create_treeview()
        self.create_statusbar()

        # Load Initial Data
        self.load_data()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam") 
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=25)

    def setup_icon(self):
        """Attempts to load a logo.png file from the script directory"""
        try:
            # Check if the file exists before trying to load it
            if os.path.exists(self.logo_path):
                icon_image = tk.PhotoImage(file=self.logo_path)
                # Set the icon for the window
                self.root.iconphoto(False, icon_image)
            else:
                print(f"Logo not found at: {self.logo_path}. Using default icon.")
        except Exception as e:
            print(f"Could not load icon: {e}")

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # --- FILE MENU ---
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Reload File", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # --- EDIT MENU ---
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Add New Student", command=self.add_student)
        edit_menu.add_command(label="Update Selected Student", command=self.update_student)
        edit_menu.add_command(label="Delete Selected Student", command=self.delete_student)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # --- VIEW MENU ---
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Show All Students", command=self.refresh_table)
        view_menu.add_separator()
        view_menu.add_command(label="Show A Grades Only", command=self.show_a_grades)
        view_menu.add_command(label="Show F Grades Only", command=self.show_f_grades)
        menu_bar.add_cascade(label="View", menu=view_menu)

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=10)

        # Search
        tk.Label(control_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        entry_search = tk.Entry(control_frame, textvariable=self.search_var, width=20)
        entry_search.pack(side="left", padx=5)
        entry_search.bind("<KeyRelease>", self.filter_data)

        # Main Table Filters
        tk.Button(control_frame, text="Reset View", command=self.clear_filter).pack(side="left", padx=5)

        # --- ACTION BUTTONS ---
        tk.Button(control_frame, text="Add Student", bg="#d0e1f9", command=self.add_student).pack(side="right", padx=5)
        tk.Button(control_frame, text="Delete", bg="#ffcccc", command=self.delete_student).pack(side="right", padx=5)
        tk.Button(control_frame, text="Update", bg="#fff2cc", command=self.update_student).pack(side="right", padx=5)

    def create_treeview(self):
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("ID", "Name", "C1", "C2", "C3", "Exam", "Total", "%", "Grade")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Define headings and column widths
        widths = [60, 180, 40, 40, 40, 50, 60, 60, 60]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=w, anchor="center")
        
        self.tree.column("Name", anchor="w")

        self.tree.tag_configure("grade_A", background="#d4edda")
        self.tree.tag_configure("grade_F", background="#f8d7da")

    def create_statusbar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side="bottom", fill="x")

    # ---------- Data Logic ----------

    def load_data(self):
        self.student_data = []
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
                if not lines: return

                for line in lines[1:]: 
                    parts = line.strip().split(",")
                    if len(parts) != 6: continue
                    try:
                        s_id = int(parts[0])
                        name = parts[1].strip()
                        c1, c2, c3, exam = map(int, parts[2:])
                        
                        # Store raw data for editing later
                        total = c1 + c2 + c3 + exam
                        percentage = (total / 160) * 100
                        grade = self.calculate_grade(percentage)

                        self.student_data.append({
                            "ID": s_id, "Name": name, 
                            "C1": c1, "C2": c2, "C3": c3, "Exam": exam, 
                            "Total": total, "Percentage": round(percentage, 2),
                            "Grade": grade
                        })
                    except ValueError: continue 

            self.refresh_table()
            
        except FileNotFoundError:
            # Uses the absolute path so the user knows exactly where it was looking
            messagebox.showerror("Error", f"File not found!\nLooking at:\n{self.filename}")

    def save_to_file(self):
        """Writes the current self.student_data list back to the text file."""
        try:
            with open(self.filename, "w") as file:
                # First line is the count of students
                file.write(f"{len(self.student_data)}\n")
                
                # Subsequent lines: ID,Name,C1,C2,C3,Exam
                for s in self.student_data:
                    line = f"{s['ID']},{s['Name']},{s['C1']},{s['C2']},{s['C3']},{s['Exam']}\n"
                    file.write(line)
            # Log success (optional)
            self.status_var.set("File saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file: {e}")

    def calculate_grade(self, percentage):
        if percentage >= 70: return "A"
        if percentage >= 60: return "B"
        if percentage >= 50: return "C"
        if percentage >= 40: return "D"
        return "F"

    # ---------- CRUD FEATURES (Add, Update, Delete) ----------

    def add_student(self):
        """Popup window to add a new student"""
        self.open_edit_window(title="Add Student")

    def update_student(self):
        """Popup window to edit selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Student", "Please select a student to update.")
            return

        # Get the ID of the selected row
        item_values = self.tree.item(selected[0], "values")
        selected_id = int(item_values[0])

        # Find the full student object
        student_obj = next((s for s in self.student_data if s["ID"] == selected_id), None)
        
        if student_obj:
            self.open_edit_window(title="Update Student", student=student_obj)

    def delete_student(self):
        """Deletes selected student and saves file"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Student", "Please select a student to delete.")
            return

        item_values = self.tree.item(selected[0], "values")
        selected_id = int(item_values[0])
        student_name = item_values[1]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?")
        if confirm:
            # Remove from list
            self.student_data = [s for s in self.student_data if s["ID"] != selected_id]
            self.save_to_file()
            self.refresh_table()
            messagebox.showinfo("Deleted", f"Student {student_name} deleted.")

    def open_edit_window(self, title, student=None):
        """Generic window for Adding OR Updating a student"""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("300x350")
        
        # Try to set the icon for the popup too!
        if os.path.exists(self.logo_path):
             win.iconphoto(False, tk.PhotoImage(file=self.logo_path))

        # Fields
        labels = ["ID", "Name", "Coursework 1 (20)", "Coursework 2 (20)", "Coursework 3 (20)", "Exam (100)"]
        entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(win, text=label_text).pack(pady=2)
            entry = tk.Entry(win)
            entry.pack(pady=2)
            entries[label_text] = entry

        # Pre-fill data if Updating
        if student:
            entries["ID"].insert(0, student["ID"])
            entries["ID"].config(state="disabled") # Usually ID shouldn't change
            entries["Name"].insert(0, student["Name"])
            entries["Coursework 1 (20)"].insert(0, student["C1"])
            entries["Coursework 2 (20)"].insert(0, student["C2"])
            entries["Coursework 3 (20)"].insert(0, student["C3"])
            entries["Exam (100)"].insert(0, student["Exam"])

        def save_action():
            try:
                # Validation
                s_id = int(entries["ID"].get())
                name = entries["Name"].get().strip()
                c1 = int(entries["Coursework 1 (20)"].get())
                c2 = int(entries["Coursework 2 (20)"].get())
                c3 = int(entries["Coursework 3 (20)"].get())
                exam = int(entries["Exam (100)"].get())

                if not name: raise ValueError("Name cannot be empty")
                if any(x < 0 for x in [c1, c2, c3, exam]): raise ValueError("Marks cannot be negative")

                # Calculations
                total = c1 + c2 + c3 + exam
                percentage = (total / 160) * 100
                grade = self.calculate_grade(percentage)

                new_record = {
                    "ID": s_id, "Name": name, 
                    "C1": c1, "C2": c2, "C3": c3, "Exam": exam, 
                    "Total": total, "Percentage": round(percentage, 2),
                    "Grade": grade
                }

                if student:
                    # UPDATE EXISTING
                    # Find index and replace
                    idx = next(i for i, s in enumerate(self.student_data) if s["ID"] == s_id)
                    self.student_data[idx] = new_record
                    action_type = "Updated"
                else:
                    # ADD NEW (Check ID unique)
                    if any(s["ID"] == s_id for s in self.student_data):
                        messagebox.showerror("Error", "Student ID already exists!")
                        return
                    self.student_data.append(new_record)
                    action_type = "Added"

                # Save and Close
                self.save_to_file()
                self.refresh_table()
                win.destroy()
                messagebox.showinfo("Success", f"Student {action_type} Successfully.")

            except ValueError as ve:
                messagebox.showerror("Input Error", f"Invalid Data: {ve}")

        tk.Button(win, text="Save Record", bg="#d4edda", command=save_action).pack(pady=15, fill="x", padx=20)

    # ---------- View Logic ----------

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if data is None:
            data = self.student_data

        total_percent = 0
        for s in data:
            tag = "normal"
            if s["Grade"] == "A": tag = "grade_A"
            elif s["Grade"] == "F": tag = "grade_F"
            
            self.tree.insert("", tk.END, values=(
                s["ID"], s["Name"], s["C1"], s["C2"], s["C3"], s["Exam"], 
                s["Total"], f"{s['Percentage']}%", s["Grade"]
            ), tags=(tag,))
            total_percent += s["Percentage"]

        count = len(data)
        avg = (total_percent / count) if count > 0 else 0
        self.status_var.set(f"Records Shown: {count} | Average: {avg:.2f}%")

    def filter_data(self, event=None):
        query = self.search_var.get().lower().strip()
        if not query:
            self.refresh_table()
            return
        filtered = [s for s in self.student_data if query in s["Name"].lower() or query in str(s["ID"])]
        self.refresh_table(filtered)

    def clear_filter(self):
        self.search_var.set("")
        self.refresh_table()

    def show_a_grades(self):
        if not self.student_data: return
        self.refresh_table([s for s in self.student_data if s["Grade"] == "A"])

    def show_f_grades(self):
        if not self.student_data: return
        self.refresh_table([s for s in self.student_data if s["Grade"] == "F"])

    def sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0].strip('%')), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0], reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()