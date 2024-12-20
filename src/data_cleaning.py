import numpy as np

def handle_missing_values(data):
    """Replace missing values with column means for numeric columns."""
    quantitative_columns = data.select_dtypes(include=np.number).columns
    data[quantitative_columns] = data[quantitative_columns].apply(lambda col: col.fillna(col.mean()))
    print("Missing values handled.")
    return data

def treat_outliers(data):
    """Handle outliers using the IQR method for numeric columns."""
    quantitative_columns = data.select_dtypes(include=np.number).columns
    for col in quantitative_columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        data[col] = np.where(data[col] < lower_bound, lower_bound, data[col])
        data[col] = np.where(data[col] > upper_bound, upper_bound, data[col])
    print("Outliers handled.")
    return data
