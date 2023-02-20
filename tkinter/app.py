import csv
import tkinter as tk
from tkinter import ttk


class ScreenOne(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Screen 1").pack(pady=10)
        tk.Button(self, text="Next", command=self.next_screen).pack()

    def next_screen(self):
        self.master.current_screen += 1
        self.master.show_frame()


class ScreenTwo(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Screen 2").pack(pady=10)
        tk.Button(self, text="Next", command=self.next_screen).pack()
        tk.Button(self, text="Back", command=self.back_screen).pack()

    def next_screen(self):
        self.master.current_screen += 1
        self.master.show_frame()

    def back_screen(self):
        self.master.current_screen -= 1
        self.master.show_frame()


class ScreenThree(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Screen 3").pack(pady=10)
        tk.Button(self, text="Back", command=self.back_screen).pack()

    def back_screen(self):
        self.master.current_screen -= 1
        self.master.show_frame()


def csv_to_dict(file_path):
    result_list = []
    with open(file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            result_list.append(row)
    return result_list


class CheckboxTreeview(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.data = csv_to_dict("./data.csv")
        columns = self.data[0]
        check_box_columns = ["cb1", "cb2", "cb3"]
        self.columns = columns + check_box_columns
        del self.data[0]

        self.pack()

        for i, label in enumerate(self.columns):
            col_label = tk.Label(
                self,
                text=label,
                font=("Helvetica", 14, "bold"),
                bg="#f0f0f0",
                fg="#333",
                padx=5,
                pady=5,
                bd=1,
                relief="solid",
                width=12
            )
            col_label.grid(row=0, column=i, sticky="nsew")

        for i, row in enumerate(self.data):
            format_args = {
                "width": 20,
                "font": ("Helvetica", 12),
                "bd": 1,
                "relief": "solid"
            }
            # create the cells for this row
            name_entry = tk.Label(self, text=row[0], **format_args)
            name_entry.grid(row=i+1, column=0)
            
            age_entry = tk.Label(self, text=row[1], **format_args)
            age_entry.grid(row=i+1, column=1)
            
            gender_entry = tk.Label(self, text=row[2], **format_args)
            gender_entry.grid(row=i+1, column=2)

            cb1 = ttk.Checkbutton(self)
            cb1.grid(row=i+1, column=3)

            cb2 = ttk.Checkbutton(self)
            cb2.grid(row=i+1, column=4)

            cb3 = ttk.Checkbutton(self)
            cb3.grid(row=i+1, column=5)

        # for record in self.data:
        #     for i in range(3):
        #         record.append("")

        # for record in self.data:
        #     item = self.insert("", "end", values=record)
        #     cb1 = ttk.Checkbutton(self)
        #     cb2 = ttk.Checkbutton(self)
        #     cb3 = ttk.Checkbutton(self)

        #     # self.set(item, "#0", "")
        #     self.item(item, values=("","","",cb1,"",""))
        #     self.item(item, values=("","","","",cb2,""))
        #     self.item(item, values=("","","","","",cb3))

    def get_checked_items(self):
        checked_items = []
        for item in self.get_children():
            if self.item(item, "values")[1] == 1:
                checked_items.append(self.item(item, "text"))
        return checked_items


class Application(tk.Tk):
    """initialize toplevel tk window"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, className=" QuickSight Migration Tool", *args, **kwargs)
        self.geometry("1000x400")
        self.current_screen = 1
        self.screens = {}
        self.create_screens()

    def create_screens(self):
        """define 3 screens that will be viewable"""
        screen_one = CheckboxTreeview(self)
        screen_two = ScreenTwo(self)
        screen_three = ScreenThree(self)

        self.screens[1] = screen_one
        self.screens[2] = screen_two
        self.screens[3] = screen_three

        screen_one.pack()

    def show_frame(self):
        """show frame for current screen"""
        for screen in self.screens.values():
            screen.pack_forget()

        self.screens[self.current_screen].pack()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
