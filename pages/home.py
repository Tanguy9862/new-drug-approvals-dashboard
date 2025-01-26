from typing import List, Dict, Tuple, Any

import dash
from dash import dcc, html, callback, Input, Output, State, no_update, clientside_callback, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import dash_ag_grid as dag
import pandas as pd
from plotly.graph_objs import Figure

from assets.header import header

from utils.home_utils import (
    plot_approvals_year,
    plot_drug_type,
    plot_stacked_item_company,
    add_loading_overlay,
    MARGIN_BOTTOM
)

from layouts.home_layout import (
    make_container,
    assemble_kpi_panel,
    make_tooltip_layout,
    make_modal
)

from layout_constants import (
    FIG_CONFIG,
    KPI_ITEMS as kpi_items,
    SUFFIXES_TO_DELETE,
)

dash.register_page(
    __name__,
    path='/',
    order=1,
    title='Pharmaceutical Drug Approvals Dashboard',
    description='A comprehensive visualization of global drug approval data, featuring interactive charts and '
                'real-time updates. This dashboard provides insights into drug approvals by category, company, '
                'and treatment types, drawing on extensive data collected from public health sources.',
    image="miniature.png"
)

layout = html.Div(
    [
        dcc.Store(data=None, id='drug-approvals-data'),
        dcc.Store(data=None, id='filtered-drug-approvals-data'),
        dcc.Store(id='mouse-position'),
        make_modal(),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Group(
                            [
                                dmc.Group(
                                    [
                                        dmc.Title(
                                            'Drug Approval Overview for',
                                            order=3,
                                            align='justify',
                                            style={
                                                'font-family': 'Roboto, Sans Serif',
                                                'font-weight': '300'
                                            }

                                        ),
                                        dmc.NumberInput(
                                            label=None,
                                            id='year-input',
                                            p=0,
                                            mt=-3,
                                            style={"width": "90px"},
                                            styles={
                                                'input': {
                                                    'background-color': '#F8F8F8',
                                                    'padding-left': '0',
                                                    'border': 'none',
                                                    'font-size': '1.375rem',
                                                    'font-weight': '300',
                                                    'font-family': 'Roboto, Sans Serif',
                                                },
                                                'control': {'border': 'none'}
                                            },
                                            className='text-underline'
                                        )
                                    ],
                                    position='left',
                                    spacing=7
                                ),
                                header
                            ],
                            position='apart'
                        )
                    ],
                    offsetMd=1,
                    md=10
                )
            ],
            mt='md',
            mb=20
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
                                                            m=0,
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
                                                'border-radius': '10px',
                                                'height': '100%',
                                                'display': 'flex',
                                                'flex-direction': 'column',
                                                'justify-content': 'center'
                                            }
                                        )
                                    ],
                                    xl=2
                                ),
                                *[
                                    dmc.Col(
                                        [
                                            make_container(
                                                children=[
                                                    dmc.Center(
                                                        [assemble_kpi_panel(item)]
                                                    )
                                                ],
                                                extra_styles={
                                                    'display': 'flex',
                                                    'flex-direction': 'column',
                                                    'justify-content': 'center',
                                                    'align-items': 'center'
                                                },
                                                pl=0,
                                                pt=0,
                                                style_height='100%'
                                            )
                                        ],
                                        xl=2.5
                                    ) for item in kpi_items
                                ]
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
                                                    id='total-approvals-title',
                                                    size='sm',
                                                    mb='lg'
                                                ),
                                                add_loading_overlay(
                                                    elements=[
                                                        dcc.Graph(
                                                            id='yearly-approvals-fig',
                                                            figure=plot_approvals_year(
                                                                pd.DataFrame(columns=['Date of Approval', 'total'])
                                                            ),
                                                            style={'height': '250px', 'width': '95%',
                                                                   'margin-left': '10px'},
                                                            config=FIG_CONFIG,
                                                            responsive=True
                                                        )
                                                    ]
                                                )
                                            ],
                                            style_height='300px'
                                        )
                                    ],
                                    lg=8
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
                                                add_loading_overlay(
                                                    elements=[
                                                        dcc.Graph(
                                                            id='drug-type-fig',
                                                            figure=plot_drug_type(
                                                                df=pd.DataFrame(columns=['drug_type', 'total'])
                                                            ),
                                                            config=FIG_CONFIG,
                                                            style={'height': '250px'},
                                                            clear_on_unhover=True,
                                                            responsive=True
                                                        )
                                                    ]
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
                                    lg=4
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
                                                add_loading_overlay(
                                                    [
                                                        dcc.Graph(
                                                            id='company-stacked-fig',
                                                            config=FIG_CONFIG,
                                                            figure=plot_stacked_item_company(
                                                                df=pd.DataFrame(columns=['total', 'Company', 'drug_type']),
                                                                item_type='drug_type',
                                                                companies_sorted=list()
                                                            ),
                                                            responsive=True,
                                                            style={'height': '75%', 'margin-top': '30px'}
                                                        )
                                                    ],
                                                    extra_styles={'height': '75%'}
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
                                dmc.Text(None, mb='lg', id='approved-drugs-title', pt=20, pl=25),
                                dmc.Container(
                                    [
                                        dag.AgGrid(
                                            id='approvals-grid-data',
                                            className='ag-theme-material',
                                            style={'height': '100%', 'width': '90%'},
                                            columnSize='sizeToFit',
                                            dashGridOptions={'suppressMovableColumns': True},
                                            defaultColDef={'width': 128, 'resizable': False},
                                        )
                                    ],
                                    px=0,
                                    style={
                                        'display': 'flex',
                                        'justify-content': 'center',
                                        'align-items': 'center',
                                        'height': '88%',
                                        'width': '100%'
                                    }
                                )
                            ],
                            pt=0, pl=0,
                            style_height='82.8vh'
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
    Output('total-approvals-title', 'children'),
    Output('approved-drugs-title', 'children'),
    Input('year-input', 'value'),
    State('drug-approvals-data', 'data')
)
def update_drug_approvals_data(year: int, data: dict) -> tuple[list[dict], str, str]:
    """
    Filters drug approvals data based on the selected year and converts it to a dictionary suitable for Dash components.

    Args:
        year (int): The year selected by the user.
        data (dict): The original drug approvals data..

    Returns:
        tuple[list[dict], str, str]:
            - A list of dictionaries representing the filtered drug approvals data for the selected year.
            - A formatted string indicating the total number of approvals for the selected year.
            - A formatted string indicating the title for the list of approved drugs in the selected year.
    """

    df = pd.DataFrame(data)
    df_filtered = df.query('year == @year')
    return df_filtered.to_dict('records'), f'Total Approvals in {year}', f'Approved Drugs in {year}'


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
    State('drug-approvals-last-update', 'data'),
    prevent_initial_call=True
)
def update_kpi_panel(data: List[Dict[str, Any]], last_update) -> tuple[Any, str | Any]:
    """
    Processes drug approval data to update KPIs for display in the dashboard.

    Args:
        data (List[Dict[str, Any]]): The data from the client-side store that includes drug approvals.

    Returns:
        Tuple containing KPI values for the top company, main focus, leading drug class, and the last updated timestamp.
    """
    df = pd.DataFrame(data)
    all_kpis = []

    # Process top items for each KPI
    for col in ['Company', 'disease_type', 'drug_type']:
        top_item = df.groupby(col).size().reset_index(name='total').sort_values(by='total', ascending=False)
        top_item_name = top_item.iloc[0][col]

        # Clean up disease_type names by removing specified suffixes
        if col == 'disease_type':
            for suffix in SUFFIXES_TO_DELETE:
                if suffix in top_item_name:
                    top_item_name = top_item_name.replace(suffix, '')
                    break

        # Creates a tooltip for names that are too long or need additional context for display.
        if 'Reproductive' in top_item_name:
            top_item_name = dmc.Tooltip(
                ['Reprod. Sys.'],
                label=top_item_name,
                transition='fade',
                position='bottom',
                withArrow=True
            )

        elif len(top_item_name.split()) > 1:
            split_name = top_item_name.split()
            top_item_name = dmc.Tooltip(
                [f'{split_name[0]} {split_name[1][:5 if col != "Company" else 4]}.'],
                label=top_item_name,
                transition='fade',
                position='bottom',
                withArrow=True
            )

        all_kpis.append(top_item_name)

    return *all_kpis, last_update


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


