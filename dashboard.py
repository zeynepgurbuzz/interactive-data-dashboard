import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt

class DataHandler:
    def __init__(self):
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()

    def load_data(self, path):
        self.df = pd.read_csv(path)
        self.filtered_df = self.df.copy()

    def get_numeric_columns(self):
        return self.df.select_dtypes(include='number').columns.tolist()

    def get_categorical_columns(self):
        return self.df.select_dtypes(include='object').columns.tolist()

    def filter_by_range(self, column, min_val, max_val):
        self.filtered_df = self.df[(self.df[column] >= min_val) & (self.df[column] <= max_val)]

    def get_stats(self, column):
        return self.filtered_df[column].describe()

class Visualizer:
    def __init__(self):
        self.last_plot = None

    def plot_histogram(self, df, col):
        plt.figure()
        df[col].plot(kind="hist", edgecolor="black")
        plt.title(f"{col} - Histogram")
        plt.xlabel(col)
        self.last_plot = plt.gcf()
        plt.show()

    def plot_line(self, df, col):
        plt.figure()
        df[col].plot(kind="line")
        plt.title(f"{col} - Line Plot")
        plt.ylabel(col)
        self.last_plot = plt.gcf()
        plt.show()

    def plot_scatter(self, df, x, y):
        plt.figure()
        plt.scatter(df[x], df[y])
        plt.title(f"{x} vs {y} - Scatter Plot")
        plt.xlabel(x)
        plt.ylabel(y)
        self.last_plot = plt.gcf()
        plt.show()

    def plot_pie(self, df, col):
        plt.figure()
        df[col].value_counts().plot(kind="pie", autopct="%1.1f%%")
        plt.title(f"{col} - Pie Chart")
        self.last_plot = plt.gcf()
        plt.show()

    def plot_heatmap(self, df):
        numeric_df = df.select_dtypes(include='number')
        corr = numeric_df.corr()
        if corr.shape[0] < 2:
            messagebox.showwarning("Heatmap Error", "Need at least two numeric columns for correlation heatmap.")
            return

        plt.figure(figsize=(8, 6))
        plt.imshow(corr, cmap='coolwarm', interpolation='none')
        plt.colorbar()
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        self.last_plot = plt.gcf()
        plt.show()

    def save_plot(self):
        if self.visualizer.last_plot:
            file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Plot As"
        )
        if file_path:
            self.visualizer.last_plot.savefig(file_path)
            messagebox.showinfo("Saved", f"Plot saved as:\n{file_path}")
        else:
            messagebox.showwarning("No Plot", "There is no plot to save.")

class VisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Data Explorer")
        self.data = DataHandler()
        self.visualizer = Visualizer()
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Upload CSV", command=self.load_file).grid(row=0, column=1, pady=10)

        tk.Label(self.root, text="Select Column:").grid(row=1, column=0)
        self.col_var = tk.StringVar()
        self.col_box = ttk.Combobox(self.root, textvariable=self.col_var, width=25)
        self.col_box.grid(row=1, column=1)
        self.col_box.bind("<<ComboboxSelected>>", lambda e: self.display_stats())

        self.stats_box = tk.Text(self.root, height=8, width=40)
        self.stats_box.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Label(self.root, text="Value Range Filter:").grid(row=3, column=0)
        self.min_entry = tk.Entry(self.root, width=10)
        self.min_entry.grid(row=3, column=1, sticky='w')
        self.max_entry = tk.Entry(self.root, width=10)
        self.max_entry.grid(row=3, column=1, sticky='e')
        tk.Button(self.root, text="Apply Filter", command=self.apply_filter).grid(row=3, column=2)

        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=5)
        tk.Button(btn_frame, text="Histogram", command=self.show_hist).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Line Plot", command=self.show_line).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Scatter Plot", command=self.show_scatter).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Pie Chart", command=self.show_pie).grid(row=0, column=3, padx=5)

        tk.Label(self.root, text="Scatter X:").grid(row=5, column=0)
        self.x_var = tk.StringVar()
        self.x_box = ttk.Combobox(self.root, textvariable=self.x_var)
        self.x_box.grid(row=5, column=1)

        tk.Label(self.root, text="Scatter Y:").grid(row=6, column=0)
        self.y_var = tk.StringVar()
        self.y_box = ttk.Combobox(self.root, textvariable=self.y_var)
        self.y_box.grid(row=6, column=1)

        tk.Label(self.root, text="Pie Chart Column:").grid(row=7, column=0)
        self.pie_var = tk.StringVar()
        self.pie_box = ttk.Combobox(self.root, textvariable=self.pie_var)
        self.pie_box.grid(row=7, column=1)

        tk.Button(self.root, text="Correlation Heatmap", command=self.show_heatmap).grid(row=8, column=0, columnspan=4, pady=10)
        tk.Button(self.root, text="Save Last Plot", command=self.save_plot).grid(row=9, column=0, columnspan=4)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.data.load_data(path)
            num_cols = self.data.get_numeric_columns()
            cat_cols = self.data.get_categorical_columns()
            self.col_box['values'] = num_cols
            self.x_box['values'] = num_cols
            self.y_box['values'] = num_cols
            self.pie_box['values'] = cat_cols
            messagebox.showinfo("Success", "CSV file loaded.")

    def display_stats(self):
        col = self.col_var.get()
        if col:
            stats = self.data.get_stats(col)
            self.stats_box.delete("1.0", tk.END)
            self.stats_box.insert(tk.END, stats.to_string())

    def show_hist(self):
        col = self.col_var.get()
        if col:
            self.visualizer.plot_histogram(self.data.filtered_df, col)

    def show_line(self):
        col = self.col_var.get()
        if col:
            self.visualizer.plot_line(self.data.filtered_df, col)

    def show_scatter(self):
        x = self.x_var.get()
        y = self.y_var.get()
        if x and y:
            self.visualizer.plot_scatter(self.data.filtered_df, x, y)

    def show_pie(self):
        col = self.pie_var.get()
        if col:
            self.visualizer.plot_pie(self.data.filtered_df, col)

    def show_heatmap(self):
        self.visualizer.plot_heatmap(self.data.filtered_df)

    def save_plot(self):
        self.visualizer.save_plot("plot.png")
        messagebox.showinfo("Saved", "Plot saved as plot.png")

    def apply_filter(self):
        col = self.col_var.get()
        try:
            if col not in self.data.df.columns:
                raise ValueError("Selected column not in data.")

            min_val = float(self.min_entry.get())
            max_val = float(self.max_entry.get())

            if min_val > max_val:
                raise ValueError("Enter valid numeric filter values")

            self.data.filter_by_range(col, min_val, max_val)

            if self.data.filtered_df.empty:
                raise ValueError("No data in selected range.")

            self.display_stats()

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()
