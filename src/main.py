from database import connect_to_postgres, load_data_from_postgres
from data_cleaning import handle_missing_values, treat_outliers
from plotting import plot_histograms_and_boxplots, plot_scatterplots, plot_correlation_matrix
from pca_analysis import apply_pca

def main():
    # Connect to PostgreSQL
    connection = connect_to_postgres('postgres', 'sh36am67', '10.11.0.81', '5432', 'my_database')

    if connection:
        query = "SELECT * FROM xdr_data;"  # Replace with your actual query
        data = load_data_from_postgres(connection, query)
        
        print("Data Types and Missing Values:")
        print(data.info())
        print(data.isnull().sum())

        # Data Cleaning
        data = handle_missing_values(data)
        data = treat_outliers(data)

        # Save cleaned data (optional)
        data.to_csv("cleaned_data.csv", index=False)
        
        # Create new columns
        data["Total Data (Bytes)"] = data["Total DL (Bytes)"] + data["Total UL (Bytes)"]
        data["Duration Decile"] = pd.qcut(data["Dur. (ms)"], 10, labels=False, duplicates="drop") + 1
        
        # Plotting
        quantitative_columns = data.select_dtypes(include=np.number).columns
        plot_histograms_and_boxplots(data, quantitative_columns)

        application_columns = [
            "Social Media DL (Bytes)", "Google DL (Bytes)", "Email DL (Bytes)",
            "Youtube DL (Bytes)", "Netflix DL (Bytes)", "Gaming DL (Bytes)", "Other DL (Bytes)"
        ]
        plot_scatterplots(data, application_columns, "Total Data (Bytes)")
        plot_correlation_matrix(data, application_columns)

        # PCA
        apply_pca(data, application_columns)

        # Close the connection
        connection.close()

if __name__ == "__main__":
    main()