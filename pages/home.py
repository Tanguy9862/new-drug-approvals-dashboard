import dash
from dash import dcc, html, callback, Input, Output, State, no_update, clientside_callback, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import pandas as pd
from dash_iconify import DashIconify
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.graph_objs as go

from utils.home_utils import (
    drug_approvals_df,
    plot_approvals_year,
    # plot_min_approvals_year,
    plot_drug_type,
    plot_stacked_item_company,
    MIN_YEAR,
    MAX_YEAR,
    CURRENT_YEAR,
    MARGIN_BOTTOM
)

from layouts.home_layout import (
    make_container,
    assemble_kpi_panel,
    make_tooltip_layout
)

from utils.config import (
    FIG_CONFIG,
    KPI_ITEMS as kpi_items,
    SUFFIXES_TO_DELETE
)

dash.register_page(
    __name__,
    path='/',
    order=1,
    title="Overview",
    description="",
    image=""
)

from datetime import datetime
c_time = datetime.utcnow()


layout = html.Div(
    [
        dcc.Store(data=drug_approvals_df.to_dict('records'), id='drug-approvals-data'),
        dcc.Store(data=None, id='filtered-drug-approvals-data'),
        dcc.Store(id='mouse-position'),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Title(
                            'Annual Drug Approval Overview',
                            order=3,
                            align='justify',
                            style={
                                'font-family': 'Roboto, Sans Serif',
                                'font-weight': '300'
                            }

                        )
                    ],
                    offsetMd=1,
                    md=4
                ),
                dmc.Col(
                    [
                        dmc.Group(
                            [
                                dmc.NumberInput(
                                    label=None,
                                    id='year-input',
                                    value=CURRENT_YEAR,
                                    min=MIN_YEAR,
                                    max=MAX_YEAR,
                                    style={"width": 250}
                                )
                            ]
                        )
                    ],
                    md=5
                )
            ],
            mt='md',
            mb=MARGIN_BOTTOM
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Container(
                                            [
                                                dmc.Stack(
                                                    [
                                                        dmc.Text(
                                                            children=[],
                                                            weight=500,
                                                            color='rgba(255,255,255,1)',
                                                            id='total-approvals-count',
                                                            style={
                                                                'font-size': '2.375rem'
                                                            }
                                                        ),
                                                        dmc.Text(
                                                            'approvals',
                                                            transform='uppercase',
                                                            color='white',
                                                            style={
                                                                'font-size': '0.85rem'
                                                            }
                                                        ),
                                                    ],
                                                    spacing=0,
                                                    align='center'
                                                )
                                            ],
                                            px=0,
                                            style={
                                                'background': 'linear-gradient(135deg, #3c8d5d 0%, #c8e6c9 100%)',
                                                # 'border': 'solid 1px #49aa39',
                                                'border-radius': '10px',
                                                'height': '100%',
                                                'position': 'relative'
                                            }
                                        )
                                    ],
                                    md=2
                                ),
                                dmc.Col(
                                    [
                                        make_container(
                                            children=[
                                                dmc.Grid(
                                                    [
                                                        assemble_kpi_panel(item) for item in kpi_items
                                                    ]
                                                )
                                            ],
                                            style_height='75px'
                                        )
                                    ],
                                    md=10
                                )
                            ],
                            mb=MARGIN_BOTTOM
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        make_container(
                                            children=[
                                                dmc.Text(
                                                    children=[
                                                        'Total Approvals'
                                                    ],
                                                    size='sm',
                                                    mb='lg'
                                                ),
                                                dcc.Graph(
                                                    id='yearly-approvals-fig',
                                                    figure={},
                                                    style={'height': '250px', 'width': '95%', 'margin-left': '10px'},
                                                    config=FIG_CONFIG,
                                                    responsive=True
                                                )
                                            ],
                                            style_height='300px'
                                        )
                                    ],
                                    span=8
                                ),
                                dmc.Col(
                                    [
                                        make_container(
                                            children=[
                                                dmc.Text(
                                                    children=[
                                                        'Top 5 Drug Types'
                                                    ],
                                                    size='sm',
                                                    mb='sm',
                                                ),
                                                dcc.Graph(
                                                    id='drug-type-fig',
                                                    config=FIG_CONFIG,
                                                    style={'height': '250px'},
                                                    clear_on_unhover=True,
                                                    responsive=True
                                                ),
                                                dcc.Tooltip(
                                                    id='tooltip-drug-type-fig',
                                                    direction='bottom',
                                                    background_color='rgba(0,0,0,0.9)',
                                                    border_color='rgba(0,0,0,0.9)',
                                                    style={
                                                        'border-radius': '4px',
                                                        'color': 'white',
                                                        'font-family': '"Open Sans", "Verdana", "Arial", sans-serif',
                                                        'font-size': '0.75rem',
                                                        'padding': '0',
                                                        'width': '175px',
                                                        'height': '25px',
                                                        'display': 'flex',
                                                        'flex-direction': 'column',
                                                        'justify-content': 'center'
                                                    },
                                                )
                                            ],
                                            style_height='300px',
                                        )
                                    ],
                                    span=4
                                )
                            ],
                            mb=MARGIN_BOTTOM
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        make_container(
                                            children=[
                                                dmc.Group(
                                                    [
                                                        dmc.Text('Approval Distribution by Category', size='sm'),
                                                        html.Div(
                                                            [
                                                                dmc.Group(
                                                                    [
                                                                        dmc.Select(
                                                                            label=None,
                                                                            placeholder=None,
                                                                            id="item-select",
                                                                            value="disease_type",
                                                                            dropdownPosition='top',
                                                                            data=[
                                                                                {"value": "disease_type",
                                                                                 "label": "Disease"},
                                                                                {"value": "drug_type", "label": "Drug"}
                                                                            ],
                                                                            style={"width": 100},
                                                                        ),
                                                                        dmc.NumberInput(
                                                                            label=None,
                                                                            id='n-companies',
                                                                            value=5,
                                                                            min=5,
                                                                            max=15,
                                                                            style={"width": 60}
                                                                        ),
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    position='apart'
                                                ),
                                                dcc.Graph(
                                                    id='company-stacked-fig',
                                                    config=FIG_CONFIG,
                                                    responsive=True,
                                                    style={'height': '75%', 'margin-top': '30px'}
                                                )
                                            ],
                                            style_height='322px'
                                        )
                                    ],
                                    span='auto'
                                )
                            ]
                        )
                    ],
                    offsetMd=1,
                    md=7
                ),
                dmc.Col(
                    [
                        make_container(
                            children=[
                                dmc.Text('Recent Approvals')
                            ],
                            style_height='85vh'
                        )
                    ],
                    md=3,
                )
            ]
        )
    ]
)


