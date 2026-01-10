# 📈 Interactive Data Analysis Dashboard (OOP)

A modular desktop application for loading, analyzing, and visualizing CSV datasets. Built with **Python (Tkinter)**, this project utilizes **Object-Oriented Programming (OOP)** principles to separate data handling, logic, and visualization layers.

## 🚀 Key Features

* **OOP Architecture:** Clean code structure with dedicated classes (`DataHandler`, `Visualizer`) for better maintainability.
* **Dynamic Data Loading:** Import any CSV file and automatically detect numeric/categorical columns.
* **Advanced Filtering:** Filter data rows based on value ranges dynamically.
* **Real-time Visualization:** Generate Histograms and other plots instantly using **Matplotlib**.
* **Statistical Summary:** Get instant descriptive statistics (mean, std, min, max) for selected columns.

## 🛠️ Software Architecture

The application is structured into modular components:

* **`DataHandler` Class:** Manages Pandas DataFrames, handles data loading, and executes filtering logic.
* **`Visualizer` Class:** Abstraction layer for generating Matplotlib charts.
* **`App` (GUI) Class:** Handles Tkinter widgets and user interaction.

## 📦 Libraries Used

* **Pandas:** For high-performance data manipulation.
* **Matplotlib:** For embedding plots into the GUI.
* **Tkinter:** For the graphical user interface.

## ⚙️ How to Run

1.  Clone the repository:
    ```bash
    https://github.com/zeynepgurbuzz/interactive-data-dashboard.git
    ```
2.  Install dependencies:
    ```bash
    pip install pandas matplotlib
    ```
3.  Run the application:
    ```bash
    python dashboard.py
    ```

---
Author: Zeynep Gürbüz
