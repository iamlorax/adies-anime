import tkinter as tk
from tkinter import messagebox
import threading

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("Menu Bar Example")
        self.geometry("400x300")

        # Create menu bar
        self.menu_bar = tk.Menu(self)

        # Create Refresh Credentials menu
        self.refresh_credentials_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.refresh_options = {
            "A": tk.BooleanVar(),
            "B": tk.BooleanVar(),
            "C": tk.BooleanVar()
        }

        # Add Refresh Credentials option to the menu
        self.refresh_credentials_menu.add_command(label="Refresh Credentials", command=self.open_refresh_window)

        # Attach Refresh Credentials menu to the menu bar
        self.menu_bar.add_cascade(label="Menu", menu=self.refresh_credentials_menu)

        # Configure menu bar and attach it to the window
        self.config(menu=self.menu_bar)

        # Create a label for displaying refresh status
        self.refresh_status_label = tk.Label(self, text="", anchor=tk.W)
        self.refresh_status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def open_refresh_window(self):
        # Create a new window for refreshing credentials
        refresh_window = tk.Toplevel(self)
        refresh_window.title("Refresh Credentials")
        refresh_window.geometry("300x200")

        # Create a Label to display "Refreshing..."
        refresh_label = tk.Label(refresh_window, text="", padx=10, pady=20)

        def refresh():
            # Disable the refresh button and hide the checkboxes
            refresh_button.config(state=tk.DISABLED)
            for checkbox in checkboxes:
                checkbox.pack_forget()

            # Get selected options
            selected_options = [option for option, var in self.refresh_options.items() if var.get()]

            # Display "Refreshing..." text with selected options
            refresh_label.config(text="Refreshing {}...".format(", ".join(selected_options)))
            refresh_label.pack(pady=20)

            def refresh_thread():
                # Simulating refreshing process for 2 seconds
                import time
                time.sleep(2)

                # Display "Refresh complete!" text
                refresh_label.config(text="Refresh complete!")

                # Enable the refresh button
                refresh_button.config(state=tk.NORMAL)

                # Update refresh status label in the root window
                self.update_refresh_status(selected_options)

                # Close the refresh window after a short delay
                refresh_window.after(1000, refresh_window.destroy)

            # Start a separate thread for refreshing
            threading.Thread(target=refresh_thread).start()

        # Create Refresh button
        refresh_button = tk.Button(refresh_window, text="Refresh", command=refresh)
        refresh_button.pack(pady=10)

        # Create a frame to hold the options
        options_frame = tk.Frame(refresh_window)
        options_frame.pack(pady=10)

        # Create checkboxes for refresh options
        checkboxes = []
        for option, var in self.refresh_options.items():
            checkbox = tk.Checkbutton(options_frame, text="Refresh " + option, variable=var)
            checkbox.pack(side=tk.LEFT)
            checkboxes.append(checkbox)

        # Center align the options frame
        options_frame.pack_configure(anchor=tk.CENTER)

        # Set the refresh_window as transient to the main window (makes it appear on top)
        refresh_window.transient(self)

        # Set the refresh_window as a modal window
        refresh_window.grab_set()

    def update_refresh_status(self, refreshed_options):
        status_text = "Refreshed: {}".format(", ".join(refreshed_options))
        self.refresh_status_label.config(text=status_text)

# Create and run the application
app = Application()
app.mainloop()
