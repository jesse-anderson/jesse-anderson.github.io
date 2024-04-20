import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import OPTICS
from sklearn import datasets
from kneed import KneeLocator
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
from scipy.spatial import ConvexHull

# Load example data
n_samples = 1000
min_samples = 15
data, _ = datasets.make_blobs(n_samples=n_samples, centers=4, random_state=42, cluster_std=2.0)

# Plot the original data
plt.figure(figsize=(8, 6))
plt.scatter(data[:, 0], data[:, 1], alpha=0.6, edgecolors='w', s=30)
plt.title('Blob Data Distribution')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.grid(True)
plt.show()

# Step 1: Apply OPTICS
optics_model = OPTICS(min_samples=min_samples)
optics_model.fit(data)

# Step 2: Plot the reachability diagram
space = np.arange(len(data))
reachability = optics_model.reachability_[optics_model.ordering_]

# Check for infinity values in reachability distances
if np.isinf(reachability).any():
    print("Infinity values found in reachability distances, handling...")
    # Identify finite indices where reachability values are not infinity
    finite_indices = np.isfinite(reachability)

    # Filter out infinite reachability values and their corresponding indices
    reachability = reachability[finite_indices]
    space = space[finite_indices]

plt.figure(figsize=(10, 5))
plt.bar(space, reachability, color='g')
plt.title('OPTICS Reachability Plot')
plt.xlabel('Data points')
plt.ylabel('Reachability Distance')
plt.show()

# Plot sorted reachability distances
sorted_reachability = np.sort(reachability)
indices = np.arange(len(sorted_reachability))
plt.figure(figsize=(10, 5))
plt.plot(indices, sorted_reachability, label='Reachability Distance')

# Compute the line endpoints based on the first and last reachability distance
line_start = np.array([0, sorted_reachability[0]])
line_end = np.array([len(sorted_reachability) - 1, sorted_reachability[-1]])

# Calculate the slope and intercept of the line (y = mx + b)
slope = (line_end[1] - line_start[1]) / (line_end[0] - line_start[0])
intercept = line_start[1] - (slope * line_start[0])

# Calculate the y-values of the line across all x-values
line_y = (slope * indices) + intercept

# Plot the line
plt.plot(indices, line_y, 'r--', label='Line from first to last index')

# Find the elbow index (maximum deviation point)
deviations = np.abs(sorted_reachability - line_y)
elbow_index = np.argmax(deviations)

elbow_cutoff = sorted_reachability[elbow_index]


# Mark the elbow point
plt.axvline(x=elbow_index, color='b', linestyle='--', label=f'Elbow Point at index {elbow_index} = {elbow_cutoff}')
plt.axhline(y = elbow_cutoff, color = 'k', linestyle = ':', label = 'Cutoff for reachability distance.')
plt.title('Sorted Reachability Distances with Maximum Deviation Line')
plt.xlabel('Data points (sorted)')
plt.ylabel('Reachability Distance')
plt.legend()
plt.show()

elbow_cutoff =0.866 ##THIS IS A GREAT EXAMPLE OF WHEN YOUR ELBOW FAILS YOU AND YOU NEED TO PLAY AROUND WITH VALUES!!!!

#  Create a list of colors to use for bars below the threshold, and black for above
# We'll generate a color map to cycle through a set of colors for segments below the threshold
below_threshold_colors = list(mcolors.TABLEAU_COLORS.values())  # Get a set of unique colors
color_index = 0
current_color = below_threshold_colors[color_index]
colors = []

# Track whether the previous bar was below the threshold
previous_bar_below = False

# Assign colors to bars based on their height relative to the threshold
for val in reachability:
    if val <= elbow_cutoff:
        # If we're transitioning from above to below the threshold, change the color
        if not previous_bar_below:
            color_index = (color_index + 1) % len(below_threshold_colors)
            current_color = below_threshold_colors[color_index]
        colors.append(current_color)
        previous_bar_below = True
    else:
        colors.append('k')  # Black for bars above the threshold
        previous_bar_below = False

# Now, let's create the reachability plot with custom bar colors
plt.figure(figsize=(10, 5))
plt.axhline(y=elbow_cutoff, color='k', linestyle=':', label='Cutoff for reachability distance.')
plt.bar(space, reachability, color=colors)
plt.title('OPTICS Reachability Plot')
plt.xlabel('Data points')
plt.ylabel('Reachability Distance')
plt.legend()
plt.show()

# Step 3: Extract clusters using the reachability distance at the elbow point as a cutoff
# The reachability distance at the elbow is used as a threshold for cluster extraction
reachability_distance_at_elbow = elbow_cutoff

# Retrieve the ordered reachability distances from the OPTICS model
ordered_reachability = optics_model.reachability_[optics_model.ordering_]
ordered_indices = optics_model.ordering_

# Initialize all points as noise (-1)
labels = np.full(ordered_reachability.shape, -1)  

# Manually assign clusters based on the new threshold, apparently OPTICS.expand_clusters or similar doesn't work anymore so here we are...
cluster_id = 0
for i in range(len(ordered_reachability)):
    if ordered_reachability[i] <= reachability_distance_at_elbow:
        if labels[ordered_indices[i]] == -1:  # If this point has not been assigned a cluster
            # Start a new cluster from this point
            labels[ordered_indices[i]] = cluster_id
            # Add all directly reachable points to the same cluster
            for j in range(i + 1, len(ordered_reachability)):
                if ordered_reachability[j] <= reachability_distance_at_elbow:
                    labels[ordered_indices[j]] = cluster_id
                else:
                    break
            cluster_id += 1

# Step 4: Plot the clusters based on the new manually set labels
plt.figure(figsize=(10, 7))
unique_labels = set(labels)

# Generate colors for each cluster label
colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))

for klass, color in zip(unique_labels, colors):
    class_member_mask = (labels == klass)
    xy = data[class_member_mask]
    if klass != -1:
        # Draw the convex hull and fill it with a light shade of the cluster color
        if xy.shape[0] > 2:  # ConvexHull needs at least 3 points to compute the hull
            hull = ConvexHull(xy)
            plt.fill(xy[hull.vertices, 0], xy[hull.vertices, 1], color=color, alpha=0.2, edgecolor='k')
        plt.scatter(xy[:, 0], xy[:, 1], color=color, edgecolor='k', label=f'Cluster {klass}')
    else:
        plt.scatter(xy[:, 0], xy[:, 1], c='k', marker='x', label='Noise')

plt.title('Clusters by OPTICS with Manual Threshold and Hulls')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()