@callback(
    Output('filtered-drug-approvals-data', 'data'),
    Input('year-input', 'value'),
    State('drug-approvals-data', 'data')
)
def update_drug_approvals_data(year: int, data: dict) -> list:
    """
    Filters drug approvals data based on the selected year and converts it to a dictionary suitable for Dash components.

    Args:
        year (int): The year selected by the user.
        data (dict): The original drug approvals data..

    Returns:
        list: A list of dictionaries representing the filtered drug approvals data.
    """

    df = pd.DataFrame(data)
    df_filtered = df.query('year == @year')
    return df_filtered.to_dict('records')


@callback(
    Output('total-approvals-count', 'children'),
    Input('filtered-drug-approvals-data', 'data'),
    State('year-input', 'value'),
    prevent_initial_call=True
)
def update_count_total_approvals(data: dict, year: int) -> int:
    """
    Computes the total number of drug approvals for the selected year and updates the display.

    Args:
        data (dict): The filtered drug approvals data.
        year (int): The year selected by the user.

    Returns:
        int: The total number of drug approvals for the selected year.
    """

    df = pd.DataFrame(data)
    df_filtered = df.query('year == @year')
    return df_filtered.shape[0]


@callback(
    Output('top-company-kpi', 'children'),
    Output('main-focus-kpi', 'children'),
    Output('leading-class-kpi', 'children'),
    Output('last-updated-kpi', 'children'),
    Input('filtered-drug-approvals-data', 'data'),
    prevent_initial_call=True
)
def update_kpi_panel(data):
    df = pd.DataFrame(data)

    all_kpis = []
    for col in ['Company', 'disease_type', 'drug_type']:
        top_item = df.groupby(col).size().reset_index(name='total').sort_values(by='total', ascending=False)
        top_item_name = top_item.iloc[0][col]
        if col == 'disease_type':
            for suffix in SUFFIXES_TO_DELETE:
                if suffix in top_item_name:
                    top_item_name = top_item_name.replace(suffix, '')
                    break
        split_name = top_item_name.split()
        if len(split_name) > 1:
            top_item_name = f'{split_name[0]} {split_name[1][:5]}.'

        all_kpis.append(top_item_name)

    # !!! REMPLACER PAR HEURE RECUPEREE VIA GCS !!!!
    abbreviated_time = c_time.strftime('%y-%m-%d %H:%M')

    return *all_kpis, abbreviated_time


