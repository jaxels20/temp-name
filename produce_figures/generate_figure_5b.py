import plotly.graph_objects as go
import pandas as pd


INPUT_FILE = "./data/figure_5b/data.csv"
OUTPUT_PATH = "./figures/figure_5b.pdf"

def plot_df(df):
    fig = go.Figure()
    color = "lightgrey"

    # Compute IQR per Dataset
    iqr_df = (
        df.groupby('Dataset')['Score']
        .agg(lambda x: x.quantile(1) - x.quantile(0))
        .reset_index(name='IQR')
    )

    # Sort datasets by IQR
    sorted_datasets = iqr_df.sort_values('IQR')['Dataset'].tolist()

    fig.add_trace(go.Scatter(
        x=df['Dataset'],
        y=df['Score'],
        mode='markers',
        name='Objective Fitness',
        marker=dict(color=color, size=6, line=dict(width=1, color='black'))
    ))

    # Update x-axis order
    fig.update_layout(
        xaxis=dict(categoryorder='array', categoryarray=sorted_datasets)
    )

    # Layout adjustments
    fig.update_layout(
        boxmode='group',  # group boxes of same x-axis value
        font=dict(family='Times', size=16),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            xanchor='center',
            y=1.05,        # slightly above the top of the plot
            x=0.5
        ),
        xaxis_title='Dataset',
        yaxis_title='Objective Fitness',
        margin=dict(l=60, r=30, t=50, b=120),
        template='simple_white',
        height=500,
        width=900
    )
    # set the y axisto 0 to 1
    fig.update_yaxes(range=[60, 100], dtick=10)
    
    # Rotate x-axis labels
    fig.update_xaxes(tickangle=45, tickmode='array', tickvals=sorted_datasets)
    
    # save the plot
    fig.write_image(OUTPUT_PATH)


if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)
    plot_df(df)