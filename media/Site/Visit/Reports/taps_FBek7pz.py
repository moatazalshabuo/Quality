import json
from datetime import datetime, timedelta
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash
from dash import Output, Input, html, dcc, State, Patch, MATCH, dash_table, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import sqlite3
from Analytic3.ReusbleVar import Var
from Analytic3.sidebar import create_sidebar
from dashboard.database_connection import DatabaseConnection
from datetime import datetime, date
import polars as pl
import dash_auth
import plotly.graph_objects as go
import pandas as pd

def create_analysis_tap():
    presentday = datetime.now()
    yesterday = presentday - timedelta(1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    db = DatabaseConnection()
    df_wells = db.well_names("Erawin")

    whole_filed = dmc.Checkbox(id="filed", label="Field", value="whole_filed", mb=10),
    wells = dmc.MultiSelect(
        label="Select Wells",
        placeholder="Select all you like!",
        id='wells-selection',
        data=[{'label': i, 'value': i} for i in df_wells['well'].unique()],
        style={"marginBottom": 10},
        value=['E1'],
        disabled=False,  # This disables interaction
    ),

    date_from = dmc.DatePicker(
        label="Start Date",
        id="date-from",
        value=yesterday,
        minDate=date(2023, 10, 1),

        # style={"width": 250},
    )
    date_to = dmc.DatePicker(
        label="To Date",
        id="date-to",
        value=yesterday,
        # style={"width": 250},
    )

    calculated_data = dmc.Select(
        label="Calculated Data",
        data=["Discharge Pressure",
              "Average Amps",
              "Drive Frequency",
              "Intake Pressure",
              "Intake Temperature",
              "Motor Temperature",
              "Oil",
              "Gas",
              "Water"],
        id='calculated_data',
        icon=DashIconify(icon="radix-icons:magnifying-glass"),
        searchable=True,
        clearable=True,
        nothingFound="No options found",
        style={"width": 100},
    )

    period = dmc.Select(
        label="Recurring duration",
        id='period',
        data=[
            {'label': 'daily', 'value': 'daily'},
            {'label': 'weekly', 'value': 'weekly'},
            {'label': 'monthly', 'value': 'monthly'},
            {'label': 'quarters', 'value': 'quarters'},
        ],

        value='daily'
    )
    agg_method = dmc.Select(
        label="Aggregation method",
        id='agg-method',
        data=[
            {'label': 'sum', 'value': 'sum'},
            {'label': 'avg', 'value': 'avg'},
        ],

        value='sum'
    )
    variable_name = dmc.TextInput(id='variable_name', label="variable name", style={"width": 100}),

    submit = dbc.Button('submit', id='sbmt', n_clicks=0, size="sm", color="primary", disabled=True),
    tabs = dmc.Tabs(
        [
            dbc.Card(
                [
                    dbc.CardBody([
                        dbc.Row(id='variable', children=[]),
                    ]),
                    html.Div([
                        dmc.TabsList(
                            [
                                dmc.Tab("Analysis", value="1"),
                                dmc.Tab("Calculation", value="2"),
                                dmc.Tab("Calculation_", value="3"),
                            ]
                        ),
                    ], className='w-50 m-auto '),
                ], className='shadow-sm'),


            dmc.TabsPanel(
                [
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(whole_filed, width=1),
                                    dbc.Col(wells),
                                    dbc.Col(calculated_data),
                                    dbc.Col(date_from),
                                    dbc.Col(date_to),
                                    dbc.Col(variable_name),
                                    dbc.Col(submit, style={"margin-top": "1rem"},),

                                ],),
                        ], body=True, style={"margin": "1rem"}),
                    html.Div(id="analysis-table", style={"margin-top": "1rem"}),
                    html.Div(id="analysis-chart", style={"margin-top": "1rem"}),
                    html.Div(id='df-value', style={'display': 'none'})

                ],
                value="1"),
            dmc.TabsPanel([
            # =============================== Muetaz's modifications start from here ======================================
                html.Div(
                    id="calcul",
                    children=dbc.Card(
                        children=dbc.CardBody(
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col([

                                            dbc.Label(children='Index', className='m-0'),
                                            dbc.Input(type='text', disabled=True, id='var_index_show',
                                                      placeholder='index'), ], width=2

                                        ),
                                        dbc.Col(
                                            [
                                                dmc.Select(
                                                    label="aggregation",
                                                    placeholder="aggregation",
                                                    id='aggregation',
                                                    data=[
                                                        {"label": "ALL", "value": ""},
                                                        {'label': 'Mounthly', 'value': 'month'},
                                                        {'label': 'Weekly', 'value': 'week'},
                                                        {'label': 'Daily', 'value': 'day'}
                                                    ],
                                                    style={"marginBottom": 10},
                                                    value='line',
                                                )
                                            ],
                                            width=3
                                        ),
                                        dbc.Col(
                                            [
                                                dmc.Select(
                                                    label="Group",
                                                    placeholder="Group",
                                                    id='Group',
                                                    data=[
                                                        {"label": "None", "value": ""},
                                                        {'label': 'sum', 'value': 'sum'},
                                                        {'label': 'mean', 'value': 'mean'},
                                                        {'label': 'min', 'value': 'min'},
                                                        {'label': 'max', 'value': 'max'},
                                                    ],
                                                    style={"marginBottom": 10},
                                                    value='line',
                                                )
                                            ],
                                            width=3
                                        ),
                                        dbc.Col(
                                            dbc.Button(className='btn btn-primary', children='add', id='add-var'),
                                            width=2
                                        )
                                    ]
                                ),
                                dbc.Alert(children='', className='alert-danger', is_open=False, id='alert-opration'),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Textarea(placeholder='The result', disabled=True, style={'padding': 20},
                                                         id='show-resault', rows=7), width=10)
                                        , dbc.Col([dbc.Button(className='btn btn-primary w-100', id='ex', n_clicks=0,
                                                             children='excute'),dbc.Button("save ",className='btn-info w-100 mt-2', id="open", n_clicks=0),], width=2)
                                    ]
                                ),
                                dbc.Card(
                                    className='pt-2',
                                    children=[
                                        dbc.Row([
                                            dbc.Col(
                                                children=dbc.Table(
                                                    children=[
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    dbc.Button(
                                                                        className='btn w-100',
                                                                        children='+',
                                                                        value='+',
                                                                        id='button_+',
                                                                        n_clicks=0,
                                                                    )
                                                                ),
                                                                html.Td(
                                                                    dbc.Button(
                                                                        className='btn w-100',
                                                                        children='-',
                                                                        value='-',
                                                                        id='button_-',
                                                                        n_clicks=0,
                                                                    )
                                                                ),
                                                                html.Td(
                                                                    dbc.Button(
                                                                        className='btn w-100',
                                                                        children='/',
                                                                        value='/',
                                                                        id='button_/',
                                                                        n_clicks=0,
                                                                        n_clicks_timestamp=0
                                                                        # Optional for tracking recent clicks
                                                                    )
                                                                ),
                                                                html.Td(
                                                                    dbc.Button(
                                                                        className='btn w-100',
                                                                        children='*',
                                                                        value='*',
                                                                        id='button_*',
                                                                        n_clicks=0,
                                                                    )
                                                                ),
                                                            ]
                                                        ),
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    dbc.Button(
                                                                        className='btn w-100',
                                                                        children='log',
                                                                        value='log',
                                                                        id='button_log',
                                                                        n_clicks=0,
                                                                    )
                                                                ),
                                                                html.Td(
                                                                    dbc.Button(
                                                                        className='btn w-100',
                                                                        children='e',
                                                                        value='e',
                                                                        id='button_e',
                                                                        n_clicks=0,
                                                                    )
                                                                ), html.Td(
                                                                dbc.Button(
                                                                    className='btn w-100',
                                                                    children='(',
                                                                    value='(',
                                                                    id='button_(',
                                                                    n_clicks=0,
                                                                )
                                                            ), html.Td(
                                                                dbc.Button(
                                                                    className='btn w-100',
                                                                    children=')',
                                                                    value=')',
                                                                    id='button_)',
                                                                    n_clicks=0,
                                                                )
                                                            ),

                                                            ]
                                                        ),
                                                    ],
                                                    id='tab-buttons',
                                                ),
                                                width=6
                                            ), dbc.Col(
                                                children=
                                                dbc.Input(
                                                    type='number',
                                                    placeholder='enter number',
                                                    step=0.1,
                                                    id='num_id'
                                                ),
                                                width=4
                                            ), dbc.Col(
                                                children=dbc.Button(
                                                    className='btn btn-primary',
                                                    children='enter',
                                                    id='enter_id',
                                                    n_clicks=0
                                                )
                                            ), dbc.Col(
                                                children=dbc.Button(
                                                    className='btn btn-warning',
                                                    style={'color': '#fff'},
                                                    children='C',
                                                    id='back_id',
                                                    n_clicks=0
                                                )
                                            )
                                        ]
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ),
                html.Div(
                    dbc.Card(
                        children=[dbc.CardHeader(
                            children='Execute result'
                        ),
                            dbc.CardBody(
                                [],
                                id='show_execute'
                            ),dbc.CardBody(
                                [
                                    dash_table.DataTable(id='table-selected',
                                                         page_size=10,
                                                         style_table={'overflowY': 'auto',
                                                                      # 'width' : '200px',
                                                                      'overflowX': 'auto'},
                                                         row_selectable="single",
                                                         selected_rows=[],

                                                         )
                                ],

                            )]
                    )
                ),
                html.Div( id="eq_chart"),
                html.Div(id='eq_df', style={'display': 'none'})

            ], value="2"),
            dmc.TabsPanel([dbc.Row([
                dbc.Col(
                    [
                        dmc.Select(
                            label="equation",
                            placeholder="equation",
                            id='equation',
                            data=[
                                {"label":row['descripe'] , "value": row['id']} for index,row in DatabaseConnection().select_all_equation().to_pandas().iterrows()
                                ],
                            style={"marginBottom": 10},
                            value='line',
                        )
                    ],
                    width=8
                ),
                dbc.Col(
                    dbc.Button(
                        children='execute',
                        id='execute_e',
                        className='w-100 mt-3'
                    )
                )]
            ),dbc.Card(
                        children=[dbc.CardHeader(
                            children='Execute result'
                        ),
                            dbc.CardBody(
                                [],
                                id='show_execute_e'
                            )
                        ]
                    )], value="3"),
        ],
        value="1",
        id="tabs",
        color="red",
    )
    return tabs


