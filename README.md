XDR Data Analysis Project
This project involves the analysis of XDR (Extended Data Record) data, focusing on cleaning, visualization, and performing Principal Component Analysis (PCA). The analysis includes handling missing values, treating outliers, visualizing data distributions, correlations, and applying PCA to extract meaningful patterns from the data.

Requirements
Python 3.x
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
PostgreSQL (for database connection)
You can install the required libraries using pip:

bash
Copy code
pip install pandas numpy matplotlib seaborn scikit-learn psycopg2
Files
main.py: The main script that connects to the PostgreSQL database, loads the data, performs data cleaning, creates new columns, generates visualizations, and applies PCA.
data_cleaning.py: Functions for handling missing values and treating outliers in the data.
plotting.py: Functions to generate histograms, boxplots, scatterplots, and correlation matrices.
pca_analysis.py: Functions to apply Principal Component Analysis (PCA) on the data.
Usage
Database Connection: Ensure that the PostgreSQL database is accessible. Modify the connection parameters in main.py as necessary:

python
Copy code
connection = connect_to_postgres('postgres', 'your_password', '10.11.0.81', '5432', 'your_database')
Running the Script: Execute main.py to load the data, clean it, visualize it, and perform PCA.

bash
Copy code
python main.py
Workflow
Connect to PostgreSQL: The script connects to the PostgreSQL database and loads the data from the specified table (xdr_data in this case).
Data Cleaning:
Handles missing values by calling the handle_missing_values function.
Treats outliers using the treat_outliers function.
New Columns: Adds two new columns:
"Total Data (Bytes)": The sum of "Total DL (Bytes)" and "Total UL (Bytes)".
"Duration Decile": The duration is divided into 10 equal deciles.
Plotting:
Histograms and boxplots are plotted for quantitative columns.
Scatter plots and a correlation matrix are plotted for specific application-related columns (e.g., Social Media, Google, Email, etc.).
PCA: Principal Component Analysis (PCA) is applied to reduce dimensionality and find patterns in the data.
Output
Cleaned Data: The cleaned data is saved as cleaned_data.csv (optional).
Visualizations: Various plots, including histograms, boxplots, scatterplots, and correlation matrix, are generated and displayed.
PCA Results: PCA is applied to the data, and the results can be analyzed further.
Notes
Make sure to adjust the database connection parameters (username, password, host, port, and database name) according to your setup.
You can modify the query in the main.py script to load different datasets from your database.
Ensure that the PostgreSQL server is running and accessible
