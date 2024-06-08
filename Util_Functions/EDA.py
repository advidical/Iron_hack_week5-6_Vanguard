import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

# lines to break up print statements for clarity
end_lines = "\n"+"="*100+"\n"
sep_lines = "\n"+"-"*40+"\n"

def explore_df(df):
    """
    Explores the dataframe via its dims, dtypes, null counts of each column,
    and value counts for each columns

    Arguments: df (pd.Dataframe) - Dataframe to explore
    Returns: None
    """
    print("Dataframe shape: ")
    print(f"{df.shape[0]} rows X {df.shape[1]} columns", end=end_lines)

    print("Dataframe data types")
    print(df.dtypes,end=end_lines)

    print(f"Null Count:")
    null_df = pd.concat([df.isnull().sum(), df.isnull().mean()],axis=1)
    null_df.columns = ['count','normalize_count']
    print(null_df, end=end_lines)

    print(f"{df.columns}", end=end_lines)
    print("Value counts for each column:")
    for col in df.columns:
        print(df[col].value_counts(dropna=False),end=sep_lines)

    print(end_lines)
    print(df.describe(include='all'))

def drop_rows(df, drop_threshold=.8):
    """
      Finds rows that exceed a threshold of null values.
      By default, it returns rows with 80% of col values being null

      Arguments:
        df (pd.Dataframe) - Dataframe to find null threshold rows
        drop_threshold (float[0-1]) - threshold of nulls for which to test
      Returns: dataframe with rows exceeding threshold, which should be dropped
      """
    null_rows = df.isna().mean(axis=1)
    null_rows = null_rows[null_rows > drop_threshold]
    return df.iloc[null_rows.index]

def demo_title(col):
    """
    Helper function to get formatted column names for final demo
    Arguments: col (str) - final demo column to get title
    Returns: formatted column (str)
    """
    if col in ['clnt_tenure_yr', 'clnt_tenure_mnth', 'clnt_age']:
        return col.replace('clnt','client')

    if col == 'gendr':
        return 'Gender'
    if col == 'num_accts':
        return 'Number_of_Accounts'
    if col == 'bal':
        return 'Balance'
    if col == 'calls_6_mnth':
        return 'Calls over 6 Months'
    if col == 'logons_6_mnth':
        return 'Logons over 6 Months'
    return col

def data_demo(df, demographic, title_mod='', only_violin=False, return_plot=False):
    """
      Calculates mean, median, mode, skew, and kurtosis of a demographic
      column from df and displays visuals to determine demographic

      Arguments:
        df (pd.Dataframe)  - Dataframe that has demographic column
        demographic (str)  - column (w/ numeric dtype) to get data for.
        title_mod (str)    - string to add to title data
        only_violin (bool) - specify whether to only return the violin plot
        return_plot (bool) - specifiy to return plot instead of displaying
      
      Returns: None | matplotlib object
    """
    # summary data (central tendency + skew/kurtosis)
    client_demo = df[demographic]
    mean, median, mode = client_demo.mean(), client_demo.median(), client_demo.mode()[0]
    skew, kurtosis= client_demo.skew(), client_demo.kurtosis()
    summary_df = pd.DataFrame({'mean': [mean], 'median': [median], 'mode': [mode],
                               'skew': [skew], 'kurtosis':[kurtosis]})
    print(summary_df, end=sep_lines)

    fig = None
    # title data for charts
    modifier = ' by '+ title_mod if title_mod else ''
    full_title = demo_title(demographic) + modifier

    if only_violin:
        # violin plot
        fig, ax = plt.subplots(figsize=(4, 6))
        sns.violinplot(data=df,y=demographic, color="goldenrod", ax=ax)
    else:
        #  histogram plot,  box plot, & violin plot
        fig, axes = plt.subplots(3, 1, figsize=(6, 8))  # 3 rows, 1 column

        sns.histplot(client_demo, kde=True, color="salmon", ax=axes[0])
        sns.boxplot(data = client_demo, color="lightblue", ax=axes[1])
        sns.violinplot(data=df,y=demographic, color="goldenrod", ax=axes[2])

        axes[0].set_title(f'Histogram with KDE of {full_title}')
        axes[1].set_title(f'Boxplot of {full_title}')
        axes[2].set_title(f'Violin Plot of {full_title}')

    fig.suptitle(f'{full_title}')

    # Adjust layoout
    plt.tight_layout()

    if return_plot:
        return fig

    # Show the plots
    plt.show()

def cat_vs_numerical(df, cat_demo, num_demo):
    """
    Gets Violin plot between categorical demo vs numerical continuous demo
    Arguments: df (pd.Dataframe) - dataframe to get violin plat
               cat_demo (str) - categorical demographic column
               num_demo (str) - numerical demographic column
    """
    sns.violinplot(data=df, x=cat_demo, y=num_demo, palette="coolwarm", hue=cat_demo, legend=False)
    plt.tight_layout()
    plt.show()