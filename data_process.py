import numpy as np
import math

class data_process:
    # def __init__(self, file_path, mass, electron):
    #     self.file_path = file_path
    #     self.mass = mass
    #     self.electron = electron
    @staticmethod
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

    @staticmethod
    def norm_pt(electron):
        pt, eta, phi = electron['pt'], electron['eta'], electron['phi']
        ptx = pt * math.cos(phi)
        pty = pt * math.sin(phi)
        ptz = pt * math.sinh(eta)
        norm_pt = math.sqrt(ptx**2 + pty**2 + ptz**2)
        return norm_pt, ptx, pty, ptz

    @staticmethod
    def total_E(P,m):
        return math.sqrt(P**2 + m**2)

    @staticmethod
    def inv_mass(electron1, electron2, mass):
        norm_pt1, ptx1, pty1, ptz1 = data_process.norm_pt(electron1)
        norm_pt2, ptx2, pty2, ptz2 = data_process.norm_pt(electron2)
        E1 = data_process.total_E(norm_pt1, mass)
        E2 = data_process.total_E(norm_pt2, mass)
        return math.sqrt((E1 + E2)**2 - (ptx1 + ptx2)**2 - (pty1 + pty2)**2 - (ptz1 + ptz2)**2)

class fig_process:
    @staticmethod
    def read_csv(file_path):
        with open(file_path) as f:
            lines = f.readlines()
            data = []
            for line in lines:
                data.append(float(line.strip()))
        return data

class window:
    @staticmethod
    def calculate_significance_for_params(hypothesis_mz, delta_m, mass_signal, mass_background,
                                          signal_weight, background_weight):
        # 选择落在窗口内的数据点
        window_mask_signal = (mass_signal >= (hypothesis_mz - delta_m)) & (
                    mass_signal <= (hypothesis_mz + delta_m))
        window_mask_background = (mass_background >= (hypothesis_mz - delta_m)) & (
                    mass_background <= (hypothesis_mz + delta_m))

        # 计算窗口内的加权信号和背景总数
        signal_in_window = np.sum(np.array(mass_signal)[window_mask_signal]) * signal_weight
        background_in_window = np.sum(
            np.array(mass_background)[window_mask_background]) * background_weight

        # 计算显著性
        significance = signal_in_window / np.sqrt(background_in_window + 1e-6)
        return hypothesis_mz, delta_m, significance