@callback(
    Output('approvals-grid-data', 'rowData'),
    Output('approvals-grid-data', 'columnDefs'),
    Input('filtered-drug-approvals-data', 'data'),
    prevent_initial_callback=True
)
def update_grid_approvals(data: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Updates the data and column definitions for an Ag-Grid component in a Dash application.

    This callback fetches updated drug approval data and configures the grid to display this data.
    It also defines how the 'Details' column should render using a custom Dash-Mantine component for interactivity.

    Args:
        data (List[Dict]): List of dictionaries where each dictionary contains data of a single drug approval.

    Returns:
        Tuple[List[Dict], List[Dict]]: A tuple where the first element is the list of records for the grid's rowData
        and the second element is the list of dictionaries defining column properties for the grid.
    """

    df = pd.DataFrame(data)

    # Initialize 'Details' column to prepare for interactive elements
    df['Details'] = ''

    # Filter the DataFrame to ensure it's sorted by date and duplicates are removed
    cols = ['Date of Approval', 'drug_name', 'Details']
    filtered_df = df[cols].sort_values(by='Date of Approval', ascending=False).drop_duplicates()
    filtered_df['Date of Approval'] = filtered_df['Date of Approval'].str.split('T').str[0]

    # Set up column definitions for the grid, including custom renderers for interactive functionality
    column_defs = [
        {
            'headerName': 'Date',
            'field': 'Date of Approval',
        },
        {
            'headerName': 'Drug Name',
            'field': 'drug_name',
        },
        {
            'field': 'Details',
            'cellRenderer': 'DMC_ActionIcon',
            'cellRendererParams': {
                'icon': 'f7:ellipsis-circle-fill',
                'iconColor': '#bfbfbf',
                'iconWidth': '20',
                'iconHeight': '20',
                'variant': 'subtle',
                'marginTop': '8px',
                'marginLeft': '6px',
            }
        },
    ]

    return filtered_df.to_dict('records'), column_defs


@callback(
    Output('modal-detailed-drug', 'opened'),
    Output('modal-detailed-drug', 'title'),
    Output('badge-disease-type', 'children'),
    Output('badge-drug-type', 'children'),
    Output('badge-mode-administration', 'children'),
    Output('drug-description', 'children'),
    Output('modal-treatment-for', 'children'),
    Output('modal-company', 'children'),
    Input('approvals-grid-data', 'cellRendererData'),
    State('modal-detailed-drug', 'opened'),
    State('filtered-drug-approvals-data', 'data'),
    prevent_initial_call=True
)
def toggle_modal_drug(
        clicked_grid_data: dict,
        opened: bool,
        approvals_data: list
) -> tuple:
    """
    Toggles the drug detail modal, updates the content based on the clicked row in the drug approvals grid.

    Args:
        clicked_grid_data (dict): Data containing the clicked row information, such as drug name and date of approval.
        opened (bool): Current state of the modal, whether it is open or closed.
        approvals_data (list): List of dictionaries representing the drug approvals data.

    Returns:
        tuple: Returns multiple outputs to update the state of the modal and its content. This includes:
               - Modal open/close state.
               - Modal title.
               - Disease type, drug type, and mode of administration as badges.
               - Drug description.
               - Treatment information.
               - Company information.
    """

    # Extracting necessary details from clicked grid data
    drug_name = clicked_grid_data['value']['drugName']
    approval_date = clicked_grid_data['value']['dateApproval']

    # Filtering the DataFrame for the selected drug based on drug name and approval date
    if drug_name:
        df = pd.DataFrame(approvals_data)
        df_filtered = df.query(
            'drug_name == @drug_name and `Date of Approval`.str.startswith(@approval_date)').drop_duplicates().iloc[0]

        # Preparing the modal title with drug name and generic name
        modal_title = [
            drug_name,
            dmc.Text(
                df_filtered['drug_generic_name'] or '-',
                size=15,
                style={'font-style': 'italic'}
            )
        ]
        # Generating badges for disease type, drug type, and mode of administration
        all_badges = [
            df_filtered['disease_type'] or '-',
            df_filtered['drug_type'] or '-',
            df_filtered['mode_administration'] or '-'
        ]

        # Setting the drug description or a default message if none is available
        description_drug = df_filtered['description'] or 'No description provided for this medication.'

        # Setting treatment and company information for the footer of the modal
        footer_modal = [df_filtered['Treatment for'] or '-', df_filtered['Company'] or '-']

        return not opened, modal_title, *all_badges, description_drug, *footer_modal

    raise PreventUpdate
