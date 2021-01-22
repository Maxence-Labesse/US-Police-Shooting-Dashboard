import dash

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=False,
                meta_tags=[{'name': 'shooting',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
