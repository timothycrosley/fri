import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram

# Get three colors for each relevance type
color_palette_3 = sns.color_palette(palette="muted", n_colors=3)


def plotIntervals(ranges, ticklabels=None, invert=False, classes=None):
    # Figure Parameters
    fig = plt.figure(figsize=(13, 6))
    ax = fig.add_subplot(111)
    N = len(ranges)

    # Ticklabels
    if ticklabels is None:
        ticks = np.arange(N) + 1
    else:
        ticks = list(ticklabels)
        for i in range(N):
            ticks[i] += " - {}".format(i + 1)
    # Interval sizes
    ind = np.arange(N) + 1
    width = 0.6
    upper_vals = ranges[:, 1]
    lower_vals = ranges[:, 0]
    height = upper_vals - lower_vals
    # Minimal height to make very small intervals visible
    height[height < 0.001] =  0.001

    # Bar colors
    if classes is None:
        classes = np.zeros(N)
    color = [color_palette_3[c] for c in classes]

    # Plot the bars
    bars = ax.bar(ind, height, width, bottom=lower_vals, tick_label=ticks, align="center", edgecolor="none",
                  linewidth=1.3, color=color)

    plt.xticks(ind, ticks, rotation='vertical')
    # Limit the y range to 0,1 or 0,L1
    ax.set_ylim([0, 1])

    plt.ylabel('relevance', fontsize=19)
    plt.xlabel('feature', fontsize=19)

    relevance_classes = ["Irrelevant", "Weakly relevant", "Strongly relevant"]
    patches = []
    for i, rc in enumerate(relevance_classes):
        patch = mpatches.Patch(color=color_palette_3[i], label=rc)
        patches.append(patch)

    plt.legend(handles=patches)
    # Invert the xaxis for cases in which the comparison with other tools
    if invert:
        plt.gca().invert_xaxis()
    return fig


def plot_dendrogram_and_intervals(intervals, linkage, threshold=0.55, figsize=(13, 7), ticklabels=None, **kwargs):
    import matplotlib.pyplot as plt

    z = linkage
    fig = plt.figure(figsize=figsize)

    # Top dendrogram plot
    ax2 = fig.add_subplot(211)
    d = dendrogram(
        z,
        color_threshold=threshold,
        leaf_rotation=0.,  # rotates the x axis labels
        leaf_font_size=12.,  # font size for the x axis labels
        ax=ax2,
        **kwargs
    )
    # Get index determined through linkage method and dendrogram
    rearranged_index = d['leaves']
    ranges = intervals[rearranged_index]

    ax = fig.add_subplot(212)
    N = len(ranges)
    if ticklabels is None:
        ticks = np.array(rearranged_index)
        ticks += 1  # Index starting at 1
    else:
        ticks = list(ticklabels[rearranged_index])
        for i in range(N):
            ticks[i] += " - {}".format(rearranged_index[i] + 1)

    ind = np.arange(N) + 1
    width = 0.6
    upper_vals = ranges[:, 1]
    lower_vals = ranges[:, 0]
    bars = ax.bar(ind, upper_vals - lower_vals, width, bottom=lower_vals, tick_label=ticks, align="center",
                  linewidth=1.3)

    plt.ylabel('relevance', fontsize=19)
    plt.xlabel('feature', fontsize=19)
    plt.xticks(ind, ticks, rotation='30', ha="right")
    ax.margins(x=0)
    ax2.set_xticks([])
    ax2.margins(x=0)
    plt.tight_layout()
    # plt.subplots_adjust(wspace=0, hspace=0)

    return fig
