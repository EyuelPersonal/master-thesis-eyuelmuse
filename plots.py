from matplotlib import pyplot as plt
import numpy as np

def compare_histograms(scores1:np.ndarray,
                       scores2:np.ndarray,
                       title:str,
                       label1:str = None,
                       label2:str = None) -> None:
    plt.figure(figsize=(7,5))
    plt.hist(scores1, histtype='step', label=label1, density=True, color='red')
    plt.hist(scores2, histtype='step', label=label2, density=True, color='blue')
    plt.ylabel('Probability')
    plt.xlabel(title)
    plt.legend(loc='upper right')
    plt.show()

def plot_histograms(scores1:np.ndarray,
                    title:str,
                    label1:str = None) -> None:
    plt.figure(figsize=(7,5))
    plt.hist(scores1, histtype='step', label=label1, density=True, color='red')
    plt.ylabel('Probability')
    plt.xlabel(title)
    plt.show()

def degree_plots(degree_sequence:list) -> None:
    fig = plt.figure("Degree of a random graph", figsize=(15, 10))
    axgrid = fig.add_gridspec(5, 4)
    ax1 = fig.add_subplot(axgrid[3:, :2])
    x = list(np.arange(0, len(degree_sequence), 1))
    ax1.scatter(x, degree_sequence, s=None, marker="o", color='red')
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")
    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.hist(degree_sequence, histtype='step', density=True, color='red')
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("Probability")

    fig.tight_layout()
    plt.show()

def log_log_plot(degree_sequence:list) -> None:
    fig = plt.figure("Degree of a random graph", figsize=(10, 10))
    axgrid = fig.add_gridspec(5, 4)
    ax1 = fig.add_subplot(axgrid[3:, :2])
    x_in = np.unique(np.log(degree_sequence), return_counts=False)
    y_in = np.log(np.unique(np.log(degree_sequence), return_counts=True)[1])
    ax1.scatter(x_in, y_in, color='red')
    ax1.set_title("log-log scale degree")
    ax1.set_ylabel("log count")
    ax1.set_xlabel("log degree")


def compare_log_log_plots(degree_sequence_1:list, 
                          degree_sequence_2:list,
                          label1:str = 'Network',
                          label2:str = 'Model') -> None:
    fig = plt.figure("Degree of a random graph", figsize=(10, 10))
    axgrid = fig.add_gridspec(5, 4)
    ax1 = fig.add_subplot(axgrid[3:, :2])
    x_in_1 = np.unique(np.log(degree_sequence_1), return_counts=False)
    y_in_1 = np.log(np.unique(np.log(degree_sequence_1), return_counts=True)[1])
    x_in_2 = np.unique(np.log(degree_sequence_2), return_counts=False)
    y_in_2 = np.log(np.unique(np.log(degree_sequence_2), return_counts=True)[1])
    ax1.scatter(x_in_1, y_in_1, color='red')
    ax1.scatter(x_in_2, y_in_2, color='blue')
    ax1.legend([label1, label2], loc='upper right', fontsize='x-large')
    ax1.set_ylabel('log count')
    ax1.set_xlabel('log degree')

def line_plot(data, title, xlabel, ylabel):
    plt.plot(data,
            label='title', 
            color='red', 
            linestyle='dashed',
            marker='o',
            markerfacecolor='blue',
            markersize=5,
            linewidth=2,
            alpha=0.7
            )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()