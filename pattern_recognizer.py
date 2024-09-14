import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
from collections import Counter
import ttkbootstrap as tb


class PatternRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pattern Recognizer")
        self.master.geometry("900x700")  # Set a larger window size
        self.style = tb.Style(theme="superhero")

        self.file_path = None
        self.data = None
        self.pattern_data = []  # Store pattern results
        self.csv_visible = True  # Control CSV path visibility

        # Make the window responsive
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Main Frame with Padding
        self.main_frame = ttk.Frame(master, padding=32)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)

        # Frame for CSV summary
        self.summary_frame = ttk.Frame(self.main_frame)
        self.summary_frame.grid(row=0, column=0, pady=10, sticky="ew")
        self.summary_frame.grid_columnconfigure(0, weight=1)

        # Label for displaying CSV summary
        self.csv_summary_label = ttk.Label(self.summary_frame, text="No CSV file loaded", style="primary.TLabel",
                                           font=("Helvetica", 12, "bold"))
        self.csv_summary_label.grid(row=0, column=0, sticky="w")

        # Toggle CSV Location Button
        self.toggle_button = ttk.Button(self.summary_frame, text="Hide CSV Location", command=self.toggle_csv_location,
                                        style="info.TButton")
        self.toggle_button.grid(row=0, column=1, sticky="e")

        # Upload Button
        self.upload_button = ttk.Button(self.main_frame, text="Upload CSV", command=self.upload_csv,
                                        style="success.TButton")
        self.upload_button.grid(row=1, column=0, pady=5, sticky="w")

        # Reload Button
        self.reload_button = ttk.Button(self.main_frame, text="Reload CSV", command=self.reload_csv,
                                        style="warning.TButton")
        self.reload_button.grid(row=1, column=0, pady=5)

        # Exit Button
        self.exit_button = ttk.Button(self.main_frame, text="Exit", command=self.master.quit, style="danger.TButton")
        self.exit_button.grid(row=1, column=0, pady=5, sticky="e")

        # Frame for column selection, pattern length, and sorting
        self.selection_frame = ttk.Frame(self.main_frame)
        self.selection_frame.grid(row=2, column=0, pady=10, sticky="ew")

        # Column Selection Dropdown
        self.column_label = ttk.Label(self.selection_frame, text="Select Column:", style="info.TLabel",
                                      font=("Helvetica", 10))
        self.column_label.grid(row=0, column=0, padx=5)
        self.column_dropdown = tk.StringVar(master)
        self.column_dropdown.set("No Column Selected")
        self.column_menu = ttk.OptionMenu(self.selection_frame, self.column_dropdown, "No Column Selected")
        self.column_menu.grid(row=0, column=1, padx=5)

        # Pattern Length Selection Dropdown
        self.pattern_label = ttk.Label(self.selection_frame, text="Select Pattern Length:", style="info.TLabel",
                                       font=("Helvetica", 10))
        self.pattern_label.grid(row=0, column=2, padx=5)
        self.pattern_length = tk.IntVar(value=4)
        self.pattern_menu = ttk.OptionMenu(self.selection_frame, self.pattern_length, 4, 3, 4, 5)
        self.pattern_menu.grid(row=0, column=3, padx=5)

        # Sorting Options Dropdown
        self.sorting_label = ttk.Label(self.selection_frame, text="Sort By:", style="info.TLabel", font=("Helvetica", 10))
        self.sorting_label.grid(row=0, column=4, padx=5)
        self.sorting_option = tk.StringVar(value="Descending")
        self.sorting_menu = ttk.OptionMenu(self.selection_frame, self.sorting_option, "Descending", "Ascending")
        self.sorting_menu.grid(row=0, column=5, padx=5)

        # Analyze Button
        self.analyze_button = ttk.Button(self.main_frame, text="Analyze Patterns", command=self.analyze_patterns,
                                         style="success.TButton")
        self.analyze_button.grid(row=3, column=0, pady=20)

        # Results Display Frame with Scroll
        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.grid(row=4, column=0, pady=10, sticky="nsew")

        self.result_text = tk.Text(self.result_frame, height=20, width=80, wrap="word", font=("Helvetica", 12))
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.result_frame, command=self.result_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=self.scrollbar.set)

        # Start automatic reload
        self.start_auto_reload()

    def upload_csv(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.file_path:
            return

        self.load_csv()

    def reload_csv(self):
        if self.file_path:
            self.load_csv()
        else:
            messagebox.showerror("Error", "No CSV file loaded. Please upload a CSV file first.")

    def load_csv(self):
        try:
            self.data = pd.read_csv(self.file_path)
            self.update_column_options()
            self.show_csv_summary()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def update_column_options(self):
        if self.data is not None:
            columns = list(self.data.columns)
            menu = self.column_menu["menu"]
            menu.delete(0, "end")
            for col in columns:
                menu.add_command(label=col, command=lambda c=col: self.column_dropdown.set(c))

    def show_csv_summary(self):
        if self.data is not None:
            num_rows, num_columns = self.data.shape
            summary_text = f"Loaded CSV: {self.file_path if self.csv_visible else 'CSV Loaded'}\nTotal Rows: {num_rows}\nTotal Columns: {num_columns}"
            self.csv_summary_label.config(text=summary_text)

    def toggle_csv_location(self):
        self.csv_visible = not self.csv_visible
        self.toggle_button.config(text="Show CSV Location" if not self.csv_visible else "Hide CSV Location")
        self.show_csv_summary()

    def analyze_patterns(self):
        if self.data is None or self.column_dropdown.get() == "No Column Selected":
            messagebox.showerror("Error", "Please upload a CSV file and select a column.")
            return

        try:
            selected_column = self.column_dropdown.get()
            column_data = self.data[selected_column]
            pattern_length = self.pattern_length.get()

            # Extract all patterns of the selected length in the selected column
            patterns = [tuple(column_data[i:i + pattern_length]) for i in range(len(column_data) - pattern_length + 1)]

            # Count the frequency of each pattern
            pattern_counts = Counter(patterns)

            # Convert to a sorted list based on the user's choice
            self.pattern_data = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=self.sorting_option.get() == "Descending")

            self.display_patterns()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze patterns: {e}")

    def display_patterns(self):
        self.result_text.delete(1.0, tk.END)
        for pattern, count in self.pattern_data:
            pattern_str = ' '.join(str(num) for num in pattern)
            self.result_text.insert(tk.END, f"Pattern: {pattern_str} | Occurrences: {count}\n")

    def start_auto_reload(self):
        self.reload_csv()
        self.master.after(5000, self.start_auto_reload)  # Reload every 5 seconds


if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = PatternRecognizerApp(root)
    root.mainloop()