@callback(
    Output('yearly-approvals-fig', 'figure'),
    Input('filtered-drug-approvals-data', 'data'),
    prevent_initial_call=True
)
def update_yearly_approvals_fig(data: dict) -> Figure:
    """
    Callback to update the yearly approvals figure.

    Args:
        data (dict): The data containing drug approvals.

    Returns:
        Figure: Plotly figure of the yearly drug approvals chart.

    """

    # Convert data to DataFrame and parse dates
    df = pd.DataFrame(data)
    df['Date of Approval'] = pd.to_datetime(df['Date of Approval'], errors='coerce')

    # Group data by month and calculate total approvals
    approvals_per_year = df.groupby(df['Date of Approval'].dt.to_period('M')).size().reset_index(name='total')
    approvals_per_year['Date of Approval'] = approvals_per_year['Date of Approval'].dt.to_timestamp()

    return plot_approvals_year(approvals_per_year)


@callback(
    Output('drug-type-fig', 'figure'),
    Input('filtered-drug-approvals-data', 'data'),
    prevent_initial_call=True
)
def update_drug_type_fig(data: dict) -> Figure:
    """
    Callback to update the drug type figure.

    Args:
        data (dict): The data containing drug approvals categorized by drug type.

    Returns:
        Figure: Plotly figure of the top 5 drug types by approval count.
    """

    # Group and count approvals by drug type, then take the top 5
    df = pd.DataFrame(data)
    approvals_per_drug_type = df.groupby('drug_type').size().reset_index(name='total')
    approvals_per_drug_type = approvals_per_drug_type.sort_values(by='total', ascending=False)[:5]

    return plot_drug_type(approvals_per_drug_type)


# Clientside callback to capture and store the mouse position whenever a hover event is triggered on the drug-type
# graph. This function updates the `data` property of a `dcc.Store` component (`mouse-position`) with the current
# mouse coordinates.
clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='update_mouse_position'),
    Output('mouse-position', 'data'),
    Input('drug-type-fig', 'hoverData'),
    prevent_initial_call=True
)


@callback(
    Output('tooltip-drug-type-fig', 'bbox'),
    Input('mouse-position', 'data'),
    prevent_initial_call=True
)
def update_tooltip_bbox(mouse_pos: dict) -> dict:
    """
    Calculates and returns the bounding box for the tooltip based on the mouse position.

    Args:
        mouse_pos (dict): Dictionary containing mouse coordinates ('x' and 'y').

    Returns:
        dict: A dictionary specifying the tooltip's bounding box with keys 'x0', 'y0', 'x1', 'y1'.
    """
    if mouse_pos:
        bbox = {
            "x0": mouse_pos['x'],
            "y0": mouse_pos['y'],
            "x1": mouse_pos['x'],
            "y1": mouse_pos['y'] + 25
        }
        return bbox

    return no_update


@callback(
    Output('tooltip-drug-type-fig', 'show'),
    Output('tooltip-drug-type-fig', 'children'),
    Input('drug-type-fig', 'hoverData'),
    prevent_initial_call=True
)
def update_tooltip_drug_fig(hover_data: dict) -> tuple:
    """
    Updates the tooltip visibility and content based on hover data from the drug-type graph.

    Args:
        hover_data (dict): Dictionary containing hover data from the drug-type graph.

    Returns:
        tuple: A tuple containing a boolean to control the tooltip visibility and a string for the tooltip content.
    """

    if hover_data:
        return True, make_tooltip_layout(hover_data)

    return False, no_update


@callback(
    Output('company-stacked-fig', 'figure'),
    Input('filtered-drug-approvals-data', 'data'),
    Input('item-select', 'value'),
    Input('n-companies', 'value'),
    prevent_initial_call=True
)
def update_stacked_fig(data: dict, item_type: str, n_companies: int) -> Figure:
    """
    Update and return the stacked bar chart figure based on the selected item type and number of companies.
    This function processes the data to create a figure showing the number of approvals per company,
    segmented by drug or disease type, for the top N companies.
    """

    # Convert input data into a DataFrame and group by company and item type to count approvals
    df = pd.DataFrame(data)
    item_per_company = df.groupby(['Company', item_type]).size().reset_index(name='total')

    # Calculate the total number of approvals per company and sort these companies by the total
    # approvals in descending order
    total_approvals_company = item_per_company.groupby('Company')['total'].sum().reset_index(name='total')
    total_approvals_company_sorted = total_approvals_company.sort_values(by=['total', 'Company'], ascending=False)[
                                     :n_companies]

    # Filter the data to include only the top N companies for visualization
    companies_sorted = total_approvals_company_sorted['Company'].to_list()
    item_per_company_filtered = item_per_company[item_per_company['Company'].isin(companies_sorted)]

    return plot_stacked_item_company(
        df=item_per_company_filtered,
        item_type=item_type,
        companies_sorted=companies_sorted
    )
