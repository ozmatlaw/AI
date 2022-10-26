import matplotlib.pyplot as plt
import numpy as np


def plot_ratio(lst, title, x_axis, y_axis):
    plt.figure()
    plt.plot(lst, '-o', color="black")
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.suptitle(title)
    plt.title("Online / Offline ratio")
    plt.savefig(title + "_ratio.png")
    plt.show()


def plot_graph(online_lst, sjf_lst, fcfs_lst, online, sjf, fcfs):
    """
    A function that receives arrays and total scores of the agents and generates a graph
    """

    plt.figure()
    plt.plot(online_lst)
    plt.plot(sjf_lst)
    plt.plot(fcfs_lst)
    plt.xlabel('time')
    plt.ylabel('score')
    plt.legend(['Online', 'SJF', 'FCFS'])
    plt.suptitle("Results")
    plt.title("Score: online: " + str(online) + "  SJF: " +
              str(sjf) + "  FCFS: " + str(fcfs))
    plt.savefig("results_graph.png")
    plt.show()


def plot_graph_with_offline(online_lst, sjf_lst, fcfs_lst, offline_lst, online, sjf, fcfs, offline):
    """
    Works the same as plot_graph except it receives also information about the offline agent
    """
    plt.figure()
    plt.plot(online_lst)
    plt.plot(sjf_lst)
    plt.plot(fcfs_lst)
    plt.plot(offline_lst)
    plt.xlabel('time')
    plt.ylabel('score')
    plt.legend(['Online', 'SJF', 'FCFS', "Offline"])
    plt.suptitle("Results")
    plt.title("Score: online: " + str(online) + "  SJF: " +
              str(sjf) + "  FCFS: " + str(fcfs), " Offline: " + str(offline))
    plt.savefig("results_graph.png")
    plt.show()

