from datetime import datetime

from dash import dcc, html, Output, Input, State, clientside_callback, ClientsideFunction
import dash_mantine_components as dmc
from dash_iconify import DashIconify

GITHUB = 'https://github.com/Tanguy9862/new-drug-approvals-dashboard'
CONTACT_ICON_WIDTH = 30

CURRENT_YEAR = datetime.utcnow().year


def modal_data_source():
    return dmc.Modal(
        id='modal-data-source',
        size='50%',
        styles={
            'modal': {
                'background-color': '#f2f2f2',
            }
        },
        children=[
            dcc.Markdown(
                [
                    f"""
                    # Data Source Overview
                    
                    ## Source and Systematic Automation
                    
                    Our drug approval data is derived from the comprehensive and up-to-date listings available at 
                    [Drugs.com](https://www.drugs.com/newdrugs-archive/{CURRENT_YEAR}.html), which includes detailed information on newly approved drugs spanning various years. We 
                    have automated our scraping process to run autonomously every 6 hours, ensuring our 
                    database consistently reflects the most current data. This relentless automation guarantees that 
                    any updates or new entries on the Drugs.com archive are immediately captured and updated in our 
                    database.
                    
                    ## Integrated Data Enrichment 
                    
                    During each scraping session, the data is not only collected but also enriched using advanced 
                    language models, particularly OpenAI's GPT-3.5 Turbo. This integrated enrichment process includes:
                    
                    - **Drug Classification:** Assigning categories to drugs based on their name, mode of 
                    administration, description, and indicated treatment, which include detailed categories like 
                    Antibiotics, Cardiovascular, Antineoplastics, etc. 
                    
                    - **Disease Classification:** Sorting diseases based on the drug used and the indicated treatment 
                    into categories such as Infectious Diseases, Neurological Disorders, etc.

                    ## Access to Scraper Details
                    
                    The source code for our scraper is openly maintained on GitHub. For those interested in 
                    understanding more about our scraping process or seeking detailed information on the methodology, 
                    you can visit our repository here: [GitHub Repository](https://github.com/Tanguy9862/scraper-new-drug-approvals).
                    """
                ],
                style={'text-align': 'justify'}
            )
        ]
    )


header = html.Div(
    [
        modal_data_source(),
        dmc.Group(
            [
                dmc.ActionIcon(
                    [
                        DashIconify(icon='bx:data', color='#C8C8C8', width=25)
                    ],
                    variant='transparent',
                    id='about-data-source'
                ),
                dmc.Anchor(
                    [
                        DashIconify(icon='uil:github', color='#8d8d8d', width=CONTACT_ICON_WIDTH),
                    ],
                    href=GITHUB
                )
            ],
            spacing='md',
        )
    ]
)

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='toggle_modal_data_source'),
    Output('modal-data-source', 'opened'),
    Input('about-data-source', 'n_clicks'),
    State('modal-data-source', 'opened')
)
