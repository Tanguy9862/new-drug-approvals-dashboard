from operator import itemgetter
from typing import Dict, Any

import dash_mantine_components as dmc
from dash_iconify import DashIconify


PADDING_TOP = 15
PADDING_LEFT = 25
BORDER_RADIUS = 10


def make_container(
        children,
        style_height,
        pt=PADDING_TOP,
        pl=PADDING_LEFT,
        **kwargs
):
    extra_styles = kwargs.get('extra_styles', {})
    return dmc.Container(
        children=children,
        pt=pt,
        pl=pl,
        fluid=True,
        style={
            'background-color': 'white',
            'border-radius': BORDER_RADIUS,
            'height': style_height,
            'font-family': 'Ubuntu, sans-serif',
            **extra_styles
        }
    )


def assemble_kpi_panel(kpi_item):

    label, icon, color = kpi_item['label'], kpi_item['icon'], kpi_item['color']

    return dmc.Col(
        [
            dmc.Group(
                [
                    DashIconify(
                        icon=icon,
                        width=40,
                        height=45,
                        color=color
                    ),
                    dmc.Stack(
                        [
                            dmc.Text(
                                label.replace('-', ' '),
                                transform='uppercase',
                                weight=200,
                                style={'font-size': '0.9375'}
                                # size=15
                            ),
                            dmc.Text(
                                None,
                                transform='capitalize',
                                weight=500,
                                # size=16 if label != 'last-updated' else 14,
                                style={'font-size': '1rem'},
                                id=f'{label}-kpi'
                            )
                        ],
                        style={'height': '100%'},
                        justify='center',
                        ml='xs',
                        spacing=0
                    )
                ],
                mt=5,
                spacing='sm'
            )
        ],
        span=3,
    )


def make_tooltip_layout(hover_data: Dict[str, Any]) -> dmc.Group:
    """
    Creates a layout for displaying tooltip information based on hover data from a Plotly graph.

    This function constructs a visual representation for a tooltip that includes a color box
    representing the data point and textual information about the data point (label and value).

    Args:
        hover_data (Dict[str, Any]): A dictionary containing the hover data from the drug-type graph.
            This dictionary is expected to contain a 'points' list with at least one item,
            which itself is a dictionary with 'label', 'color', and 'v' keys.

    Returns:
        dmc.Group: A Dash Mantine Component (dmc) Group component that includes the visual layout
        for the tooltip, composed of a colored box and text elements displaying the data label and value.
    """

    label, color, value = itemgetter('label', 'color', 'v')(hover_data['points'][0])

    return dmc.Group(
        [
            dmc.Container(
                px=0,
                m=0,
                mr=8,
                style={
                    'background-color': color,
                    'width': '12px',
                    'height': '12px',
                    'border-radius': '15px',
                    'border': 'none'
                }
            ),
            f'{label}:',
            dmc.Text(
                value,
                weight=700,
                ml=3,
            )
        ],
        position='center',
        spacing=0,
        style={
            'width': '100%'
        }
    )

