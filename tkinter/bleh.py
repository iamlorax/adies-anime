import tkinter as tk
import csv

class GridFrameWindow:
    def __init__(self, parent, rows, cols, width, height):
        self.parent = parent
        self.rows = rows
        self.cols = cols + 3
        self.width = width
        self.height = height

        self.frames = [[None for c in range(self.cols)] for r in range(rows)]
        self.check_vars = [[None for c in range(cols, self.cols)] for r in range(rows)]

        # Create the grid of frames
        for r in range(rows):
            for c in range(self.cols):
                self.frames[r][c] = tk.Frame(parent, width=width, height=height, borderwidth=1, relief='solid')
                self.frames[r][c].grid(row=r, column=c, sticky='nsew')
                self.frames[r][c].grid_propagate(False)

            # Add checkbox columns to empty cells
            for i in range(self.cols - cols, self.cols):
                if r == 0:
                    label_text = "check{}".format(i - (self.cols - 3) + 1)
                    label = tk.Label(self.frames[r][i], text=label_text, font=('Arial', 10))
                    label.grid(row=r, column=i, sticky='nsew')
                else:
                    check_var = tk.BooleanVar()
                    self.check_vars[r][i - cols] = check_var  # store the variable in a 2D list
                    check = tk.Checkbutton(self.frames[r][i], variable=check_var)
                    check.pack(fill='both', expand=True)

    def pack(self, **kwargs):
        self.parent.pack(**kwargs)

    def set_data(self, data):
        for r in range(self.rows):
            for c in range(self.cols):
                if c < self.cols - 3:
                    self.frames[r][c].grid_propagate(False)
                    label = tk.Label(self.frames[r][c], text=data[r][c], font=('Arial', 10))
                    label.pack(fill='both', expand=True, padx=10, pady=10)

    def get_checked_rows(self):
        checked_rows = []
        for r in range(1, self.rows):
            for c in range(self.cols - 3, self.cols):
                if self.check_vars[r][c - (self.cols - 3)].get():
                    checked_rows.append(r)
                    break
        return checked_rows


class AppWindow:
    def __init__(self, root, csv_file, width, height):
        self.root = root
        self.root.title("Grid of Frames")

        # Read the CSV data
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            rows = len(data)
            cols = len(data[0])

        # Create a frame to hold the grid of frames
        frame_container = tk.Frame(root, padx=50, pady=50)
        frame_container.pack(fill="both", expand=True)

        # Create the grid of frames
        self.grid = GridFrameWindow(frame_container, rows, cols, width, height)

        # Populate the frames with data
        self.grid.set_data(data)

        # Create a "print" button
        self.print_button = tk.Button(frame_container, text="Print", command=self.print_checked_data)
        self.print_button.grid(row=height+1, column=0, sticky="nesw")

    def print_checked_data(self):
        checked_rows = self.grid.get_checked_rows()
        if len(checked_rows) > 0:
            print("Checked rows:")
            for r in checked_rows:
                row_data = []
                for c in range(self.grid.cols - 3):
                    frame = self.grid.frames[r][c]
                    widget = frame.winfo_children()[0]
                    if isinstance(widget, tk.Label):
                        row_data.append(widget.cget("text"))
                    elif isinstance(widget, tk.Checkbutton):
                        row_data.append(widget.var.get())
                print(row_data)
        else:
            print("No rows selected.")

if __name__ == '__main__':
    root = tk.Tk()
    app = AppWindow(root, 'data.csv', 100, 25)
    app.grid.pack()

    root.mainloop()
