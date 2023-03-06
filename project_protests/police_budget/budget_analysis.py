import pandas as pandas
import re 
import pathlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Monica Nimmagadda #

def load_budget_data():
    budget_filepath = pathlib.Path(__file__).parent / "police_budget_by_city.csv"
    budget_df = pd.read_csv(budget_filepath)
    cols = budget_df.columns
    for col in cols[2:-1]:
        budget_df[col] = budget_df[col].astype(float)
    budget_df = project_population(budget_df)
    # visualize_budget(budget_df)
    return budget_df

def project_population(df):
    for row in df.itertuples():
        if row.Type == 'Population':
            fy_21 = row.FY21
            fy_20 = row.FY20
            percent_change = (fy_21 - fy_20) / fy_20
            fy_22 = fy_21 + (fy_21 * percent_change)
            df.loc[row.Index, 'FY22'] = fy_22
            fy_23 = fy_22 + (fy_22 * percent_change)
            df.loc[row.Index, 'FY23'] = fy_23
    
    return df

def normalize_budget():
    df = load_budget_data()
    df.sort_values(by=['City', 'Type'], ascending=False, inplace=True)
    
    return df

def visualize_budget(df):
    df_population = df.loc[df['Type'] == 'Population']
    df_budget = df.loc[df['Type'] == 'Total']
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter( 
            x=df_budget['City'],
            y=df_budget[df_budget.columns[2:9]], 
            name="Budget"
        ), secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df_population['City'],
            y=df_population[df_population.columns[2:9]], 
            name="Population"
        ), secondary_y=True,
    )
    fig.update_yaxes(title_text="Budget ($)", secondary_y=False)
    fig.update_yaxes(title_text="Population (#)", secondary_y=True)
    fig.show()


