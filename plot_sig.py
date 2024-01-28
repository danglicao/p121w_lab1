import matplotlib.pyplot as plt
import os
import json
import matplotlib.pyplot as plt

def main()->None:
    with open('C:/uci/p121w/lab1/deltas.json', 'r') as f:
        data = json.load(f)

    # Convert keys to integers and get the second element from each value list
    x_values = [int(key) for key in data.keys()]
    y_values = [value[1] for value in data.values()]

    # Create the plot
    plt.plot(x_values, y_values)

    # Optionally, you can set the title and labels for the plot
    plt.title('Significance vs. Mass')
    plt.xlabel('Mass')
    plt.ylabel('Significance')

    plt.savefig('significance vs mass.png')
    plt.close()



if __name__ == '__main__':
    main()

# import matplotlib.pyplot as plt
# import os
# import json
# import matplotlib.pyplot as plt
# from scipy.interpolate import make_interp_spline, BSpline
# import numpy as np
#
# def main()->None:
#     with open('C:/uci/p121w/lab1/deltas.json', 'r') as f:
#         data = json.load(f)
#
#     # Convert keys to integers and get the second element from each value list
#     x_values = [int(key) for key in data.keys()]
#     y_values = [value[1] for value in data.values()]
#
#     # Define a new set of x values to create a smooth curve
#     xnew = np.linspace(min(x_values), max(x_values), 500)
#
#     # Create a BSpline object
#     spl = make_interp_spline(x_values, y_values, k=3)
#     y_smooth = spl(xnew)
#
#     # Create the plot
#     plt.plot(xnew, y_smooth)
#
#     # Optionally, you can set the title and labels for the plot
#     plt.title('Significance vs. Mass')
#     plt.xlabel('Mass')
#     plt.ylabel('Significance')
#
#     # Display the plot
#     plt.savefig('significance vs mass curve.png')
#     plt.close()
#
# if __name__ == '__main__':
#     main()