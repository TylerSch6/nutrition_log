import tkinter as tk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk

path = r"C:\study\AA2025_spring\Mel\cisp71\Project\\"

class NutritionDB:
    def __init__(self, db_path=path + "nutrition_log.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nutrition_log (
                date TEXT PRIMARY KEY,
                weight REAL,            
                protein REAL,
                fat REAL,
                carbs REAL,
                calorie REAL
            )
        ''')
        self.conn.commit()

    def insert_entry(self, date, weight, protein, fat, carbs, calorie):
        try:
            self.cursor.execute('''
                INSERT INTO nutrition_log (date, weight, protein, fat, carbs, calorie)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (date, weight, protein, fat, carbs, calorie))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_entry(self, date, weight, protein, fat, carbs, calorie):
        self.cursor.execute('''
            UPDATE nutrition_log
            SET weight=?, protein=?, fat=?, carbs=?, calorie=?
            WHERE date=?
        ''', (date, weight, protein, fat, carbs, calorie))
        self.conn.commit()

    def delete_entry(self, date):
        self.cursor.execute('''
            DELETE FROM nutrition_log WHERE date=?
        ''', (date,))
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute('''
            SELECT * FROM nutrition_log ORDER BY date DESC
        ''')
        return self.cursor.fetchall()

    def search_by_date(self, date):
        self.cursor.execute("SELECT * FROM nutrition_log WHERE date=?", (date,))
        return self.cursor.fetchall()

    def get_all_records(self):
        self.cursor.execute("SELECT * FROM nutrition_log ORDER BY date")
        return self.cursor.fetchall()



class NutritionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Nutrition Tracker")
        self.root.iconbitmap(path + "diet.ico")
        self.root.geometry("650x600")

        self.db = NutritionDB()
        self.create_widgets()
        self.show_all()  # 启动时自动显示数据
    
    def create_widgets(self):
# 第一块，标题
        title_label = tk.Label(self.root,text="Daily Nutrition Tracker",font=("Arial", 24),fg="blue")
        title_label.place(x=360, y=75, anchor='n')

#插入图片
        img = Image.open(path + "image.jpg")
        img = img.resize((150, 150))  # 调整图片大小
        self.photo = ImageTk.PhotoImage(img)

        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.place(x=10, y=10)

# 第二块区域，输入框 (Label + Entry）)
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

        self.calorie_label = tk.Label(self.root, text="Calorie (kcal):")
        self.calorie_label.place(x=350, y=250)
        self.calorie_entry = tk.Entry(self.root)
        self.calorie_entry.place(x=450, y=250)

#第三块区域 展示表格
        self.tree = ttk.Treeview(self.root, columns=("date", "weight", "protein", "fat", "carbs", "calorie"), show="headings")
        self.tree.place(x=60, y=290, width=530, height=200)
        self.tree.heading("date", text="Date")
        self.tree.heading("weight", text="Weight")
        self.tree.heading("protein", text="Protein")
        self.tree.heading("fat", text="Fat")
        self.tree.heading("carbs", text="Carbohydrate")
        self.tree.heading("calorie", text="Tatal Calorie")
# 设置一下列宽，这样表格不会一开始太窄或看起来歪斜
        for col in ("date", "weight", "protein", "fat", "carbs", "calorie"):
            self.tree.column(col, width=80, anchor="center")

#第四块，“添加 / 更新 / 删除 / 清空”按钮，以及对应函数
        self.add_button = tk.Button(self.root, text="Add", command=self.add_record)
        self.add_button.place(x=60, y=500)

        self.update_button = tk.Button(self.root, text="Update", command=self.update_record)
        self.update_button.place(x=130, y=500)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_record)
        self.delete_button.place(x=210, y=500)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_inputs)
        self.clear_button.place(x=290, y=500)

        self.show_all_button = tk.Button(self.root, text="Show All", command=self.show_all)
        self.show_all_button.place(x=370, y=500)  


    def add_record(self):
        data = (
            self.date_entry.get(),
            self.weight_entry.get(),
            self.protein_entry.get(),
            self.fat_entry.get(),
            self.carbs_entry.get(),
            self.calorie_entry.get()
        )
        if "" in data:
            messagebox.showwarning("Input Required", "Please fill in all fields.")
            return
        try:
            self.db.insert_entry(*data)
            self.show_all()
            self.clear_inputs()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate Entry", "A record for this date already exists. Use Update instead.")

    def update_record(self):
        data = (
            self.weight_entry.get(),
            self.protein_entry.get(),
            self.fat_entry.get(),
            self.carbs_entry.get(),
            self.calorie_entry.get(),
            self.date_entry.get()
        )
        if "" in data:
            messagebox.showwarning("Input Required", "Please fill in all fields.")
            return
        self.db.update_record(data)
        self.show_all()
        self.clear_inputs()

    def delete_record(self):
        date = self.date_entry.get()
        if not date:
            messagebox.showwarning("Input Required", "Please enter the date of the record to delete.")
            return
        self.db.delete_record(date)
        self.show_all()
        self.clear_inputs()


    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.protein_entry.delete(0, tk.END)
        self.fat_entry.delete(0, tk.END)
        self.carbs_entry.delete(0, tk.END)
        self.calorie_entry.delete(0, tk.END)

    def show_all(self):
        # 从数据库获取所有记录
        records = self.db.get_all_records()

        # 清空表格内容
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 将所有记录插入表格
        for rec in records:
            self.tree.insert("", tk.END, values=rec)
            

        #第5部分，查找
        # Label 提示
        self.search_label = tk.Label(self.root, text="Search by Date (YYYY-MM-DD):")
        self.search_label.place(x=60, y=550)

        # 输入框
        self.search_entry = tk.Entry(self.root)
        self.search_entry.place(x=240, y=550, width=120)

        # 查找按钮
        self.search_button = tk.Button(self.root, text="Search", command=self.search_record)
        self.search_button.place(x=370, y=545)

    def search_record(self):
        date = self.search_entry.get()
        if not date:
            messagebox.showwarning("Input Required", "Please enter a date to search.")
            return
        
        records = self.db.search_by_date(date)
        # 先清空表格
        for row in self.tree.get_children():
            self.tree.delete(row)
        if records:
            for rec in records:
                self.tree.insert("", tk.END, values=rec)
        else:
            messagebox.showinfo("No Result", f"No records found for date {date}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = NutritionApp(root)
    root.mainloop()
