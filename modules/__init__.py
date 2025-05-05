# modules/__init__.py

# --- Uploader ---
from .uploader import allowed_file, save_and_load

# --- Cleaner ---
from .cleaner import detect_missing, drop_missing, fill_missing, \
                       detect_outliers_zscore, drop_outliers

# --- Analyzer ---
from .analyzer import run_kmeans, run_regression

# --- Visualizer ---
#from .visualizer import plot_histogram, plot_bar, plot_pie, plot_scatter

# --- Exporter ---
#from .exporter import export_csv, export_excel

__all__ = [
    # uploader
    'allowed_file', 'save_and_load',
    # cleaner
    'detect_missing', 'drop_missing', 'fill_missing',
    'detect_outliers_zscore', 'drop_outliers',
    # analyzer
    'run_kmeans', 'run_regression',
    # visualizer
    #'plot_histogram', 'plot_bar', 'plot_pie', 'plot_scatter',
    # exporter
    #'export_csv', 'export_excel',
]
