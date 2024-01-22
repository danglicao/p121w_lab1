import math
import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
import time
def read_data(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        i = 0
        data = []
        while i < len(lines):
            if lines[i].strip() == 'NumElectrons: 2':
                i += 1
                row_data1 = lines[i].strip().split()
                i += 1
                row_data2 = lines[i].strip().split()
                electron1 = {'pt':float(row_data1[3]),'eta':float(row_data1[5]), 'phi':float(row_data1[7]), 'charge':float(row_data1[9])}
                electron2 = {'pt':float(row_data2[3]),'eta':float(row_data2[5]), 'phi':float(row_data2[7]), 'charge':float(row_data2[9])}
                if electron1['charge'] + electron2['charge'] == 0:
                    event = (electron1, electron2)
                    data.append(event)
                i += 1
            else:
                i += 1
    return data

def norm_pt(electron):
    pt, eta, phi = electron['pt'], electron['eta'], electron['phi']
    ptx = pt * math.cos(phi)
    pty = pt * math.sin(phi)
    ptz = pt * math.sinh(eta)
    norm_pt = math.sqrt(ptx**2 + pty**2 + ptz**2)
    return norm_pt, ptx, pty, ptz

def total_E(P,m):
    return math.sqrt(P**2 + m**2)

def inv_mass(electron1, electron2,mass):
    norm_pt1, ptx1, pty1, ptz1 = norm_pt(electron1)
    norm_pt2, ptx2, pty2, ptz2 = norm_pt(electron2)
    E1 = total_E(norm_pt1, mass)
    E2 = total_E(norm_pt2, mass)
    return math.sqrt((E1+E2)**2 - (ptx1+ptx2)**2 - (pty1+pty2)**2 - (ptz1+ptz2)**2)

# def calculate_significance_for_delta_M(delta_M, mass_signal, mass_background, signal_weight, background_weight, HypothesisMz):
#     # 选择落在窗口内的数据点
#     window_mask_signal = (mass_signal >= (HypothesisMz - delta_M)) & (mass_signal <= (HypothesisMz + delta_M))
#     window_mask_background = (mass_background >= (HypothesisMz - delta_M)) & (mass_background <= (HypothesisMz + delta_M))
#
#     # 计算窗口内的加权信号和背景总数
#     signal_in_window = np.sum(np.array(mass_signal)[window_mask_signal]) * signal_weight
#     background_in_window = np.sum(np.array(mass_background)[window_mask_background]) * background_weight
#
#     # 计算显著性
#     significance = signal_in_window / np.sqrt(background_in_window + 1e-6)
#     return delta_M, significance

def calculate_significance_for_params(hypothesis_mz, delta_m, mass_signal, mass_background, signal_weight, background_weight):
    # 选择落在窗口内的数据点
    window_mask_signal = (mass_signal >= (hypothesis_mz - delta_m)) & (mass_signal <= (hypothesis_mz + delta_m))
    window_mask_background = (mass_background >= (hypothesis_mz - delta_m)) & (mass_background <= (hypothesis_mz + delta_m))

    # 计算窗口内的加权信号和背景总数
    signal_in_window = np.sum(np.array(mass_signal)[window_mask_signal]) * signal_weight
    background_in_window = np.sum(np.array(mass_background)[window_mask_background]) * background_weight

    # 计算显著性
    significance = signal_in_window / np.sqrt(background_in_window + 1e-6)
    return hypothesis_mz, delta_m, significance


def main()->None:
    start_time = time.time()
    signal_weight = 0.75
    background_weight = 2.0
    Me = 0.511 * 1e-3  # GeV
    hypothesis_mass = 750  # GeV
    hypothesis_mz_values = np.linspace(300, 820, 1)
    background = read_data('p121_lab1_data/ee_mll650_electrons.txt')
    signal = read_data('p121_lab1_data/zp_mzp750_electrons.txt')
    mass_background = []
    mass_signal = []
    for event_background in background:
        mass_background.append(inv_mass(event_background[0], event_background[1], Me))
    for event_signal in signal:
        mass_signal.append(inv_mass(event_signal[0], event_signal[1], Me))
    # mass_signal_array = np.array(mass_signal)
    # mass_background_array = np.array(mass_background)
    # print(len(mass_background), len(mass_signal))
    # deltas = np.arange(10, 200, 0.1)
    # results = []
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(statistical_significance, delta, mass_signal_array,
    #                         mass_background_array,
    #                         hypothesis_mass) for delta in deltas]
    #     for future in concurrent.futures.as_completed(futures):
    #         results.append(future.result())
    # max_result = max(results, key = lambda x: x[1])
    # print(max_result)
    mass_total = mass_background+mass_signal
    weight2 = [background_weight]*len(mass_background)+[signal_weight]*len(mass_signal)

    # sig_set = []
    # for delta in range(10,200,1):
    #     de, significance = statistical_significance(delta, mass_signal_array, mass_background_array, hypothesis_mass)
    #     sig_set.append(significance)
    # plt.plot()
    delta_M_values = np.arange(1, 200, 0.1)

    significance_results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 创建所有可能的参数组合的并行任务
        futures = [
            executor.submit(calculate_significance_for_params, hypothesis_mz, delta_m, mass_signal,
                            mass_background, signal_weight, background_weight)
            for hypothesis_mz in hypothesis_mz_values
            for delta_m in delta_M_values]

        # 处理结果
        for future in concurrent.futures.as_completed(futures):
            significance_results.append(future.result())

    # 找到最大显著性和对应的参数
    best_hypothesis_mz, best_delta_m, max_significance = max(significance_results,
                                                             key = lambda x: x[2])

    # 输出最佳 HypothesisMz、delta M 和对应的显著性
    print("Best HypothesisMz:", best_hypothesis_mz)
    print("Best delta M:", best_delta_m)
    print("Maximum significance:", max_significance)
    # plt.hist(mass_total, bins = 50, range = mass_window, weights = weight2, label = 'signal')
    # plt.hist(mass_background, bins = 50, range = mass_window,
    #          weights = [background_weight] * len(mass_background), label = 'background')
    # plt.show()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    print(min(mass_signal))
if __name__ == '__main__':
    main()