font_color = "#8d8f91"
background_color_first_row = "#1a1c23"
background_color_second_row = "#282b38"
grid_color = "#3E3F40"


def update_line_plot(fig):
    """

    :param fig:
    :return:
    """
    fig.update_layout(
        height=250,
        margin={"t": 50, "l": 10, "b": 30, "r": 10},
        font_color=font_color,
        paper_bgcolor=background_color_first_row,
        plot_bgcolor=background_color_first_row,
        legend_title_font_color=font_color,
        title_font_color=font_color,
        title={
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=1,
            tickfont=dict(
                color=font_color,
            ),
            title_font=dict(color=font_color)
        ),
        xaxis=dict(
            showgrid=True,
            # tickangle=45,
            gridcolor=grid_color,
            gridwidth=1,
            title_font=dict(color=font_color),
            tickfont=dict(
                color=font_color)
        )
    )

    fig.update_xaxes(
        ticktext=["2015", "2016", "2017", "2018", "2019", "2020"],
        tickvals=['15-01', '16-01', '17-01', '18-01', '19-01', '20-01'],
    )


def update_pie_plot(fig):
    """

    :param fig:
    :return:
    """
    fig.update_layout(

        showlegend=False,
        autosize=True,
        height=300,
        # width=300,
        margin={"t": 50, "l": 10, "b": 10, "r": 10},
        title={'y': 0.95, 'x': 0.5,
               # 'xanchor': 'center',
               'yanchor': 'top'},
        paper_bgcolor=background_color_first_row,
        plot_bgcolor=background_color_first_row,
        font_color=font_color,
        title_font_color=font_color,
    )

    fig.update_traces(
        # rotation=-180,
        textposition='outside', textinfo='label+percent')
    # fig.add_traces(textposition="inside", textinfo="percent"


def update_map(fig):
    fig.update_layout(
        geo=dict(bgcolor=background_color_second_row),
        paper_bgcolor=background_color_second_row,
        plot_bgcolor=background_color_second_row,
        margin={"t": 0, "l": 0, "b": 0, "r": 0})


def update_heatmap(fig):
    fig.update_layout(

        title={'text': "Female proportion among victims"},
        xaxis={
            # "title_font"=dict(color=font_color),
            # "tickfont"={"color"=font_color},
            "title": '',
            "tickvals": [],  # Display x values with different labels
            'ticktext': []
        },
        yaxis={
            'title': "",
            'showgrid': False,
            'tickvals': [],  # Display x values with different labels
            'ticktext': []
        },
        paper_bgcolor=background_color_second_row,
        plot_bgcolor=background_color_second_row
    )


def update_bar_plot(fig):
    fig.update_layout(
        showlegend=False,
        autosize=True,
        height=300,
        width=380,
        font_color=font_color,
        title_font_color=font_color,
        margin={"t": 50, "l": 10, "b": 10, "r": 10},
        title={'y': 0.95, 'x': 0.5,
               # 'xanchor': 'center',
               'yanchor': 'top'},
        paper_bgcolor=background_color_second_row,
        plot_bgcolor=background_color_second_row)
