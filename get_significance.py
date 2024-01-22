import os
import math
import numpy as np
from data_process import *
from params import *
import time
import json

def main()->None:
    data_path = 'C:/uci/p121w/database'
    entries = os.listdir(data_path)
    entires_int = [int(entry) for entry in entries]
    entires_int.sort()
    deltas = {}
    for entry in entires_int:
        signal_file = os.path.join(data_path, str(entry), f'{entry}_signal.csv')
        background_file = os.path.join(data_path, str(entry), f'{entry}_background.csv')
        signal = fig_process.read_csv(signal_file)
        background = fig_process.read_csv(background_file)
        # 初始化最大显著性和对应的delta_m
        max_significance = 0
        best_delta_m = None

        # 遍历delta_m的可能值
        for delta_m in np.arange(1, 50.1, 0.1):  # 从1到50，步长为0.1
            _, _, significance = window.calculate_significance_for_params(
                entry, delta_m, signal, background,
                signal_weight[entry], background_weight
            )

            # 更新最大显著性和对应的delta_m
            if significance > max_significance:
                max_significance = significance
                best_delta_m = delta_m
        mass_window = (entry - best_delta_m, entry + best_delta_m)
        print("最大显著性:", max_significance)
        print("对应的delta_m:", best_delta_m)
        print("mass窗口:", mass_window)

        deltas[entry] = (best_delta_m, max_significance, mass_window)
    with open('C:/uci/p121w/deltas.json', 'w') as f:
        json.dump(deltas, f, indent=4)



if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

