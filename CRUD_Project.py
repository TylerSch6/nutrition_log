import tkinter as tk # Import the Tkinter GUI toolkit
import sqlite3 # Import the SQLite3 library to interact with a local SQLite database
from tkinter import messagebox # Import the messagebox module for showing popup alerts and messages
from PIL import Image, ImageTk # Import Image and ImageTk from the Pillow library for image handling in Tkinter
from tkinter import ttk # Import the themed Tkinter widgets
# Avoid 'from tkinter import *' to prevent conflicts with ttk

path = r"C:\study\AA2025_spring\Mel\cisp71\Project\\" # File path for images, database, and icon

# SQLite database class
class NutritionDB:
    def __init__(self, db_path=path + "nutrition_log.db"):
        # Connect to database
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        # Create table if not exists
        # Date as primary key(The app is for self use only, and there is only one entry per day), stored as text
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nutrition_log (
                date TEXT PRIMARY KEY, 
                weight REAL,            
                protein REAL,
                fat REAL,
                carbs REAL,
                workout_type TEXT
            )
        ''')
        self.conn.commit() # Save changes to database

    # Insert a new record
    def insert_entry(self, date, weight, protein, fat, carbs, workout_type):
        self.cursor.execute('''
            INSERT INTO nutrition_log (date, weight, protein, fat, carbs, workout_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, weight, protein, fat, carbs, workout_type))
        self.conn.commit()
    
    # Update an existing record
    # Because the primary key might be updated, two parameters—old_date and new_date—are set.
    def update_entry(self, old_date, new_date, weight, protein, fat, carbs, workout_type):
        self.cursor.execute('''
            UPDATE nutrition_log
            SET date=?, weight=?, protein=?, fat=?, carbs=?, workout_type=?
            WHERE date=?
        ''', (new_date, weight, protein, fat, carbs, workout_type, old_date))
        # Pass these parameters in order to the SQL statement
        self.conn.commit()

    # Delete a record by date
    def delete_record(self, date):
        self.cursor.execute('''
            DELETE FROM nutrition_log WHERE date=?
        ''', (date,))
        self.conn.commit()

    # Search for a record by date
    def search_by_date(self, date):
        self.cursor.execute("SELECT * FROM nutrition_log WHERE date=?", (date,))
        return self.cursor.fetchall()

    # Get all records sorted by date (latest first)
    def get_all_records(self):
        self.cursor.execute("SELECT * FROM nutrition_log ORDER BY date DESC")
        return self.cursor.fetchall()

