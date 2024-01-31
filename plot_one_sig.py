import os
import numpy as np
from data_process import *
import params
import time
import json
import concurrent.futures
from collections import OrderedDict
from matplotlib import pyplot as plt


def calculate_significance(entry, delta_m, signal, background, signal_weight, background_weight):
    _, _, significance = window.calculate_significance_for_params(
        entry, delta_m, signal, background, signal_weight, background_weight
    )
    return delta_m, significance

def calculate_max_significance(entry, data_path, signal_weight, background_weight):
    signal_file = os.path.join(data_path, str(entry), f'{entry}_signal.csv')
    background_file = os.path.join(data_path, str(entry), f'{entry}_background.csv')
    signal = fig_process.read_csv(signal_file)
    background = fig_process.read_csv(background_file)

    sig = []

    # 创建一个进程池
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(calculate_significance, entry, delta_m, signal, background, signal_weight, background_weight)
                   for delta_m in np.arange(1, 50.01, 0.01)]  # 从1到50，步长为0.1

        for future in concurrent.futures.as_completed(futures):
            sig.append(future.result())

    return sig

def plot_sig(entry, sig):
    x_coords, y_coords = zip(*sig)

    # 对数据进行排序，确保曲线图是按x坐标顺序绘制
    sorted_pairs = sorted(zip(x_coords, y_coords))
    sorted_x, sorted_y = zip(*sorted_pairs)

    # 创建曲线图
    plt.plot(sorted_x, sorted_y)

    # 可以添加标题和轴标签
    plt.title('Significance vs. Delta M for ' + str(entry) + ' GeV')
    plt.xlabel('Delta M')
    plt.ylabel('Significance')
    plt.savefig(f'Significance vs. Delta M for {str(entry)} GeV.png')
    plt.close()

def main() -> None:
    data_path = 'C:/uci/p121w/lab1/database'
    # entries = os.listdir(data_path)
    # entries_int = [int(entry) for entry in entries]
    # entries_int.sort()
    enter = 200
    signal_weight = params.signal_weight[enter]
    background_weight = params.background_weight
    sig = calculate_max_significance(enter, data_path, signal_weight, background_weight)
    print(sig)
    plot_sig(enter, sig)



if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")



