import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PlaylistPlanner:
    def __init__(self, master):
        self.master = master
        master.title("TV Playlist Planner")

        self.contents = []

        # UI Elements
        tk.Label(master, text="Назва контенту:").grid(row=0, column=0)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)

        tk.Label(master, text="Тривалість (хвилини):").grid(row=1, column=0)
        self.duration_entry = tk.Entry(master)
        self.duration_entry.grid(row=1, column=1)

        tk.Label(master, text="Тип контенту:").grid(row=2, column=0)
        self.type_combo = ttk.Combobox(master, values=["Фільм", "Серіал", "Реклама", "Передача", "Інше"])
        self.type_combo.grid(row=2, column=1)

        self.add_button = tk.Button(master, text="Додати", command=self.add_content)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(master, columns=("name", "duration", "type"), show="headings")
        self.tree.heading("name", text="Назва")
        self.tree.heading("duration", text="Тривалість (хв)")
        self.tree.heading("type", text="Тип")
        self.tree.grid(row=4, column=0, columnspan=2, pady=5)

        self.total_label = tk.Label(master, text="Загальна тривалість: 0 хв")
        self.total_label.grid(row=5, column=0, columnspan=2)

        self.missing_label = tk.Label(master, text="Не вистачає: 1440 хв (24 години)")
        self.missing_label.grid(row=6, column=0, columnspan=2)

        self.export_button = tk.Button(master, text="Експортувати плейлист", command=self.export_playlist)
        self.export_button.grid(row=7, column=0, columnspan=2, pady=5)

    def add_content(self):
        name = self.name_entry.get()
        try:
            duration = int(self.duration_entry.get())
        except ValueError:
            messagebox.showerror("Помилка", "Тривалість повинна бути числом!")
            return
        content_type = self.type_combo.get()
        if not name or not content_type:
            messagebox.showerror("Помилка", "Заповніть всі поля!")
            return

        self.contents.append({"name": name, "duration": duration, "type": content_type})
        self.tree.insert("", tk.END, values=(name, duration, content_type))
        self.update_labels()

        self.name_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.type_combo.set("")

    def update_labels(self):
        total = sum(item["duration"] for item in self.contents)
        missing = 1440 - total  # 24 години = 1440 хвилин
        self.total_label.config(text=f"Загальна тривалість: {total} хв")
        if missing > 0:
            self.missing_label.config(text=f"Не вистачає: {missing} хв")
        else:
            self.missing_label.config(text="Сітка заповнена або переповнена!")

    def export_playlist(self):
        with open("playlist.txt", "w", encoding="utf-8") as f:
            for item in self.contents:
                f.write(f'{item["name"]}, {item["duration"]} хв, {item["type"]}\n')
        messagebox.showinfo("Експорт", "Плейлист експортовано у playlist.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistPlanner(root)
    root.mainloop()
