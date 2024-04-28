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
        # style={'border': 'solid 1px red'},
        span=3,
    )
