import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.datasets import make_blobs

# Generate synthetic data
X, labels_true = make_blobs(n_samples=2000, centers=4, cluster_std=0.1, random_state=0)

# Set the parameter k equal to the MinPts recommended by DBSCAN
k = 4

# Compute the nearest neighbors
nbrs = NearestNeighbors(n_neighbors=k).fit(X)
distances, indices = nbrs.kneighbors(X)

# Sort the distances
sorted_distances = np.sort(distances[:, k-1], axis=0)

# Plot the k-distance graph
plt.figure(figsize=(8, 4))
plt.plot(sorted_distances)
plt.title("K-distance Graph")
plt.xlabel("Points sorted by distance")
plt.ylabel(f"Distance to {k}-th nearest neighbor")
plt.grid(True)
plt.show()
