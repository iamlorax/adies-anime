import tkinter as tk
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
        self.refresh_options = [
            ("Dev", tk.BooleanVar()),
            ("Test", tk.BooleanVar()),
            ("Prod", tk.BooleanVar()),
        ]

        # Add Refresh Credentials option to the menu
        self.refresh_credentials_menu.add_command(label="Refresh Credentials", command=self.open_refresh_window)

        # Attach Refresh Credentials menu to the menu bar
        self.menu_bar.add_cascade(label="Menu", menu=self.refresh_credentials_menu)

        self.status_bar = tk.Text(self, height=1)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, anchor=tk.CENTER)

        self.status_bar.tag_config("active", foreground="green")
        self.status_bar.tag_config("inactive", foreground="red")
        self.status_bar.tag_config("ending_soon", foreground="DarkGoldenrod4")
        self.status_bar.tag_configure("center", justify="center")

        self.status_bar.insert("1.0", "Dev - ")
        self.status_bar.insert("end", "Active", "active")
        self.status_bar.insert("end", " | Test - ")
        self.status_bar.insert("end", "Inactive", "inactive")
        self.status_bar.insert("end", " | Prod - ")
        self.status_bar.insert("end", "Ending Soon", "ending_soon")
        self.status_bar.tag_add("center", "1.0", "end")

        # Create status bar
        # self.status_bar = tk.Label(self, text="Dev - Active   |   Test - Inactive   |   Prod - Expiring Soon")
        # self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # TODO: Button on right of status bar to run get_login_status() function as described in line 69
        # TODO: Perhaps add an alert status if remaining time is < 5 minutes
        # TODO: Active, Inactive, Expiring Soon

        # Configure menu bar and attach it to the window
        self.config(menu=self.menu_bar)

    def open_refresh_window(self):
        # Create a new window for refreshing credentials
        refresh_window = tk.Toplevel(self)
        refresh_window.title("Refresh Credentials")
        refresh_window.geometry("300x300")

        def refresh():
            # Disable the refresh button and checkboxes
            refresh_button.config(state=tk.DISABLED)
            for checkbox in checkboxes:
                checkbox.config(state=tk.DISABLED)

            # Get selected options
            selected_options = [option[0] for option in self.refresh_options if option[1].get()]

            # Create a Label to display "Refreshing..."
            refresh_label = tk.Label(refresh_window, text="Refreshing...", padx=10, pady=5)

            # Update refreshing label text and pack
            refresh_label.config(text="Refreshing {}...\n\nPlease see the console to complete login.".format(", ".join(selected_options)))
            refresh_label.pack(pady=20)

            # TODO: Call LOGIN
            def refresh_thread():
                # Simulating refreshing process for 5 seconds
                import time
                time.sleep(5)

                # Display "Refresh complete!" text
                refresh_label.config(text="Refresh complete!")

                # TODO: Function to read pickle files and get status of each account
                # dev,test,prod = get_login_status()

                # TODO: Refresh status label
                # status_bar.config(text="Dev - {status}   |   Test - {status}   |   Prod - {status}")

                # Close the refresh window after a short delay
                refresh_window.after(1000, refresh_window.destroy)

            # Start a separate thread for refreshing
            threading.Thread(target=refresh_thread).start()

        # Create a frame to hold the options
        options_frame = tk.Frame(refresh_window)
        options_frame.pack(pady=10)

        # Create checkboxes for refresh options
        checkboxes = []
        for option in self.refresh_options:
            checkbox = tk.Checkbutton(options_frame, text=option[0], variable=option[1])
            checkbox.pack(side=tk.TOP, anchor="w")
            checkboxes.append(checkbox)

        # Create Refresh button
        refresh_button = tk.Button(refresh_window, text="Refresh", command=refresh)
        refresh_button.pack(pady=10)

        # Center align the options frame
        options_frame.pack_configure(anchor=tk.CENTER)

        # Set the refresh_window as transient to the main window (makes it appear on top)
        refresh_window.transient(self)

        # Set the refresh_window as a modal window
        refresh_window.grab_set()

# Create and run the application
app = Application()
app.mainloop()
