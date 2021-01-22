import dash_core_components as dcc
import dash_html_components as html
import dash

from app import app
from layout import overview, page2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/shooting/overview':
        return overview
    elif pathname == '/shooting/get_data':
        return page2
    else:
        return overview  # This is the "home page"


if __name__ == '__main__':
    app.run_server(debug=True)
