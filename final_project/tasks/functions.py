import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_df(key):
    return df_responses.iloc[df_orgs_private_grouped.groups[key]]


def get_methods(obj):
    # Getting all methods from the groupby object:
    meth=[method_name for method_name in dir(obj) if callable(getattr(obj, method_name)) & ~method_name.startswith('_')]

    # Printing the result
    print(IPython.utils.text.columnize(meth))


def get_model_group_indices(group):
    return df_model.groupby(['dim', 'lvl']).groups[group[0], int(group[1])]


def get_levels(df_responses_group, dim):
    df_dim=pd.DataFrame()
    for lvl in dict_mod[dim]:
        df_dim[lvl]=df_responses_group[dict_mod[dim][lvl]].mean(axis=1)

    df_dim[df_dim.apply(lambda x: x >= 5)]=0
    df_dim['max']=df_dim.apply(lambda row: next((i for i, x in enumerate(row) if x), None), axis=1)

    df_dim[df_dim.isna()]=0
    df_dim['partial']=df_dim.apply(lambda row: 0.25 * (-1+row[int(row[['max']])+1]), axis=1)
    df_dim['level']=df_dim.apply(lambda row: row['max']+row['partial']+1, axis=1)

    # df_dim = df_dim['level']
    df_dim['level'][df_dim['level']==0.75]=5.0
    df_dim=df_dim[['level']]
    return df_dim


def analyze(df_responses):
    df=df_responses
    for dim in dimensions:
        df[dim]=get_levels(df_responses, dim)
    df=df[dimensions]
    return df


def rank_plot(df):
    fig, ax=plt.subplots(len(df.keys()), figsize=(10, 50))
    fig.subplots_adjust(hspace=0.5)
    #     fig.

    for i, key in enumerate(list(df.keys())):
        ax[i].bar(df[key]['name'].values, df[key]['overall'].values)
        ax[i].set_title('{}'.format(str(key)))
        ax[i].set_xlabel('x_label')  #         ax[i].set_xticks(rotation=70)

