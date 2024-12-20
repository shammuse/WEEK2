import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_folder(folder_name):
    """Create a folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def plot_histograms_and_boxplots(data, quantitative_columns):
    """Plot histograms and boxplots for numeric columns and save them."""
    histogram_folder = "graphs/histograms"
    boxplot_folder = "graphs/boxplots"
    create_folder(histogram_folder)
    create_folder(boxplot_folder)

    for col in quantitative_columns:
        # Histogram
        plt.figure(figsize=(8, 4))
        sns.histplot(data[col], kde=True)
        plt.title(f"Histogram of {col}")
        plt.tight_layout()
        plt.savefig(f"{histogram_folder}/{col}_histogram.png")
        plt.close()

        # Boxplot
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=data[col])
        plt.title(f"Boxplot of {col}")
        plt.tight_layout()
        plt.savefig(f"{boxplot_folder}/{col}_boxplot.png")
        plt.close()

def plot_scatterplots(data, application_columns, target_column):
    """Plot scatterplots for application data vs Total Data and save them."""
    scatterplot_folder = "graphs/scatterplots"
    create_folder(scatterplot_folder)

    for app in application_columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=data[app], y=data[target_column])
        plt.title(f"{target_column} vs {app}")
        plt.xlabel(app)
        plt.ylabel(target_column)
        plt.tight_layout()
        plt.savefig(f"{scatterplot_folder}/{app}_scatterplot.png")
        plt.close()

def plot_correlation_matrix(data, columns):
    """Plot and save the correlation matrix."""
    correlation_folder = "graphs/correlation"
    create_folder(correlation_folder)

    correlation_matrix = data[columns].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(f"{correlation_folder}/correlation_matrix.png")
    plt.close()
