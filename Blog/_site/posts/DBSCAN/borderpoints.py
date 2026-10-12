import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import DBSCAN

# Generate synthetic data
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# Parameters for DBSCAN
eps = 0.3
min_samples = 4

# Apply DBSCAN
dbscan = DBSCAN(eps=eps, min_samples=min_samples)
labels = dbscan.fit_predict(X)

# Extract core, border, and noise points
core_samples_mask = np.zeros_like(dbscan.labels_, dtype=bool)
core_samples_mask[dbscan.core_sample_indices_] = True
unique_labels = set(labels)

# Plot setup
fig, ax = plt.subplots()
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

# Plot the results
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    # Plot core points
    xy = X[class_member_mask & core_samples_mask]
    ax.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14, label='Core points' if k != -1 else '')

    # Plot border points
    xy = X[class_member_mask & ~core_samples_mask]
    ax.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=8, label='Border points' if k != -1 else '')

    # Plot noise points separately to ensure proper legend entry
    if k == -1:
        ax.plot(xy[:, 0], xy[:, 1], 'x', color='black', markersize=10, label='Noise')

# Choose a point to draw the epsilon circle around (typically a core point)
core_point = X[dbscan.core_sample_indices_[30]]

# Draw a circle with radius epsilon
circle = plt.Circle((core_point[0], core_point[1]), eps, color='black', fill=False, linestyle='dashed', linewidth=1.5, label='Epsilon radius', zorder=3)
ax.add_artist(circle)
ax.annotate(f'ε={eps}', xy=(core_point[0] + eps, core_point[1]), xytext=(8, 8), textcoords='offset points', arrowprops=dict(arrowstyle='->', connectionstyle='arc3'))

# Draw a line from the center to the edge of the circle
end_point = (core_point[0] + eps, core_point[1])
ax.plot([core_point[0], end_point[0]], [core_point[1], end_point[1]], 'black', linewidth=2, zorder=4)

# Set aspect of the plot to be equal
ax.set_aspect('equal', adjustable='datalim')

# Title, labels, and legend
ax.set_title('DBSCAN clustering with ε illustration')
ax.set_xlabel('X')
ax.set_ylabel('Y')
subtitle_text = f'Number of samples: {len(X)}, ε: {eps}, MinPts: {min_samples}\nColor: Core points, Border points, Noise'
ax.set_title(subtitle_text, fontsize=10, style='italic')
ax.legend()

# Show plot
plt.show()
