
PROJECT_NAME = 'new-drug-approvals'
BUCKET_NAME = 'new_drug_approvals_data'
FILENAME = 'new_drug_approvals.csv'
FILENAME_UPDATE = 'last_update.txt'
API_KEY_SECRET_ID = 'api_key_openai'

# Uncomment and set the GOOGLE_APPLICATION_CREDENTIALS environment variable to your Google Cloud service account key
# file ONLY if you are planning to use Google Cloud Storage for data operations. This is necessary for authentication
# and authorization when interacting with Google Cloud services. Make sure to replace
# 'new-drug-approvals-c2228690de9f.json' with the path to your actual service account key file.

# import os
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'new-drug-approvals-c2228690de9f.json'


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

KPI_ITEMS = [
    {'label': 'top-company', 'icon': 'mdi:domain', 'color': '#A3CCE9'},
    {'label': 'main-focus', 'icon': 'mdi:bacteria-outline', 'color': '#F9B5AC'},
    {'label': 'leading-class', 'icon': 'mdi:pill', 'color': '#9AD3BC'},
    {'label': 'last-updated', 'icon': 'mdi:clock-outline', 'color': '#B8A9C9'},
]
SUFFIXES_TO_DELETE = [' Diseases', ' Disorders', ' Conditions', ' System']
