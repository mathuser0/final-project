from csci_utils.luigi.target import SuffixPreservingLocalTarget
from csci_utils.luigi.data import DownloadModel, DownloadImage, DownloadContent
from luigi.format import Nop
import os
from luigi import Task, Parameter,ExternalTask
import pandas as pd
import numpy as np


class Responses(ExternalTask):
    def output(self):
        return SuffixPreservingLocalTarget('data/responses/responses.xlsx', format=Nop)

class Organizations(ExternalTask):
    def output(self):
        return SuffixPreservingLocalTarget('data/organizations/organization_table.csv', format=Nop)

class Model(ExternalTask):
    def output(self):
        return SuffixPreservingLocalTarget('data/models/model.csv', format=Nop)

class Analyze(Task):
    def requires(self):
        return {'model':Model(),
        'responses':Responses(),
        'orgs':Organizations()}

    def output(self):
        return SuffixPreservingLocalTarget('data/results/df_entire.csv', format=Nop)

    def run(self):
        inputs = self.input()
        output=self.output()

        df_model=pd.read_csv(inputs['model'].path)
        df_responses=pd.read_excel(inputs['responses'].path, header=None)
        df_orgs=pd.read_csv(inputs['orgs'].path)

        dimensions=df_model.dim.unique()
        levels=df_model.lvl.unique()
        print(dimensions)
        print(levels)


        def get_model_group_indices(group):
            return df_model.groupby(['dim', 'lvl']).groups[group[0], int(group[1])]

        model_groups=np.array([[(dim, lvl) for lvl in levels] for dim in dimensions]).reshape(-1, 2)

        model_group_indices=np.array(list(map(get_model_group_indices, model_groups)))+1

        dict_mod=dict()
        for i, dim in enumerate(dimensions):
            dict_lvl=dict()
            for k, lvl in enumerate(levels):
                dict_lvl[lvl]=model_group_indices[i * len(levels)+k]
                dict_mod[dim]=dict_lvl

        def get_levels(df_responses_group, dim):
            df_dim=pd.DataFrame()
            for lvl in dict_mod[dim]:
                df_dim[lvl]=df_responses_group[dict_mod[dim][lvl]].mean(axis=1)

            df_dim[df_dim.apply(lambda x: x >= 5)]=0
            df_dim['max']=df_dim.apply(lambda row: next((i for i, x in enumerate(row) if x), None), axis=1)

            df_dim[df_dim.isna()]=0
            df_dim['partial']=df_dim.apply(lambda row: 0.25 * (-1+row[int(row[['max']])+1]), axis=1)
            df_dim['level']=df_dim.apply(lambda row: row['max']+row['partial']+1, axis=1)

            df_dim['level'][df_dim['level']==0.75]=5.0
            df_dim=df_dim[['level']]
            return df_dim

        def analyze(df_responses):
            df=df_responses
            for dim in dimensions:
                df[dim]=get_levels(df_responses, dim)
            df=df[dimensions]
            df['overall']=df.mean(axis=1)
            return df

        df_analyzed=analyze(df_responses)
        df_entire=df_analyzed.join(df_orgs)
        df_entire.to_csv(output.path)

class Classify(Task):

    def requires(self):
        return {'entire':Analyze(),
        'orgs':Organizations()}

    def output(self):
        df_orgs=pd.read_csv(self.input()['orgs'].path)
        dfs_orgs_grouped=df_orgs.groupby(['is_public', 'industry']).groups
        org_keys=list(df_orgs.groupby(['is_public', 'industry']).groups.keys())

        return SuffixPreservingLocalTarget('data/results/SUCCESS')

    def run(self):
        df_orgs=pd.read_csv(self.input()['orgs'].path)
        dfs_orgs_grouped=df_orgs.groupby(['is_public', 'industry']).groups
        org_keys=list(df_orgs.groupby(['is_public', 'industry']).groups.keys())
        df_entire = pd.read_csv(self.input()['entire'].path)

        for key in org_keys:
            df_entire.loc[dfs_orgs_grouped[key]].sort_values('overall').to_csv('data/results/df2_{}.csv'.format(str(key[0])+'_'+key[1]))


        with self.output().open('w') as f:
            pass

