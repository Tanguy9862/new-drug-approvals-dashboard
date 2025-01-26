import logging
import dash
import pandas as pd
from datetime import datetime
from typing import Any

from dash import dcc, html, callback, Input, Output
from utils.loading_data import load_data
from config import CONFIG

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logging.info(f"Environment chosen: {CONFIG.ENV}")


app = dash.Dash(
    __name__,
    title='Pharmaceutical Drug Approvals Dashboard',
    meta_tags=[
        {
            'name': 'description',
            'content': 'Explore comprehensive visualizations of global drug approval data. This dashboard offers '
                       'interactive analysis tools to delve into drug approvals by category, company, and treatment '
                       'types, using data sourced from recognized global health databases.'
        },
        {
            'name': 'keywords',
            'content': 'drug approvals, pharmaceuticals, healthcare data, interactive dashboard, data visualization, '
                       'global health, drug categories, treatment types'
        }
    ],
    external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap',
        'https://fonts.googleapis.com/css2?family=Anek+Devanagari:wght@100..800&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap'
    ],
    use_pages=True,
    update_title=None,
    suppress_callback_exceptions=True
)

server = app.server

app.layout = html.Div(
    [
        dcc.Store(id='drug-approvals-last-update'),
        dash.page_container
    ]
)


@callback(
    Output('drug-approvals-data', 'data'),
    Output('drug-approvals-last-update', 'data'),
    Output('year-input', 'min'),
    Output('year-input', 'max'),
    Output('year-input', 'value'),
    Input('drug-approvals-data', 'input')
)
def load_drug_approvals_data(_: Any) -> tuple[list[dict], Any]:
    """
    Loads drug approvals data from Google Cloud Storage (GCS) or locally if GCS is unreachable,
    processes the data to extract the year of approval, and provides boundary years for inputs.

    Args:
    _: This is a placeholder for the input argument which is not used in the function.

    Returns:
    Tuple containing:
        - List of dictionaries representing the drug approvals data for storing in a dcc.Store.
        - Minimum year of approval for setting the range of a year input slider.
        - Maximum year of approval for setting the range of a year input slider.
        - Current year for setting the default value of a year input slider.
    """
    df, last_update = load_data('NEW_DRUG_APPROVALS_FILENAME', 'csv')

    df['Date of Approval'] = pd.to_datetime(df['Date of Approval'], errors='coerce')
    df['year'] = df['Date of Approval'].dt.year

    year_boundaries = [
        df['year'].min(),
        df['year'].max(),
        datetime.now().year
    ]

    return df.to_dict('records'), last_update, *year_boundaries


if __name__ == "__main__":
    app.run(debug=True)

