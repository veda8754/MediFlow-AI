import pandas as pd
import plotly.express as px

# MediFlow chart theme
CHART_BACKGROUND = "#03A89E"
CHART_COLOR = "#4682B4"
TEXT_COLOR = "#000000"


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor=CHART_BACKGROUND,
        plot_bgcolor=CHART_BACKGROUND,
        font=dict(color=TEXT_COLOR),
        title_font=dict(color=TEXT_COLOR, size=20),
        legend=dict(font=dict(color=TEXT_COLOR)),
        xaxis=dict(
            title_font=dict(color=TEXT_COLOR),
            tickfont=dict(color=TEXT_COLOR),
            gridcolor="rgba(0,0,0,0.12)"
        ),
        yaxis=dict(
            title_font=dict(color=TEXT_COLOR),
            tickfont=dict(color=TEXT_COLOR),
            gridcolor="rgba(0,0,0,0.12)"
        )
    )
    return fig


def get_category_chart(df):
    category_data = (
        df["category"]
        .fillna("Unclassified")
        .replace("", "Unclassified")
        .value_counts()
        .reset_index()
    )

    category_data.columns = ["Category", "Count"]

    fig = px.bar(
        category_data,
        x="Category",
        y="Count",
        title="Enquiries by Category",
        text="Count",
        color_discrete_sequence=[CHART_COLOR]
    )

    fig.update_traces(
    textposition="outside",
    textfont=dict(color=TEXT_COLOR),
    marker=dict(
        color=CHART_COLOR,
        line=dict(width=0),
        cornerradius=20
    )
)
    

    return style_chart(fig)


def get_sentiment_chart(df):
    sentiment_data = (
        df["sentiment"]
        .fillna("Not Analysed")
        .replace("", "Not Analysed")
        .value_counts()
        .reset_index()
    )

    sentiment_data.columns = ["Sentiment", "Count"]

    fig = px.pie(
        sentiment_data,
        names="Sentiment",
        values="Count",
        title="Sentiment Distribution",
        hole=0.45,
        color_discrete_sequence=[
            CHART_COLOR,
            "#6495ED",
            "#5F9EA0",
            "#B0C4DE"
        ]
    )

    fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
    textfont=dict(color=TEXT_COLOR),
    marker=dict(
        line=dict(color="#03A89E", width=3)
    )
)

    return style_chart(fig)


def get_priority_chart(df):
    priority_data = (
        df["priority"]
        .fillna("Not Analysed")
        .replace("", "Not Analysed")
        .value_counts()
        .reset_index()
    )

    priority_data.columns = ["Priority", "Count"]

    fig = px.bar(
        priority_data,
        x="Priority",
        y="Count",
        title="Enquiry Priority Distribution",
        text="Count",
        color_discrete_sequence=[CHART_COLOR]
    )

    fig.update_traces(
    textposition="outside",
    textfont=dict(color=TEXT_COLOR),
    marker=dict(
        color=CHART_COLOR,
        line=dict(width=0),
        cornerradius=20
    )
)

    

    return style_chart(fig)