import json
from datetime import datetime, timedelta
import flask
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash
from dash import Output, Input, html, dcc, State, Patch, MATCH, dash_table, ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import sqlite3
from Analytic3.Const import Const
from Analytic3.ReusbleVar import Var
from Analytic3.home_page import create_home_layout
from Analytic3.sidebar import create_sidebar
from Analytic3.taps import create_analysis_tap
from Analytic3.modal import modal_save_e
from dashboard.database_connection import DatabaseConnection
from datetime import datetime, date
import polars as pl
import dash_auth
import plotly.graph_objects as go
import pandas as pd
from numpy import log, e
import numpy as np


def create_anna_application(flask_app):
    VALID_USERNAME_PASSWORD_PAIRS = {
        'sara': 'sara'
    }
    app = dash.Dash(__name__, server=flask_app,
                    suppress_callback_exceptions=True,
                    external_stylesheets=[dbc.themes.UNITED],
                    url_base_pathname='/analytiscs/',
                    )

    auth = dash_auth.BasicAuth(
        app,
        VALID_USERNAME_PASSWORD_PAIRS
    )

    app.config.suppress_callback_exceptions = True

    list_obj = {}

    def create_varible():
        agg_method = dmc.Select(
            label="Aggregation method",
            id='agg-for-var',
            data=[
                {'label': 'sum', 'value': 'sum'},
                {'label': 'avg', 'value': 'avg'},
            ],

            value='sum'
        )
        return agg_method

    content = html.Div(id="page-content")

    app.layout = html.Div([dcc.Location(id="url"),
                           create_sidebar(),
                           content, ])

    @app.callback(
        Output("sidebar", "className"),
        [Input("sidebar-toggle", "n_clicks")],
        [State("sidebar", "className")],
    )
    def toggle_classname(n, classname):
        if n and classname == "":
            return "collapsed"
        return ""

    @app.callback(
        Output("collapse", "is_open"),
        [Input("navbar-toggle", "n_clicks")],
        [State("collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open

    # create main layout
    @app.callback(Output("page-content", "children"),
                  [Input("url", "pathname")])
    def render_page_content(pathname):
        reformated_field_name = pathname.replace("%", " ")
        print(pathname)
        if pathname == "/analytiscs/calculation":
            return [create_analysis_tap(), modal_save_e()]

        if pathname == "/analytiscs/":
            return create_home_layout()

        # If the user tries to reach a different page, return a 404 message
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            className="p-3 bg-light rounded-3",
        )

    @app.callback(
        [Output("modal", "is_open"),
         Output('error_save', 'is_open'),
         Output('save_success', 'is_open'),
         Output('descripe', 'value')
         ],
        [Input("open", "n_clicks"),
         Input("close", "n_clicks"),
         Input('save', 'n_clicks')],
        [State("modal", "is_open"),
         State('descripe', 'value')],
    )
    def toggle_modal(n1, n2, save, is_open, descripe):
        ctx = dash.callback_context
        clicked_button = ctx.triggered[0]['prop_id'].split('.')[0]

        if clicked_button == 'close':
            return False, False, False, descripe
        elif clicked_button == 'open':
            return True, False, False, descripe
        elif clicked_button == 'save':
            if Const.equation != '' and descripe != '':
                db = DatabaseConnection()
                db.insert_equation(descrip=descripe, equation=Const.equation)
                return True, False, True, ''
            else:
                return True, True, False, descripe

    @app.callback(
        Output("sbmt", "disabled"),
        Input("variable_name", "value"), )
    def update_btn_disabled(var):
        print(type(var))
        if var is not None:
            if len(var) == 0:
                print("in if")
                return True  # Disable MultiSelect when checkbox is off

        elif len(var) > 0:
            return False  # Disable MultiSelect when checkbox is off

        else:
            return True

    @app.callback(
        Output("wells-selection", "disabled"),
        Input("filed", "checked"), )
    def update_multiselect_disabled(checked):
        print(checked)
        if checked:
            return True  # Disable MultiSelect when checkbox is off

    # ===================================================================eq_chart
    @app.callback(
        Output('show_execute_e', 'children'),
        [Input('execute_e', 'n_clicks'),
         Input('equation', 'value')]
    )
    def execute_e(n_clicks, equation):
        ctx = dash.callback_context
        clicked_button = ctx.triggered[0]['prop_id'].split('.')[0]

        if clicked_button == 'execute_e':
            try:
                value = DatabaseConnection().select_equation(equation).to_pandas()
            except Exception as e:
                return dbc.Alert(children=f"There's error in connection {e}", color='red')

            try:
                result = eval(value['equation'][0])
                print(result)
                if type(result) in [float, int]:
                    return html.Div([f'The result of execute is {result}'])
                elif type(result) == np.ndarray:
                    return html.Div(children=f'The result of execute is {result[0]}')
                else:
                    df = pl.DataFrame()
                    for val in Const.number:
                        dft = eval(val['value'])
                        df.rename(lambda column_name: column_name[:] + ' val' + val['var'])
                        df = pl.concat([df, dft], rechunk=True)
                    df['result'] = result
                    df = value.to_pandas()
                    df = result.to_dict('records')
                    return html.Div(children=dash_table.DataTable(df,
                                                                  page_size=10,
                                                                  style_table={'overflowY': 'auto',
                                                                               # 'width' : '200px',
                                                                               'overflowX': 'auto'}
                                                                  ))
            except Exception as e:
                return dbc.Alert(children=f"There's error in equation {e}", color='red')

    # @app.callback() fro execute the equation
    @app.callback(
        Output('show_execute', 'children'),
        Output('eq_chart', 'children'),
        Output('eq_df', 'children'),
        Input('ex', 'n_clicks')
    )
    def execute(n_clicks):
        data = {}
        if n_clicks > 0 and Const.equation != '':

            # try:
            value = eval(Const.equation)
            print("done here")
            print(value)
            if str(value).isdigit() or type(value) == float:
                return html.Div([f'The result of execute is {value}'])
            elif type(value) == np.ndarray:
                return html.Div(children=f'The result of execute is {value[0]}')
            else:
                df = pl.DataFrame()
                traces = []
                count = 1
                var_names = []
                for val in Const.number:
                    dft = eval(val['value'])
                    print("$$$$$$$$$$$$$$$$$$$$$")
                    print(dft)
                    new_df = dft.to_dict(as_series=False)

                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(new_df)
                    trace = go.Scatter(
                        x=new_df[f'{dft.columns[0]}'],
                        y=new_df[f'{dft.columns[1]}'],
                        mode='lines+markers',  # Define line style
                        # line=dict(color=item['color']),  # Set color dynamically
                        name=f"{dft.columns[0]}_{count}"
                        # Optional name for legend
                    )
                    count = count + 1
                    traces.append(trace)

                    for column in dft.columns:
                        print("$$$$$$$$$$$$$$$$$$$$$")
                        print(column)
                        dft = dft.rename({column: f'{column} var {val["var"]}'})
                        var_names.append(f'{column} var {val["var"]}')

                    df = pl.concat([df, dft], how="horizontal")

                # print(var_names)
                fig = go.FigureWidget(data=traces)

                df = df.to_pandas()
                df['result'] = value
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print(df)

                column_names = df.columns
                print(column_names)
                # Select cols names

                # df = df.to_dict('records')
                trace = go.Scatter(
                    x=df[f'{df.columns[0]}'],
                    y=df['result'],
                    mode='lines+markers',  # Define line style
                    # line=dict(color=item['color']),  # Set color dynamically
                    name=f"results"
                    # Optional name for legend
                )
                # traces.append(trace)
                selected_Variable = dmc.MultiSelect(
                    label="Select Variable",
                    placeholder="Select all you like!",
                    id='selected_Variable',
                    data=var_names,
                    style={"marginBottom": 10},
                    value=var_names,

                )
                selected_xaxis = dmc.Select(
                    label="Select xaxis",
                    placeholder="Select xaxis",
                    id='eq_xaxis',
                    data=[{'label': i, 'value': i} for i in column_names],
                    style={"marginBottom": 10},
                    value=f'{column_names[0]}',
                )

                selected_yaxis = dmc.Select(
                    label="Select yaxis",
                    placeholder="Select yaxis",
                    id='eq_yaxis',
                    data=[{'label': i, 'value': i} for i in column_names],
                    style={"marginBottom": 10},
                    value=f'{column_names[1]}',
                )

                chart_mode = dmc.Select(
                    label="Chart mode",
                    placeholder="Chart Mode",
                    id='eq_chart_mode',
                    data=[
                        {'label': 'markers', 'value': 'markers'},
                        {'label': 'Lines', 'value': 'lines'},
                        {'label': 'Lines and Markers', 'value': 'lines+markers'},

                    ],
                    style={"marginBottom": 10},
                    value='line',
                )

                add_chart = dbc.Button('Add Chart', id='show_eq', n_clicks=0, size="sm", color="primary", ),
                clear_chart = dbc.Button('Clear Chart', id='clear_eq', n_clicks=0, size="sm", color="primary", ),
                fig2 = go.FigureWidget(data=trace)
                # json_data = df.to_pandas()
                json_data = df.to_json()
                print("json_data")
                print(json_data)
                df = df.to_dict('records')

                chart_rows = html.Div([
                    dbc.Row(dcc.Graph(figure=fig2)),
                    dbc.Card(
                        [
                            dbc.Row([
                                dbc.Col(selected_xaxis, width=4),
                                dbc.Col(selected_yaxis, width=4),
                                dbc.Col(chart_mode, width=4),
                                dbc.Col(add_chart, width=4),
                                dbc.Col(clear_chart, width=4)
                            ], align="center", ),
                        ], body=True),
                    html.Div(dbc.Row(dcc.Graph(figure=fig, )), id='input_fig')
                ])

                return [html.Div(children=dash_table.DataTable(df,
                                                               page_size=10,
                                                               style_table={'overflowY': 'auto',
                                                                            # 'width' : '200px',
                                                                            'overflowX': 'auto'}
                                                               )), chart_rows, json_data]
            # except Exception as e:
            #     print(e)
            # return dbc.Alert(children=f"There's error in equation {e}",color='red')

    traces = []

    @app.callback(Output('input_fig', 'children'),
                  Input('eq_df', 'children'),
                  Input("eq_xaxis", "value"),
                  Input('eq_yaxis', 'value'),
                  Input('eq_chart_mode', 'value'),
                  Input('show_eq', 'n_clicks'),
                  Input('clear_eq', 'n_clicks'))
    def update_eq_chart(df, xaxis, yaxis, mode, btn_show, btn_clear):
        triggered_id = dash.ctx.triggered_id
        print(triggered_id)
        print(df, yaxis, xaxis, mode, btn_show)

        if triggered_id == "show_eq":
            # Convert the JSON string to a Python dictionary
            data = json.loads(df)
            # Create a Pandas DataFrame from the dictionary
            final = pd.DataFrame(data)
            pl_df = pl.from_pandas(final)
            column_names = pl_df.columns
            print(column_names)
            print(pl_df)
            trace = go.Scatter(
                x=pl_df[xaxis],
                y=pl_df[yaxis],
                mode=mode,  # Define line style
                # line=dict(color=item['color']),  # Set color dynamically
                name="var"
                # Optional name for legend
            )

            traces.append(trace)

            fig = go.FigureWidget(data=traces)
            print(fig)
            return dcc.Graph(figure=fig)

        if triggered_id == "clear_eq":
            traces.clear()
            fig = px.scatter()

            # Update layout to remove default elements
            fig.update_layout(xaxis_visible=True,
                              yaxis_visible=True,)  # Remove margins

            # (Optional) Add a title
            fig.update_layout(title_text="Empty Plot")
            return dcc.Graph(),


        else:
            raise PreventUpdate


    # =============================   this callback fro equation =============================================

    @app.callback(
        Output(component_id='show-resault', component_property='value'),
        Output('alert-opration', 'children'),
        Output('alert-opration', 'is_open'),
        Output('num_id', 'value'),
        Input({"type": "button", "index": ALL}, "n_clicks"),
        Input(component_id='button_+', component_property='n_clicks'),
        Input(component_id='button_-', component_property='n_clicks'),
        Input(component_id='button_/', component_property='n_clicks'),
        Input(component_id='button_*', component_property='n_clicks'),
        Input(component_id='button_log', component_property='n_clicks'),
        Input(component_id='button_e', component_property='n_clicks'),
        Input(component_id='button_(', component_property='n_clicks'),
        Input(component_id='button_)', component_property='n_clicks'),
        Input(component_id='enter_id', component_property='n_clicks'),
        Input('add-var', 'n_clicks'),
        Input('back_id', 'n_clicks'),
        State('num_id', 'value'),
        State('aggregation', 'value'),
        State('Group', 'value'),
        State('var_index_show', 'value')
    )
    def update_output(button, add_clicks,
                      subtract_clicks,
                      divide_clicks,
                      multiply_clicks,
                      log_clicks,
                      exp_clicks,
                      bow_rigth,
                      bow_left,
                      ent_num,
                      add_var,
                      back_id,
                      num, agg, group, index_var, ):

        ctx = dash.callback_context
        clicked_button = ctx.triggered[0]['prop_id'].split('.')[0]
        opartion = clicked_button.split('_')[-1]

        # ============== add var for equation i don't know i made it important to do agg and grouping ==============

        if clicked_button == 'add-var':
            if agg != '' and group != '':
                if agg == 'day':
                    type_agg = "%Y-%m-%d"
                if agg == 'month':
                    type_agg = "%Y-%m"
                if agg == 'week':
                    type_agg = "%Y-%W"
                Const.list_equation.append(
                    f'Var.data["{index_var}"].data_df.group_by(pl.col("DT").str.to_datetime().dt.strftime("{type_agg}")).agg(pl.{group}(Var.data["{index_var}"].data_df.columns[1])).sort("DT")[Var.data["{index_var}"].data_df.columns[1]]')
                Const.equation += f'Var.data["{index_var}"].data_df.group_by(pl.col("DT").str.to_datetime().dt.strftime("{type_agg}")).agg(pl.{group}(Var.data["{index_var}"].data_df.columns[1])).sort("DT")[Var.data["{index_var}"].data_df.columns[1]]'
                Const.list_show_equation.append(f'{group}(var{index_var},{agg})')
                Const.show_equation += f'{group}(var{index_var},{agg})'
                # print(Const.list_equation)
            elif agg == '' and group != '':
                Const.list_equation.append(
                    f'Var.data["{index_var}"].data_df[Var.data["{index_var}"].data_df.columns[1]].{group}()')
                Const.equation += f'Var.data["{index_var}"].data_df[Var.data["{index_var}"].data_df.columns[1]].{group}()'
                Const.list_show_equation.append(f'{group}(var{index_var})')
                Const.show_equation += f'{group}(var{index_var})'
            check = True
            for val in Const.number:
                if index_var == val['var']:
                    check = False
                else:
                    check = True
            if check:
                index = len(Const.list_equation) - 1
                Const.number.append({'index': index, 'var': index_var,
                                     'value': f'Var.data["{index_var}"].data_df.group_by(pl.col("DT").str.to_datetime().dt.strftime("{type_agg}")).agg(pl.{group}(Var.data["{index_var}"].data_df.columns[1])).sort("DT")'})
            print(Const.show_equation)
            return Const.show_equation, '', False, num
        # back one step in equation

        if 'back_id' == clicked_button and len(Const.list_equation) != 0:
            val = Const.list_equation[-1]
            index_val = Const.list_equation.index(val)
            val1 = Const.list_show_equation[-1]
            Const.list_equation.remove(val)
            Const.list_show_equation.remove(val1)
            Const.equation = ''.join([str(elem) for elem in Const.list_equation])
            Const.show_equation = ''.join([str(elem) for elem in Const.list_show_equation])
            print(Const.number)
            for val in Const.number:
                if index_val is val['index']:
                    Const.number.remove(val)
            print(Const.number)
            return Const.show_equation, '', False, num

        # enter number to equation

        if clicked_button == 'enter_id' and str(num).isnumeric():
            Const.list_equation.append(str(num))
            Const.equation += str(num)
            Const.list_show_equation.append(str(num))
            Const.show_equation += str(num)
            return Const.show_equation, '', False, ''

        if clicked_button in ['button_+', 'button_-', 'button_/', 'button_*', 'button_log', 'button_e', 'button_(',
                              'button_)']:
            if Const.equation == '' and clicked_button != 'button_log':
                return '', 'you cannot set an operations in first place of equation', True, num
            else:
                Const.list_equation.append(opartion)
                Const.equation += opartion
                Const.list_show_equation.append(opartion)
                Const.show_equation += opartion
            return Const.show_equation, '', False, num

    # ========================================== end here =============================================

    # new callback the handel the calculation based on the inputs and ave it at table(id, var , value)
    @app.callback(Output("variable", "children"),
                  Input("date-from", "value"),
                  Input("date-to", "value"),
                  Input("filed", "checked"),
                  Input('wells-selection', 'value'),
                  Input("calculated_data", "value"),
                  Input("variable_name", "value"),
                  Input('sbmt', 'n_clicks'),
                  State("variable", "children"), )
    def create_variable(datefrom, dateto, filed, wells_selection, calculated_data, var,
                        n_clicks, current_children):
        db = DatabaseConnection()
        # sbmt = dash.ctx.triggered_id
        print("in create var")
        button_id = dash.ctx.triggered_id
        if button_id == "sbmt":
            print('in create var')
            if filed:
                button_var = dbc.Button(f'{var}', id={"type": "button", "index": n_clicks}, n_clicks=0, size="sm",
                                        color="primary", style={"margin-top": "3px"}),

                esp_data_df = db.get_all_esp_data(filed, datefrom, dateto, wells_selection)
                if calculated_data == "Discharge Pressure":
                    discharge_df = esp_data_df.select(pl.col("DT", "DischargePressure", "well")).sort("DT",
                                                                                                      descending=True)
                    plot_data = discharge_df.with_columns(pl.col("DT").str.to_datetime().dt.strftime("%Y-%m-%d")).sort(
                        "DT", descending=True)

                    var_obj = Var(discharge_df)
                    print(var_obj.data_df)
                    Var.data[f"{n_clicks}"] = var_obj
                    print("--------------------------------")
                    print(Var.data)
                    return current_children + [dbc.Col(html.Div(button_var), width=1)]

                if calculated_data == "Average Amps":
                    avg_amps_df = esp_data_df.select(pl.col("DT", "AverageAmps", "well")).sort("DT", descending=True)
                    plot_data = avg_amps_df.with_columns(pl.col("DT").str.to_datetime().dt.strftime("%Y-%m-%d")).sort(
                        "DT", descending=True)

                    var_obj = Var(avg_amps_df)
                    print(var_obj.data_df)
                    Var.data[f"{n_clicks}"] = var_obj
                    print("--------------------------------")
                    print(Var.data)
                    return current_children + [dbc.Col(html.Div(button_var), width=1)]

                if calculated_data == "Drive Frequency":
                    plot_data = esp_data_df.select(pl.col("DT", "DriveFrequency")).sort("DT", descending=True)

                    var_obj = Var(plot_data)
                    print(var_obj.data_df)
                    Var.data[f"{n_clicks}"] = var_obj
                    print("--------------------------------")
                    print(Var.data)
                    return current_children + [dbc.Col(html.Div(button_var), width=1)]

                if calculated_data == "Intake Pressure":
                    plot_data = esp_data_df.select(pl.col("DT", "IntakePressure")).sort("DT", descending=True)

                    var_obj = Var(plot_data)
                    print(var_obj.data_df)
                    Var.data[f"{n_clicks}"] = var_obj
                    print("--------------------------------")
                    print(Var.data)
                    return current_children + [dbc.Col(html.Div(button_var), width=1)]

                if calculated_data == "Intake Temperature":
                    plot_data = esp_data_df.select(pl.col("DT", "IntakeTemperature")).sort("DT", descending=True)

                    var_obj = Var(plot_data)
                    print(var_obj.data_df)
                    Var.data[f"{n_clicks}"] = var_obj
                    print("--------------------------------")
                    print(Var.data)
                    return current_children + [dbc.Col(html.Div(button_var), width=1)]

                if calculated_data == "Motor Temperature":
                    plot_data = esp_data_df.select(pl.col("DT", "MotorTemperature")).sort("DT", descending=True)

                    var_obj = Var(plot_data)
                    print(var_obj.data_df)
                    Var.data[f"{n_clicks}"] = var_obj
                    print("--------------------------------")
                    print(Var.data)
                    return current_children + [dbc.Col(html.Div(button_var), width=1)]
        else:
            raise PreventUpdate

    @app.callback(
        Output('var_index_show', 'value'),
        Input({"type": "button", "index": ALL}, "n_clicks"),  # Match any button with "type": "button"
    )
    def set_index(button):
        triggered_id = dash.ctx.triggered_id
        return triggered_id["index"]

    @app.callback(
        Output("analysis-table", "children"),
        Output("analysis-chart", "children"),
        Output("df-value", "children"),
        Input("tabs", "value"),
        Input({"type": "button", "index": ALL}, "n_clicks"),  # Match any button with "type": "button"
        State("analysis-table", "children"),
        State("analysis-chart", "children"),
    )
    def update_output(active, n_clicks_list, table, chart_data):
        # Access clicked button's index using ctx.triggered_id
        triggered_id = dash.ctx.triggered_id
        print("active", active)
        print(n_clicks_list)
        if triggered_id and active == "1":
            clicked_index = triggered_id["index"]

            _data_df = Var.data[f"{clicked_index}"]
            result = _data_df.data_df
            json_data = result.to_pandas()
            json_data = json_data.to_json()
            print(triggered_id)
            print(_data_df.data_df)

            column_names = result.columns

            well_values = result["well"].unique()
            split_df_dict = result.partition_by('well', as_dict=True)  # Create dictionary of DataFrames

            # Define trace objects with dynamic colors
            traces = []
            for well in well_values:
                df = split_df_dict[f"{well}"]
                print("********************************************")
                print(df)
                trace = go.Scatter(
                    x=df[f'{column_names[0]}'],
                    y=df[f'{column_names[1]}'],
                    mode='lines',  # Define line style
                    # line=dict(color=item['color']),  # Set color dynamically
                    name=well  # Optional name for legend
                )
                traces.append(trace)

            fig = go.FigureWidget(data=traces)
            result = result.to_pandas()
            result = result.to_dict('records')
            data_table = dash_table.DataTable(result,
                                              page_size=10,
                                              style_table={'overflowY': 'auto',
                                                           # 'width' : '200px',
                                                           'overflowX': 'auto'}
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
            # create chart controller
            selected_xaxis = dmc.Select(
                label="Select xaxis",
                placeholder="Select xaxis",
                id='xaxis',
                data=[{'label': i, 'value': i} for i in column_names[0:2]],
                style={"marginBottom": 10},
                value=f'{column_names[0]}',
            )

            selected_yaxis = dmc.Select(
                label="Select yaxis",
                placeholder="Select yaxis",
                id='yaxis',
                data=[{'label': i, 'value': i} for i in column_names[0:2]],
                style={"marginBottom": 10},
                value=f'{column_names[1]}',
            )

            chart_mode = dmc.Select(
                label="Chart mode",
                placeholder="Chart Mode",
                id='chart_mode',
                data=[
                    {'label': 'markers', 'value': 'markers'},
                    {'label': 'Lines', 'value': 'lines'},
                    {'label': 'Line and Markers', 'value': 'lines+markers'},

                ],
                style={"marginBottom": 10},
                value='line',
            )

            show = dbc.Button('show', id='show', n_clicks=0, size="sm", color="primary", ),

            print(f"Button with index {clicked_index} was clicked!")

            chart_layout = [
                # dcc.Store(id="dataframe-store", data=json_data),

                html.Div([
                    dbc.Col([
                        dbc.Card(
                            [
                                dbc.Row([

                                    dbc.Col(selected_xaxis, width=2),
                                    dbc.Col(selected_yaxis, width=3),
                                    dbc.Col(chart_mode, width=3),
                                    dbc.Col(period, width=2),
                                    dbc.Col(show, width=2, style={'margin-top': '2rem'}),

                                ], align="center", ),
                                dbc.Row(dcc.Graph(figure=fig, id="fig-analysis"))
                            ], body=True), ])
                ])
            ]

            return [data_table, chart_layout, json_data]
        else:
            raise PreventUpdate

    @app.callback(Output("fig-analysis", "figure"),
                  Input('yaxis', 'value'),
                  Input("xaxis", "value"),
                  Input("chart_mode", "value"),
                  Input("period", "value"),
                  Input('show', 'n_clicks'),
                  Input("df-value", "children"),
                  # State('dataframe-store', 'data'),
                  prevent_initial_call=True)
    def update_analysis_chart(yaxis, xaxis, chart_mode, period, n_clicks, df):
        triggered_id = dash.ctx.triggered_id
        print(triggered_id)

        if triggered_id == "show":
            match period:
                case "daily":
                    print(df)
                    # Convert the JSON string to a Python dictionary
                    data = json.loads(df)
                    # Create a Pandas DataFrame from the dictionary
                    final = pd.DataFrame(data)
                    pl_df = pl.from_pandas(final)
                    column_names = pl_df.columns
                    print(column_names)

                    # pl_df = pl_df.with_columns(pl.col("DT").str.to_datetime().dt.day()).sort("DT", descending=True)
                    # strftime("%Y-%m-%d")).sort("DT", descending=True)
                    pl_df = pl_df.group_by(
                        [pl.col("DT").str.to_datetime().dt.strftime("%Y-%m-%d"), pl.col("well")]).agg(
                        pl.col(f"{column_names[1]}").sum(),
                    )

                    well_values = pl_df["well"].unique()
                    split_df_dict = pl_df.partition_by('well', as_dict=True)  # Create dictionary of DataFrames

                    traces = []
                    for well in well_values:
                        clean_df = split_df_dict[f"{well}"]
                        print("********************************************")
                        print(clean_df)
                        trace = go.Scatter(
                            x=clean_df[xaxis],
                            y=clean_df[yaxis],

                            mode=f'{chart_mode}',  # Define line style
                            # line=dict(color=item['color']),  # Set color dynamically
                            name=well  # Optional name for legend
                        )
                        traces.append(trace)

                    fig = go.FigureWidget(data=traces)
                    match chart_mode:
                        case "markers":
                            fig.update_traces(
                                marker=dict(size=30, symbol="diamond", line=dict(width=10, color="DarkSlateGrey")),
                                selector=dict(mode="markers"),
                            )

                        case "lines+markers":
                            fig.update_traces(
                                marker=dict(symbol="arrow", size=2, angleref="previous", ),
                                selector=dict(mode="lines+markers"),
                            )

                    return fig

                case "weekly":
                    print(df)
                    # Convert the JSON string to a Python dictionary
                    data = json.loads(df)
                    # Create a Pandas DataFrame from the dictionary
                    final = pd.DataFrame(data)
                    pl_df = pl.from_pandas(final)
                    column_names = pl_df.columns
                    print(column_names)

                    # pl_df = pl_df.with_columns(pl.col("DT").str.to_datetime().dt.day()).sort("DT", descending=True)
                    # strftime("%Y-%m-%d")).sort("DT", descending=True)
                    pl_df = pl_df.group_by(
                        [pl.col("DT").str.to_datetime().dt.week(), pl.col("well")]).agg(
                        pl.col(f"{column_names[1]}").sum(),
                    )

                    well_values = pl_df["well"].unique()
                    split_df_dict = pl_df.partition_by('well', as_dict=True)  # Create dictionary of DataFrames
                    traces = []
                    for well in well_values:
                        clean_df = split_df_dict[f"{well}"]
                        print("********************************************")
                        print(clean_df)
                        trace = go.Scatter(
                            x=clean_df[xaxis],
                            y=clean_df[yaxis],

                            mode=f'{chart_mode}',  # Define line style
                            # line=dict(color=item['color']),  # Set color dynamically
                            name=well  # Optional name for legend
                        )
                        traces.append(trace)

                    fig = go.FigureWidget(data=traces)
                    match chart_mode:
                        case "markers":
                            fig.update_traces(
                                marker=dict(size=3, symbol="diamond", line=dict(width=1, color="DarkSlateGrey")),
                                selector=dict(mode="markers"),
                            )

                        case "lines+markers":
                            fig.update_traces(
                                marker=dict(symbol="arrow", size=2, angleref="previous", ),
                                selector=dict(mode="lines+markers"),
                            )

                    return fig

                case "monthly":
                    print(df)
                    # Convert the JSON string to a Python dictionary
                    data = json.loads(df)
                    # Create a Pandas DataFrame from the dictionary
                    final = pd.DataFrame(data)
                    pl_df = pl.from_pandas(final)
                    column_names = pl_df.columns
                    print(column_names)

                    # pl_df = pl_df.with_columns(pl.col("DT").str.to_datetime().dt.day()).sort("DT", descending=True)
                    # strftime("%Y-%m-%d")).sort("DT", descending=True)
                    pl_df = pl_df.group_by(
                        [pl.col("DT").str.to_datetime().dt.month(), pl.col("well")]).agg(
                        pl.col(f"{column_names[1]}").sum(),
                    )

                    well_values = pl_df["well"].unique()
                    split_df_dict = pl_df.partition_by('well', as_dict=True)  # Create dictionary of DataFrames
                    traces = []
                    for well in well_values:
                        clean_df = split_df_dict[f"{well}"]
                        print("********************************************")
                        print(clean_df)
                        trace = go.Scatter(
                            x=clean_df[xaxis],
                            y=clean_df[yaxis],

                            mode=f'{chart_mode}',  # Define line style
                            # line=dict(color=item['color']),  # Set color dynamically
                            name=well  # Optional name for legend
                        )
                        traces.append(trace)

                    fig = go.FigureWidget(data=traces)
                    match chart_mode:
                        case "markers":
                            fig.update_traces(
                                marker=dict(size=3, symbol="diamond", line=dict(width=1, color="DarkSlateGrey")),
                                selector=dict(mode="markers"),
                            )

                        case "lines+markers":
                            fig.update_traces(
                                marker=dict(symbol="arrow", size=2, angleref="previous", ),
                                selector=dict(mode="lines+markers"),
                            )

                    return fig

                case "quarters":
                    print(df)
                    # Convert the JSON string to a Python dictionary
                    data = json.loads(df)
                    # Create a Pandas DataFrame from the dictionary
                    final = pd.DataFrame(data)
                    pl_df = pl.from_pandas(final)
                    column_names = pl_df.columns
                    print(column_names)

                    # pl_df = pl_df.with_columns(pl.col("DT").str.to_datetime().dt.day()).sort("DT", descending=True)
                    # strftime("%Y-%m-%d")).sort("DT", descending=True)
                    pl_df = pl_df.group_by(
                        [pl.col("DT").str.to_datetime().dt.quarter(), pl.col("well")]).agg(
                        pl.col(f"{column_names[1]}").sum(),
                    )

                    well_values = pl_df["well"].unique()
                    split_df_dict = pl_df.partition_by('well', as_dict=True)  # Create dictionary of DataFrames
                    traces = []
                    for well in well_values:
                        clean_df = split_df_dict[f"{well}"]
                        print("********************************************")
                        print(clean_df)
                        trace = go.Scatter(
                            x=clean_df[xaxis],
                            y=clean_df[yaxis],

                            mode=f'{chart_mode}',  # Define line style
                            # line=dict(color=item['color']),  # Set color dynamically
                            name=well  # Optional name for legend
                        )
                        traces.append(trace)

                    fig = go.FigureWidget(data=traces)
                    match chart_mode:
                        case "markers":
                            fig.update_traces(
                                marker=dict(size=3, symbol="diamond", line=dict(width=1, color="DarkSlateGrey")),
                                selector=dict(mode="markers"),
                            )

                        case "lines+markers":
                            fig.update_traces(
                                marker=dict(symbol="arrow", size=2, angleref="previous", ),
                                selector=dict(mode="lines+markers"),
                            )

                    return fig

        else:
            raise PreventUpdate

    return app


if __name__ == "__main__":
    server = flask.Flask(__name__)
    app = create_anna_application(server)
    app.run_server(debug=True)
