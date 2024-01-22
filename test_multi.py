import concurrent.futures
import numpy as np
import os
from data_process import *
from params import *
import time
import json
import concurrent.futures
from collections import OrderedDict


def calculate_significance_range(entry, delta_m_range, signal, background, signal_weight, background_weight):
    max_significance = 0
    best_delta_m = None

    for delta_m in delta_m_range:
        _, _, significance = window.calculate_significance_for_params(
            entry, delta_m, signal, background,
            signal_weight[entry], background_weight
        )

        if significance > max_significance:
            max_significance = significance
            best_delta_m = delta_m

    return best_delta_m, max_significance

def calculate_max_significance(entry, data_path, signal_weight, background_weight):
    signal_file = os.path.join(data_path, str(entry), f'{entry}_signal.csv')
    background_file = os.path.join(data_path, str(entry), f'{entry}_background.csv')
    signal = fig_process.read_csv(signal_file)
    background = fig_process.read_csv(background_file)

    # 确定线程数和每个线程处理的delta_m范围
    thread_count = 20  # 假设使用10个线程
    delta_m_values = np.arange(1, 50.01, 0.01)
    delta_m_ranges = np.array_split(delta_m_values, thread_count)

    # 使用多线程
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(calculate_significance_range, entry, delta_m_range, signal, background, signal_weight, background_weight) for delta_m_range in delta_m_ranges]

        max_significance = 0
        best_delta_m = None

        for future in concurrent.futures.as_completed(futures):
            delta_m, significance = future.result()
            if significance > max_significance:
                max_significance = significance
                best_delta_m = delta_m

    mass_window = (entry - best_delta_m, entry + best_delta_m)
    return entry, best_delta_m, max_significance, mass_window

def main() -> None:
    data_path = 'C:/uci/p121w/database'
    entries = os.listdir(data_path)
    entries_int = [int(entry) for entry in entries]
    entries_int.sort()

    deltas = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for entry in entries_int:
            futures.append(
                executor.submit(calculate_max_significance, entry, data_path, signal_weight,
                                background_weight))

        for future in concurrent.futures.as_completed(futures):
            entry, best_delta_m, max_significance, mass_window = future.result()
            print("最大显著性:", max_significance)
            print("对应的delta_m:", best_delta_m)
            print("mass窗口:", mass_window)
            deltas[entry] = (best_delta_m, max_significance, mass_window)
    sorted_data = OrderedDict(sorted(deltas.items(), key=lambda x: int(x[0])))

    with open('C:/uci/p121w/test_multi.json', 'w') as f:
        json.dump(sorted_data, f, indent = 4)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

