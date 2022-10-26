from GUI import *
from agents import *
from constants import *
from results_graph import *


def run_all(online):
    """
    Runs all agents on the same orders and displays them on a graph
    :return: array of scores of each agent at specific time
    """
    online_final_score, pre, online_scores_arr, online_moves = online.run()

    sjf = OnlineSimulator(SJFSearchAgent(), pre_orders=pre)
    sjf_final_score, p1, sjf_scores_arr, sjf_moves = sjf.run()

    fcfs = OnlineSimulator(FCFSSearchAgent(), pre_orders=p1)
    fcfs_final_score, p2, fcfs_scores_arr, fcfs_moves = fcfs.run()

    print("online: ", online_scores_arr)
    print("SJF: ", sjf_scores_arr)
    print("FCFS: ", fcfs_scores_arr)

    plot_graph(online_scores_arr, sjf_scores_arr, fcfs_scores_arr, online_final_score,
               sjf_final_score, fcfs_final_score)
    return [online_final_score, sjf_final_score, fcfs_final_score]


def run_all_with_offline(online):
    """
    Same as run_all but with offline agent too.
    """

    online_final_score, pre, online_scores_arr, online_moves = online.run()

    sjf = OnlineSimulator(SJFSearchAgent(), pre_orders=pre)
    sjf_final_score, p1, sjf_scores_arr, sjf_moves = sjf.run()

    fcfs = OnlineSimulator(FCFSSearchAgent(), pre_orders=p1)
    fcfs_final_score, p2, fcfs_scores_arr, fcfs_moves = fcfs.run()

    offline = run_Json("log.json")
    offline_final_score, p3, offline_moves, offline_moves = offline.run_offline()

    return [online_final_score, sjf_final_score, fcfs_final_score, offline_final_score]


def run_and_compare():
    """
    Function that counts the wins of each agent on the same orders and compare between them
    """

    online_count = 0
    sjf_count = 0
    fcfs_count = 0

    for i in range(NUM_OF_RUNS):
        online = run_generate()
        arr = run_all(online)
        max_score = max(arr)
        if arr[0] == max_score:
            online_count += 1
        if arr[1] == max_score:
            sjf_count += 1
        if arr[2] == max_score:
            fcfs_count += 1


if __name__ == '__main__':

    if len(sys.argv) > 3 or len(sys.argv) < 2:
        sys.stderr.write("INVALID ARGUMENT\n")
        exit(1)

    if len(sys.argv) == 2 and sys.argv[1] in {"GENERATE", "APP"}:
        if sys.argv[1] == "GENERATE":
            online = run_generate()
        else:
            online = run_Gui()
        run_all(online)

    elif len(sys.argv) == 3 and sys.argv[1] == "JSON":
        online = run_Json(sys.argv[2])
        run_all(online)

    else:
        sys.stderr.write("INVALID ARGUMENT\n")
        exit(1)
