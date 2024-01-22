import os
import csv
from data_process import *
from params import *

def main():
    folder_path = 'C:/uci/p121w/p121_lab1_data'
    database_dir = 'C:/uci/p121w/database'  # 指定的数据库目录
    file_list = os.listdir(folder_path)

    # 过滤掉不需要的文件
    signal_files = [f for f in file_list if f.startswith('zp') and f.endswith('.txt')]
    background_files = [f for f in file_list if f.startswith('ee') and f.endswith('.txt')]

    # 处理信号文件
    for signal_file in signal_files:
        mass_signal = []
        energy_level = get_energy_level(signal_file)  # 提取文件名中的能量等级
        signal_data = data_process.read_data(os.path.join(folder_path, signal_file))  # 提取信号数据
        # print(signal_data)
        for event_signal in signal_data:
            mass_signal.append(data_process.inv_mass(event_signal[0], event_signal[1], Me))

        # 创建文件夹和CSV文件
        signal_folder = os.path.join(database_dir, str(energy_level))
        os.makedirs(signal_folder, exist_ok=True)
        print(mass_signal)
        with open(os.path.join(signal_folder, f'{energy_level}_signal.csv'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for mass in mass_signal:
                writer.writerow([mass])

    # 处理背景文件
    for background_file in background_files:
        mass_background = []
        background_level = get_energy_level(background_file)
        corresponding_signal_level = find_closest_signal_level(background_level, signal_files)
        background_data = data_process.read_data(os.path.join(folder_path, background_file))
        for event_background in background_data:
            mass_background.append(data_process.inv_mass(event_background[0], event_background[1], Me))

        # 将数据写入对应的CSV文件
        with open(os.path.join(database_dir, str(corresponding_signal_level), f'{corresponding_signal_level}_background.csv'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for mass in mass_background:
                writer.writerow([mass])

def get_energy_level(filename):

    parts = filename.split('_')
    if len(parts) > 1:
        # 提取能量等级（数字部分）
        energy_level = ''.join(filter(str.isdigit, parts[1]))
        return int(energy_level)
    else:
        return None

def find_closest_signal_level(background_level, signal_files):
    signal_levels = sorted([get_energy_level(f) for f in signal_files])
    for level in signal_levels:
        if level > background_level:
            return level
    return None


if __name__ == "__main__":
    main()
