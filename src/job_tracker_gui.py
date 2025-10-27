import tkinter as tk
from tkinter import filedialog, messagebox
from main import add_single_job, add_jobs_from_file

import os

class JobTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Job Tracker")
        self.create_credentials_screen()
    
    def create_credentials_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter your LinkedIn credentials", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=40)
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=40)
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Save & Continue", command=self.save_credentials).pack(pady=10)

    def save_credentials(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        # Save to .env file in project root
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(f"LINKEDIN_USERNAME={username}\nLINKEDIN_PASSWORD={password}\n")
            messagebox.showinfo("Success", "Credentials saved!")
            self.create_main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save credentials: {e}")

    # Removed login screen, credentials handled by backend

    def create_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="LinkedIn Job Tracker", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Add Single Job URL", command=self.add_single_job_gui).pack(pady=5)
        tk.Button(self.root, text="Import Jobs from CSV", command=self.import_csv_jobs_gui).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def add_single_job_gui(self):
        self.clear_screen()
        tk.Label(self.root, text="Paste LinkedIn Job URL:").pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=60)
        self.url_entry.pack(pady=5)
        tk.Button(self.root, text="Add Job", command=self.process_single_job_gui).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

    def process_single_job_gui(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a job URL.")
            return
        success, msg = add_single_job(url, source="Added via GUI")
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def import_csv_jobs_gui(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        added, error = add_jobs_from_file(file_path, source="Imported from GUI")
        if error:
            messagebox.showerror("Error", error)
        else:
            messagebox.showinfo("Import Complete", f"Imported {added} jobs from CSV.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = JobTrackerApp(root)
    root.mainloop()
