import pandas as pd
import numpy as np
from scipy import stats as st
from statsmodels.stats.proportion import proportions_ztest

import os

from EDA import demo_title

# lines to break up print statements for clarity
end_lines = "\n"+"="*100+"\n"
sep_lines = "\n"+"-"*40+"\n"

def populate(row):
    confirms = row['confirm_count']
    not_confirms = row['total_size'] - confirms

    # Generate array and shuffle it
    data = np.concatenate((np.ones(confirms), np.zeros(not_confirms)))
    np.random.shuffle(data)
    return data

# Unit function from get_kpis
def completed_or_not(id):
    """
    Gets completion data from dataframe and fill it for hypothesis testing
    args: id - which grouped kpi to get from: client_id, visitor_id, visit_id
    returns: test/control complete np arrays
    """
    metric_folder = './metric_files/'
    data_file = os.path.join(metric_folder, f'KPI_Metrics_{id}.pkl')

    data = pd.read_pickle(data_file)
    test_row, control_row = data[data['group'] == 'Test'], data[data['group'] == 'Control']

    test_completion = populate(test_row)
    control_completion = populate(control_row)

    return test_completion, control_completion

def completion_with_cost_threshold(test_completion, control_completion, cost_threshold=.05, alpha=.05):
    """
    Performs one_sided proportion z test for datasets split by test/control groups,
    with cost threshold to increase control group by to check if test still hase 
    statisically greater average than the control group

    Arguments : test_completion (pd.DataFrame/np.array) - Test group data
                control_completion (pd.DataFrame/np.array) - control group data
                cost_threshold (float) - the threshold to test for
                alpha (float) - the test threshold

    Returns : z_stat(float) & p_value(float)
    """
    successes = np.array([test_completion.sum(),
                          control_completion.sum() + (len(control_completion) * cost_threshold)])  # number of successes in each group
    trials = np.array([len(test_completion), len(control_completion)])      # total trials in each group

    # Perform z-test
    z_stat, p_value = proportions_ztest(successes, trials, alternative='larger')

    # Interpret results
    print("Z-statistic:", z_stat)
    print("P-value:", p_value)
    if p_value < alpha:
        print("Reject null hypothesis: The completion_rate in the test group is greater than the proportion in the control group.")
    else:
        print("Fail to reject null hypothesis: There is no significant difference in completion_rates between the two groups.")
    print()
    return z_stat, p_value

# test whether the average age of clients engaging with the new process is the same as those engaging with the old process
def test_demo_groups(df, demographic, alt='two-sided'):
    """
    Run two sample tests to compare test and control groups 
    Arguments : df (pd.DataFrame) - df to test
                demographic (str) - demograhic in df to test
                alt (str)         - option for what to test for
    Returns: None
    """
    test_age_group = df[df['variation'] == 'Test'][demographic]
    control_age_group = df[df['variation'] == 'Control'][demographic]

    test_age_group = test_age_group.dropna()
    control_age_group = control_age_group.dropna()
    a = 0.05
    stat, p_value = st.ttest_ind(test_age_group, control_age_group, alternative=alt, equal_var=False)

    print(f"{stat = }, {p_value = }")
    name = demo_title(demographic)
    cond = True
    cond_msg = f"the average {name} across the test/control groups aren't the same"
    if alt != 'two-sided':
        if alt == 'greater':
            cond = stat > 0
            cond_msg = f"the average {name} in test group is greater than the control group"
        if alt == 'less':
            cond = stat < 0
            cond_msg = f"the average {name} in test group is less than the control group"

    if p_value < a and cond:
        print(f"Reject the null hypothesis: {cond_msg}")
    else:
        print(f"Fail to reject: the average {name} across the test/control groups are probably the same")

def anova_gender_test(data, demo, group, alpha = .05):
    """
    Anova test to test dataframe demographics across test/control groups

    Arguments : data (pd.DAtaframe) - dataframe to test
                demo (str)          - demograhic in df to test
                group (str)         - representing which group (Test/Control)
                alpha (float)       - the test threshold
    Returns: None
    """

    #H0: mu unspecified gender = mu male = mu female
    #H1: mu unspecified gender != mu male != mu female
    unspecified_gender = data[(data['gendr']=='U') & (data['variation'] == group)][demo]
    male = data[(data['gendr']=='M') & (data['variation'] == group)][demo]
    female = data[(data['gendr']=='F') & (data['variation'] == group)][demo]

    # make sure any nan values are dropped
    unspecified_gender = unspecified_gender.dropna()
    male = male.dropna()
    female = female.dropna()

    z_stat, p_value = st.f_oneway(unspecified_gender , male, female)

    demo_msg = demo_title(demo)
    print(f"For the {group} group")
    print(f"{z_stat = }, {p_value = }")
    if p_value < alpha:
        print(f"Reject the null hypothesis: Across gender there is significant difference in {demo_msg}")
    else:
        print(f"Fail to reject: the average {demo_msg} across the gender groups are probably the same")
    print(sep_lines)