# Main application class
class NutritionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Nutrition Tracker")  # Set window title
        self.root.iconbitmap(path + "diet.ico")  # Set window icon
        self.root.geometry("650x600")  # Set window size

        self.db = NutritionDB()  # Create database object
        self.create_widgets()  # Call function to create all UI widgets
        self.show_all()  # Show all records on start
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Daily Nutrition Tracker", font=("Arial", 24), fg="blue")
        title_label.place(x=360, y=75, anchor='n')

        # Load and display image
        img = Image.open(path + "image.jpg")
        img = img.resize((150, 150))  # Resize image to 150x150 pixels
        self.photo = ImageTk.PhotoImage(img)  # Convert image to Tkinter format
        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.place(x=10, y=10)

        # Create labels and entry boxes for each input field
        self.date_label = tk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date_label.place(x=60, y=170)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.place(x=200, y=170)

        self.weight_label = tk.Label(self.root, text="Weight (kg):")
        self.weight_label.place(x=350, y=170)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.place(x=450, y=170)

        self.protein_label = tk.Label(self.root, text="Protein (g):")
        self.protein_label.place(x=60, y=210)
        self.protein_entry = tk.Entry(self.root)
        self.protein_entry.place(x=200, y=210)

        self.fat_label = tk.Label(self.root, text="Fat (g):")
        self.fat_label.place(x=350, y=210)
        self.fat_entry = tk.Entry(self.root)
        self.fat_entry.place(x=450, y=210)

        self.carbs_label = tk.Label(self.root, text="Carbs (g):")
        self.carbs_label.place(x=60, y=250)
        self.carbs_entry = tk.Entry(self.root)
        self.carbs_entry.place(x=200, y=250)

        self.workout_type_label = tk.Label(self.root, text="Workout Type:")
        self.workout_type_label.place(x=350, y=250)
        self.workout_var = tk.StringVar()  # Create variable to store workout selection
        self.workout_var.set("None")  # Set default workout option
        workout_options = ["Cardio", "Strength", "Yoga", "Stretching", "None"]  # Workout choices
        self.workout_menu = tk.OptionMenu(self.root, self.workout_var, *workout_options)  # Create dropdown menu
        self.workout_menu.place(x=450, y=245)

        # Table to show records
        self.tree = ttk.Treeview(self.root, columns=("date", "weight", "protein", "fat", "carbs", "workout_type"), show="headings")
        self.tree.place(x=60, y=290, width=530, height=200)
        # Define column headers
        self.tree.heading("date", text="Date")
        self.tree.heading("weight", text="Weight")
        self.tree.heading("protein", text="Protein")
        self.tree.heading("fat", text="Fat")
        self.tree.heading("carbs", text="Carbohydrate")
        self.tree.heading("workout_type", text="Workout Type")

        # Set column widths
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("weight", width=80, anchor="center")
        self.tree.column("protein", width=80, anchor="center")
        self.tree.column("fat", width=80, anchor="center")
        self.tree.column("carbs", width=80, anchor="center")
        self.tree.column("workout_type", width=110, anchor="center")

        # Bind click event to load selected row data
        self.tree.bind("<ButtonRelease-1>", self.load_selected_record)

        # Action buttons
        self.add_button = tk.Button(self.root, text="Add", command=self.add_record)
        self.add_button.place(x=60, y=500)

        self.update_button = tk.Button(self.root, text="Update", command=self.update_record)
        self.update_button.place(x=130, y=500)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_record, fg="red")
        self.delete_button.place(x=210, y=500)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_inputs)
        self.clear_button.place(x=290, y=500)

        self.show_all_button = tk.Button(self.root, text="Show All", command=self.show_all)
        self.show_all_button.place(x=370, y=500)

        # Search section
        self.search_label = tk.Label(self.root, text="Search by Date (YYYY-MM-DD):")
        self.search_label.place(x=60, y=550)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.place(x=240, y=550, width=120)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_record)
        self.search_button.place(x=370, y=545)

    # Load selected row into input fields
    def load_selected_record(self, event):
        selected_item = self.tree.focus() # Get selected item in Treeview
        # Note: focus() returns the currently focused item (single selection).
        # For multiple selections, use tree.selection() which returns a tuple of selected items.
        if not selected_item:
            return
        # If nothing selected, do nothing
        record = self.tree.item(selected_item, 'values') # Get record values from selected row
        # Fill entry boxes with selected record data
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, record[0])
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, record[1])
        self.protein_entry.delete(0, tk.END)
        self.protein_entry.insert(0, record[2])
        self.fat_entry.delete(0, tk.END)
        self.fat_entry.insert(0, record[3])
        self.carbs_entry.delete(0, tk.END)
        self.carbs_entry.insert(0, record[4])
        self.workout_var.set(record[5]) # Set workout dropdown to selected value

    # Add new record
    def add_record(self):
        # Get data from input fields and group them into a tuple(Simple, safe, and order-fixed)
        data = (
            self.date_entry.get(),
            self.weight_entry.get(),
            self.protein_entry.get(),
            self.fat_entry.get(),
            self.carbs_entry.get(),
            self.workout_var.get()
        )
        # Check if any field is empty
        if "" in data:
            messagebox.showwarning("Input Required", "Please fill in all fields.")
            return
        try:
            self.db.insert_entry(*data)  # Insert data into database, "*" is unpacking operator
            self.show_all()  # Refresh table display
            self.clear_inputs()  # Clear input fields
        except sqlite3.IntegrityError: # Show error if date already exists (primary key conflict)
            messagebox.showerror("Duplicate Entry", "A record for this date already exists. Use Update instead.")

    # Update selected record
    def update_record(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a record to update.")
            return
        old_date = self.tree.item(selected, "values")[0]  # Old date to identify record
        new_date = self.date_entry.get()
        weight = self.weight_entry.get()
        protein = self.protein_entry.get()
        fat = self.fat_entry.get()
        carbs = self.carbs_entry.get()
        workout_type = self.workout_var.get()
        # Check if all fields filled
        if "" in (new_date, weight, protein, fat, carbs, workout_type):
            messagebox.showwarning("Input Required", "Please fill in all fields.")
            return
        try:
            self.db.update_entry(old_date, new_date, weight, protein, fat, carbs, workout_type)
            self.show_all()
            self.clear_inputs()
        except sqlite3.IntegrityError:  # Error if new date conflicts with existing record
            messagebox.showerror("Duplicate Entry", "A record with this date already exists.")

    # Delete a record by date
    def delete_record(self):
        date = self.date_entry.get() # Get date from input
        if not date:
            messagebox.showwarning("Input Required", "Please enter the date of the record to delete.")
            return
        self.db.delete_record(date)  # Delete record from DB
        self.show_all()  # Refresh table
        self.clear_inputs()  # Clear inputs

    # Clear all input fields
    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.protein_entry.delete(0, tk.END)
        self.fat_entry.delete(0, tk.END)
        self.carbs_entry.delete(0, tk.END)
        self.workout_var.set("None")

    # Show all records
    def show_all(self):
        records = self.db.get_all_records() # Get all records from database
        for row in self.tree.get_children(): # Clear all rows in the table first
            self.tree.delete(row)
        for rec in records: # Insert all records into the table
            self.tree.insert("", tk.END, values=rec)

    # Search by date
    def search_record(self):
        date = self.search_entry.get() # Get date to search
        if not date:  # If the input is empty, show a warning message box
            messagebox.showwarning("Input Required", "Please enter a date to search.")
            return
        records = self.db.search_by_date(date) # Call the database method to search for records by date
        # Clear all existing rows in the Treeview before inserting new search results
        for row in self.tree.get_children():
            self.tree.delete(row)
        # If records are found, insert each record into the Treeview
        if records:
            for rec in records:
                self.tree.insert("", tk.END, values=rec)
        # If no records are found, show an informational message box
        else:
            messagebox.showinfo("No Result", f"No records found for date {date}.")


# Start the app
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window using Tkinter
    app = NutritionApp(root)  # Instantiate the NutritionApp class with the root window
    root.mainloop()  # Run the main event loop to keep the application window open