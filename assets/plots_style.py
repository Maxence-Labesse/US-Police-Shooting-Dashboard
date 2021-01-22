font_color = "#8d8f91"
background_color = "#21252C"
grid_color = "#3E3F40"


def update_line_plot(fig):
    """

    :param fig:
    :return:
    """
    fig.update_layout(
        autosize=True,
        height=375,
        margin={"t": 0, "l": 0, "b": 0, "r": 0, "pad": 10},
        paper_bgcolor=background_color,
        plot_bgcolor=background_color,
        legend_title_font_color=font_color,
        title_font_color=font_color,
        font_color=font_color,
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
            title_font=dict(color=font_color),
            showgrid=True,
            # tickangle=45,
            gridcolor=grid_color,
            gridwidth=1,
            tickfont=dict(
                color=font_color)
        )
    )

    fig.update_xaxes(
        ticktext=["2015", "2016", "2017", "2018", "2019", "2020"],
        tickvals=[1501, 1601, 1701, 1801, 1901, 2001],
    )


def update_pie_plot(fig):
    """

    :param fig:
    :return:
    """
    fig.update_layout(
        showlegend=False,
        autosize=True,
        height=375,
        width=375,
        font_color=font_color,
        title_font_color=font_color,
        # margin={"t": 0, "l": 0, "b": 0, "r": 0, "pad": 10},
        paper_bgcolor=background_color,
        plot_bgcolor=background_color)

    fig.update_traces(
        # rotation=-180,
        textposition='inside', textinfo='label+percent')
    # fig.add_traces(textposition="inside", textinfo="percent")


def update_bar_plot(fig):
    fig.update_layout(
        showlegend=False,
        autosize=True,
        height=375,
        width=375,
        font_color=font_color,
        title_font_color=font_color,
        # margin={"t": 0, "l": 0, "b": 0, "r": 0, "pad": 10},
        paper_bgcolor=background_color,
        plot_bgcolor=background_color)
