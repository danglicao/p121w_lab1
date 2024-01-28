import matplotlib.pyplot as plt
import os
from data_process import fig_process
from params import *

def main()->None:
    data_path = 'C:/uci/p121w/lab1/database'
    output_path = 'C:/uci/p121w/lab1/figs'
    entries = os.listdir(data_path)
    entires_int = [int(entry) for entry in entries]
    entires_int.sort()
    for entry in entires_int:
        signal_file = os.path.join(data_path, str(entry), f'{entry}_signal.csv')
        background_file = os.path.join(data_path, str(entry), f'{entry}_background.csv')
        signal = fig_process.read_csv(signal_file)
        background = fig_process.read_csv(background_file)
        mass_total = background + signal
        weight2 = [background_weight] * len(background) + [signal_weight[entry]] * len(signal)
        range = (entry- 40, entry + 80)
        plt.hist(mass_total, bins=50, weights=weight2, range = range, label='signal', color = 'green',edgecolor='white', linewidth = 0.1)
        plt.hist(background, bins = 50, range = range,
                          weights = [background_weight] * len(background), label = 'background', color = 'red',edgecolor='white',linewidth = 0.1)
        plt.xlabel('mass (GeV)')
        plt.ylabel('entries/bin')
        plt.title(f'Invariant Mass Distribution for {entry} GeV')
        plt.legend(loc = 'upper right', title_fontsize = 'large',
                   fontsize = 'medium')

        plt.savefig(os.path.join(output_path, f'{entry}_fig.png'))
        plt.close()
    






if __name__ == '__main__':
    main()