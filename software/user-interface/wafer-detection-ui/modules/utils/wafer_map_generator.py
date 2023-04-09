import numpy as np
import matplotlib.pyplot as plt
from data.wfdata import load_data


def generate_wafer_map():


    # set the resolution of the wafer map
    resolution = (100, 100)

    df = load_data()

    # Drop all empty lines from dataset
    df = df.dropna(how='all')
    print(df.head())

    second_row_values = df.iloc[0].values
    x_range = second_row_values[0]
    y_range = second_row_values[1]


    # Skip first 2 lines from data
    df = df.iloc[2:]
    # print(df.head())

    # print(df.all())
    # df_array = df.values
    defect_coords = df.values

    # covert the coordinates to float from string (iLoc converted floats to strings)
    defect_coords = defect_coords[:, :2].astype(np.float32)

    # define the center and radius of the circle boundary
    center = (float(x_range)/2, float(y_range)/2)
    radius = float(x_range)/2

    # create a 2D grid of coordinates
    x, y = np.meshgrid(np.linspace(
        0, 100, resolution[0]), np.linspace(0, 100, resolution[1]))

    # create a boolean mask for the circle boundary
    mask = (x - center[0])**2 + (y - center[1])**2 <= radius**2

    # create a 2D histogram of defect coordinates within the circle boundary
    heatmap, xedges, yedges = np.histogram2d(
        defect_coords[:, 0], defect_coords[:, 1], bins=resolution, range=[[0, 100], [0, 100]], density=True)
    heatmap[~mask] = np.nan  # set values outside the circle boundary to NaN

    # plot the wafer map with defects inside the circle boundary
    fig, ax = plt.subplots(figsize=(8, 8))
    # create a green circle heatmap
    im = ax.imshow(heatmap.T, extent=[
                xedges[0], xedges[-1], yedges[0], yedges[-1]], cmap='Reds')
    # set the colorbar range to the max value within the circle boundary
    im.set_clim(0, np.nanmax(heatmap))
    im.set_alpha(0.5)  # set the heatmap transparency to 0.5
    ax.scatter(defect_coords[:, 0], defect_coords[:, 1], color='red', s=10)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_title('Wafer Map with Defects')

    # create a circle patch for the boundary
    circle = plt.Circle(center, radius, edgecolor='black', facecolor='none', lw=2)
    ax.add_patch(circle)

    # add a colorbar for the circle heatmap
    # cbar = plt.colorbar(im)
    # cbar.set_label('Defect Density')

    #show figure to zoom in 
    plt.show()   
    return fig