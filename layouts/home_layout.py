from operator import itemgetter
from typing import List, Dict, Any

import dash_mantine_components as dmc
from dash.development.base_component import Component
from dash_iconify import DashIconify


PADDING_TOP = 15
PADDING_LEFT = 25
BORDER_RADIUS = 10


def make_container(
        children: List[Component],
        style_height: str,
        pt: int = PADDING_TOP,
        pl: int = PADDING_LEFT,
        **kwargs: Dict[str, Any]
) -> dmc.Container:
    """
    Creates a stylized container for Dash components.

    Args:
        children (List[Component]): A list of Dash components to include within the container.
        style_height (str): The height CSS property value for the container.
        pt (int): Padding top value.
        pl (int): Padding left value.
        **kwargs (Dict[str, Any]): Additional keyword arguments to include extra styles.

    Returns:
        dmc.Container: A styled container component that encapsulates the children components.
    """

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


def assemble_kpi_panel(kpi_item: Dict[str, str]) -> dmc.Group:
    """
    Constructs a panel for displaying a key performance indicator (KPI) using badges and text.

    Args:
        kpi_item (Dict[str, str]): Dictionary containing label, icon, and color for the KPI.

    Returns:
        dmc.Group: A component group that visually represents the KPI with an icon and labels.
    """

    label, icon, color = kpi_item['label'], kpi_item['icon'], kpi_item['color']

    return dmc.Group(
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
                    ),
                    dmc.Text(
                        None,
                        transform='capitalize',
                        weight=500,
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
                    'width': '10px',
                    'height': '10px',
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


def make_modal() -> dmc.Modal:
    """
    Creates a modal component for displaying detailed information about a drug.

    Returns:
        dmc.Modal: A Dash Mantine Component modal that includes various child components like badges and texts,
                   configured for displaying drug-related information.
    """

    return dmc.Modal(
            id='modal-detailed-drug',
            title=None,
            children=[
                dmc.Group(
                    [
                        dmc.Tooltip(
                            label='Target disease category for this medication. Indicates the primary area of '
                                  'treatment.',
                            children=[
                                dmc.Badge(None, id='badge-disease-type', variant='gradient', size='md',
                                          gradient={"from": "teal", "to": "cyan", "deg": 45})
                            ],
                            transition='fade',
                            withArrow=True,
                            position='bottom'
                        ),
                        dmc.Tooltip(
                            label='Pharmacological class of the medication. Refers to the type of action the drug has '
                                  'on the body.',
                            children=[
                                dmc.Badge(None, id='badge-drug-type', variant='gradient', size='md', color='#4C9F70',
                                          gradient={"from": "grape", "to": "pink", "deg": 35})
                            ],
                            transition='fade',
                            withArrow=True,
                            position='bottom'
                        ),
                        dmc.Tooltip(
                            label='Method of drug administration. Describes how the drug is delivered to the patient.',
                            children=[
                                dmc.Badge(None, id='badge-mode-administration', variant='gradient', size='md',
                                          color='#4C9F70',
                                          gradient={"from": "orange", "to": "red"}),
                            ],
                            transition='fade',
                            withArrow=True,
                            position='bottom'
                        )
                    ],
                    spacing='xs',
                    position='left',
                    mt=-10
                ),
                dmc.Text(
                    None,
                    id='drug-description',
                    mt=35
                ),
                dmc.Group(
                    [
                        dmc.Container(
                            [
                                dmc.Text('treatment for', transform='uppercase', size=16),
                                dmc.Text(None, id='modal-treatment-for', weight=500, transform='uppercase'),
                            ],
                            style={'maxWidth': '70%'},
                            m=0,
                            px=0
                        ),
                        dmc.Container(
                            [
                                dmc.Text('developed by', transform='uppercase', size=16),
                                dmc.Text(None, id='modal-company', weight=500, transform='uppercase'),
                            ],
                            m=0,
                            px=0
                        )
                    ],
                    position='left',
                    mt='xl',
                    mb='md',
                    style={'align-items': 'flex-start'},
                    spacing=50
                )
            ],
            size='40%',
            transition='pop',
            styles={
                'title': {'font-size': '30px', 'font-weight': '400', 'margin-top': '5px'},
                'body': {'margin-top': '25px'},
                'modal': {
                    'background': 'linear-gradient(to bottom, #82c7a5 0%, #ffffff 100%)',
                    'border-radius': '15px'
                },
                'close': {'margin-top': '-50px', 'color': 'grey'}
            }
        )
