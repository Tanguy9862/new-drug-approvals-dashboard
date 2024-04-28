WITHOUT_PADDING = dict(pad=0, t=0, b=0, l=0, r=0)
BG_TRANSPARENT = 'rgba(0,0,0,0)'

HOVERLABEL_TEMPLATE = dict(
    bgcolor='rgba(0, 0, 0, 0.9)',
    bordercolor='rgba(0, 0, 0, 0.9)',
    font=dict(
        color='white'
    )
)

FIG_CONFIG = {
    'displayModeBar': False,
    'scrollZoom': False,
    'showTips': False
}

## HOME.PY
KPI_ITEMS = [
    {'label': 'top-company', 'icon': 'mdi:domain', 'color': '#A3CCE9'},
    {'label': 'main-focus', 'icon': 'mdi:bacteria-outline', 'color': '#F9B5AC'},
    {'label': 'leading-class', 'icon': 'mdi:pill', 'color': '#9AD3BC'},
    {'label': 'last-updated', 'icon': 'mdi:clock-outline', 'color': '#B8A9C9'},
]
SUFFIXES_TO_DELETE = [' Diseases', ' Disorders', ' Conditions', ' System']
