from datetime import datetime

import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objs import Figure
from pandas import DataFrame

from utils.config import (
    WITHOUT_PADDING,
    BG_TRANSPARENT,
    HOVERLABEL_TEMPLATE,
)

# DATA
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

drug_approvals_df = pd.read_csv('new_drug_approvals.csv').drop(['Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11'], axis=1)
drug_approvals_df['Date of Approval'] = pd.to_datetime(drug_approvals_df['Date of Approval'], errors='coerce')
drug_approvals_df['year'] = drug_approvals_df['Date of Approval'].dt.year
# df['months'] = df['Date of Approval'].dt.month
# df['test'] = df['Date of Approval'].dt.to_period('M')
# print(df['test'].head(25))

# CONSTANTES
MARGIN_BOTTOM = 7
MIN_YEAR, MAX_YEAR, CURRENT_YEAR = drug_approvals_df['year'].min(), drug_approvals_df['year'].max(), datetime.now().year


def plot_approvals_year(df: DataFrame) -> Figure:
    """
    Creates a time-series plot showing the number of drug approvals per month.

    Args:
        df (DataFrame): A dataframe with approval dates and counts.

    Returns:
        Figure: A Plotly figure object for the time-series plot.
    """

    fig = px.line(
        df,
        x='Date of Approval',
        y='total'
    )

    fig.update_layout(
        margin=dict(pad=15, t=0, b=0, l=0, r=15),
        yaxis=dict(title=None, gridcolor='#f0f0f0'),
        xaxis=dict(
            title=None,
            showgrid=False,
            dtick='M1',
            tickformat="%b",
            showspikes=True,
            spikedash='dot',
            spikemode='toaxis+marker',
            spikecolor='#006400',
        ),
        plot_bgcolor=BG_TRANSPARENT,
        paper_bgcolor=BG_TRANSPARENT,
        hoverlabel=HOVERLABEL_TEMPLATE,
        hovermode='x unified',
    )

    fig.update_traces(
        fill='tozeroy',
        fillcolor='rgba(0, 100, 0, 0.1)',
        mode='lines+markers',
        line=dict(color='#006400', width=2),
        line_shape='spline',
        hovertemplate="Total Approvals: %{y}<extra></extra>",
    )

    return fig


# def plot_min_approvals_year(df):
#
#     fig = px.line(
#         df,
#         x='year',
#         y='total'
#     )
#
#     fig.update_layout(
#         margin=WITHOUT_PADDING,
#         plot_bgcolor=BG_TRANSPARENT,
#         paper_bgcolor=BG_TRANSPARENT,
#         xaxis=dict(title=None, showgrid=False, visible=False),
#         yaxis=dict(title=None, showgrid=False, visible=False),
#     )
#
#     fig.update_traces(
#         fill='tozeroy',
#         fillcolor='rgba(0,0,0,0.1)',
#         line_shape='spline',
#         line=dict(color='rgba(0,0,0,0.1)', width=0),
#         hovertemplate=None,
#         hoverinfo='none'
#     )
#
#     return fig


def plot_drug_type(df: DataFrame) -> Figure:
    """
    Creates a bar chart showing the top 5 drug types based on the number of approvals.

    Args:
        df (DataFrame): A dataframe with drug types and counts.

    Returns:
        Figure: A Plotly figure object for the bar chart.
    """

    healthcare_pastel_palette = [
        '#88D9E6',
        '#97D8B2',
        '#FFC4C4',
        '#F3E0EC',
        '#FAF1D6'
    ]

    fig_approvals_drug_type = go.Figure(data=[go.Pie(
        labels=df['drug_type'],
        values=df['total'],
        hole=0.7,
        pull=[0.05] * len(df),
        textinfo='none',
        marker=dict(colors=healthcare_pastel_palette),
    )])

    fig_approvals_drug_type.update_layout(
        legend=dict(
            y=0.5,
            font=dict(
                size=9,
                color="black"
            )
        ),
        margin=WITHOUT_PADDING
    )

    return fig_approvals_drug_type


def plot_stacked_item_company(df: pd.DataFrame, item_type: str, companies_sorted: list) -> Figure:
    """
    Create a Plotly Express stacked bar chart from the filtered DataFrame.

    Args:
    df (pd.DataFrame): Filtered DataFrame containing approval data for top companies.
    item_type (str): Category of approvals ('drug' or 'disease') used for coloring the bars.
    companies_sorted (list): List of company names sorted by the total approvals.

    Returns:
    Figure: A Plotly graph object figure with a stacked bar chart.
    """

    fig = px.bar(
        df,
        x='total',
        y='Company',
        color=item_type,
        category_orders={'Company': companies_sorted},
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )

    fig.update_layout(
        bargap=0.3,
        plot_bgcolor=BG_TRANSPARENT,
        paper_bgcolor=BG_TRANSPARENT,
        hoverlabel=HOVERLABEL_TEMPLATE,
        hovermode='y unified',
        margin=dict(pad=10, t=0, b=0, l=0, r=0),
        xaxis=dict(title=None, gridcolor='#f0f0f0', tickfont=dict(color='rgba(0, 0, 0, 0.6)'), dtick=1),
        yaxis=dict(title=None, tickfont=dict(color='rgba(0, 0, 0, 0.6)'), showspikes=False),
        legend=dict(
            title=None,
            y=0.5,
            font=dict(
                size=12,
                color='rgba(0, 0, 0, 0.6)'
            )
        )
    )

    fig.update_traces(
        hovertemplate='%{x}',
        marker_line_width=0
    )

    return fig
