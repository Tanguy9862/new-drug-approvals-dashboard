import dash
from dash import html, dcc
import dash_mantine_components as dmc

app = dash.Dash(__name__, title="New Drug Approvals")

app.layout = html.Div(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Title('Drug Approvals: Annual Overview and Trends', order=2),
                    ],
                    md=11,
                    mt=75,
                    offsetMd=1
                )
            ],
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
