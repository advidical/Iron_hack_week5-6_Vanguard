import pandas as pd

step_list = ['start', 'step_1', 'step_2', 'step_3','confirm']

def is_step_success(current_step, previous_step):
    step_orders = {name : i for i, name in enumerate(step_list)}
    return step_orders[current_step] == step_orders[previous_step] + 1

def get_kpis(df, id='client_id'):
    """
    Calculates how many clients in test/control group performed the steps and
    reached the confirm step, how long clients spent on each step on average,
    and the average error rate(how many times went back to a previous step).

    Note: any steps repeated that get completed successfully will be added to
    clients total time on that step.

    Argument: df (pd.DataFrame) - the dataframe to processs confirmation rate
              id (str) - group id for the dataframe
    Returns : None - Prints the confirmation rate
    """

    client_process = [] # list of process duration & error counts
    total_steps = 0
    group = df['variation'].unique()[0] # get group of client data

    # check confirm kpi on entries with at least one successful set of steps
    confirmed = 0 # get other confirm rate based on actually reaching it
    for gid, group_data in df.groupby(id):
        group_data = group_data.sort_values(by='date_time')

        confirm_once = False

        # Get time duration diffs and error counts
        time_process_df = group_data[['date_time','process_step']]
        time_process_df = time_process_df.reset_index(drop=True)
        time_process_df = time_process_df.sort_values(by='date_time',ignore_index=True)
        time_process_df['time_diff'] = time_process_df['date_time'].diff()

        client_dict = dict()
        client_dict[id] = gid
        client_dict['error_count'] = 0
        total_steps += len(time_process_df)

        for index, time_log in time_process_df.iterrows():
            if index == 0: continue

            curr_step = time_log['process_step']
            prev_step = time_process_df.iloc[index-1]['process_step']
            if not is_step_success(curr_step, prev_step):
                client_dict['error_count'] += 1
                continue
            client_dict[prev_step] = client_dict.get(prev_step, pd.Timedelta(0)) + \
                                     time_log['time_diff']
            if curr_step == 'confirm': confirm_once = True


        confirmed += int(confirm_once)
        client_process.append(client_dict)

    process_data = pd.DataFrame(client_process) # needed to calculate aggregations
    total_size = len(df.groupby(id).size())
    completion_rate = confirmed / total_size

    return pd.DataFrame({'group': group, 'confirm_count': confirmed, 'total_size': total_size, \
                         'completion_rate': completion_rate,
                         'start_mean': process_data['start'].mean().round('1s'),
                         'step_1_mean': process_data['step_1'].mean().round('1s'),
                         'step_2_mean': process_data['step_2'].mean().round('1s'),
                         'step_3_mean': process_data['step_3'].mean().round('1s'),
                         'error_rate' : process_data['error_count'].sum() / total_steps,
                        }, index = [0])