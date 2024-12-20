from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import os

def apply_pca(data, columns, n_components=2):
    """Apply PCA to the data and plot the results."""
    pca_folder = "graphs/pca"
    create_folder(pca_folder)

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[columns])
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scaled_data)
    pca_df = pd.DataFrame(data=principal_components, columns=[f"PC{i+1}" for i in range(n_components)])
    
    print("Explained Variance Ratio:", pca.explained_variance_ratio_)

    # Plot PCA Results
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=pca_df["PC1"], y=pca_df["PC2"], hue=data["Total Data (Bytes)"], palette="viridis")
    plt.title("PCA Results")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.tight_layout()
    plt.savefig(f"{pca_folder}/pca_results.png")
    plt.close()
