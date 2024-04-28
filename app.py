import dash
from dash import html


app = dash.Dash(
    __name__,
    title='New Drug Approvals',
    external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap',
        'https://fonts.googleapis.com/css2?family=Anek+Devanagari:wght@100..800&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap'
    ],
    use_pages=True,
    update_title=None,
    suppress_callback_exceptions=True
)

app.layout = html.Div(
    [
        dash.page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=True)