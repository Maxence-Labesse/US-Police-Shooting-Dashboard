import numpy as np
from assets.plots_style import *
import plotly.graph_objs as go

font_color = "#8d8f91"
background_color = "#21252C"
grid_color = "#3E3F40"
corporate_cols = ["#badad4", "#395155"]

corporate_layout = go.Layout(
    # title=corporate_title,
    title_x=0.5,  # Align chart title to center
    title_font_color=font_color,
    xaxis={'zeroline': False},
    yaxis={'zeroline': False},
    height=300,
    width=480,
    legend={
        'orientation': 'h',
        'yanchor': 'top',
        'y': 1.01,
        'xanchor': 'left',
        'x': 1.05,
        'font': {'size': 9, 'color': font_color}
    },
    margin={'l': 5, 'r': 15, 't': 45, 'b': 15}
)


def get_heatmap(df, col):
    df_gender = df[col].value_counts(-1)
    df_gender.sort_values(inplace=True, ascending=True)

    # heatmap dimensions
    heatmap_width = 10
    heatmap_height = 10

    # total number of tiles
    total_num_tiles = heatmap_width * heatmap_height  # total number of tiles
    # Per category
    tiles_per_category = [round(proportion * total_num_tiles) for proportion in df_gender]

    # Create the matrix that will be fitted to the heatmap
    waffle_chart = np.zeros((heatmap_height, heatmap_width))

    # Fill the tiles
    category_index = 0
    tile_index = 0

    for col in range(heatmap_width):
        for row in range(heatmap_height):
            tile_index += 1

            # if the number of tiles populated for the current category is equal to its corresponding allocated tiles...
            if tile_index > sum(tiles_per_category[0:category_index]):
                # ...proceed to the next category
                category_index += 1

                # set the class value to an integer, which increases with class
            waffle_chart[row, col] = category_index

    # Figure
    data = go.Heatmap(z=waffle_chart, colorscale=corporate_cols,
                      showscale=False,
                      xgap=1,
                      ygap=1)

    fig = go.Figure(data=data, layout=corporate_layout)

    return fig



