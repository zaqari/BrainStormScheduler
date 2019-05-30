import pandas as pd
import numpy as np

nonce = 'kelilili'

class query():

    def __init__(self, staff_skillsets='input-data/skills.csv', courses='input-data/staff-1w.csv', required_skills='input-data/class_by_topic_1w.csv'):
        self.dfr=pd.read_csv(required_skills)
        self.dfc=pd.read_csv(courses)
        self.dfs=pd.read_csv(staff_skillsets)

        #clean skills sheet
        self.dfs = self.dfs.replace(to_replace=['N', 'n', 'r', 'R'], value=1)
        self.dfs = self.dfs.fillna(1)
        self.dfs = self.dfs.replace(to_replace=['Y', 'y'], value=0)
        self.dfr.fillna(nonce)

        ct=0
        self.skills_axes = {}
        for skill in self.dfs[list(self.dfs)[0]].unique():
            self.skills_axes[skill]=ct
            ct+=1

        self.training_matrices = []

        self.n_matrices=0
        self.staffID = {}
        for name in list(self.dfs)[1:]:
            self.training_matrices.append([0 for _ in range(len(self.skills_axes))])
            self.staffID[name]=self.n_matrices
            self.n_matrices+=1

        self.build()

        super(query, self).__init__()

    def swap_courses(self, new_courses_offered_worksheet, new_required_skills_worksheet):
        self.dfc = pd.read_csv(new_courses_offered_worksheet)
        self.dfr = pd.read_csv(new_required_skills_worksheet)
        self.dfr.fillna(nonce)
        self.build()

    def build(self):
        for name in list(self.dfs)[1:]:
            skills = self.dfs[[name, 'Can You\rTeach It?']]

            requirements = []
            for loc in self.dfc.index:
                if name in self.dfc[['instructor', 'assistant1', 'assistant2']].loc[loc].values.tolist():
                    course_reqs = self.dfr[list(self.dfr)[1:]].loc[self.dfr['CLASS NAME'].isin([self.dfc['course'].loc[loc]])]
                    for l in course_reqs.values.tolist():
                        requirements += l

            needs = skills.loc[skills['Can You\rTeach It?'].isin(list(set(requirements)))]

            for l in needs.index:
                try:
                    self.training_matrices[self.staffID[name]][self.skills_axes[needs['Can You\rTeach It?'].loc[l]]] = needs[name].loc[l]
                except KeyError:
                    self.staffID[name] = self.n_matrices
                    self.training_matrices.append([0 for _ in range(len(self.skills_axes))])
                    self.n_matrices+=1

                    self.training_matrices[self.staffID[name]][self.skills_axes[needs['Can You\rTeach It?'].loc[l]]] = needs[name].loc[l]

    def matrices_to_csv(self, filename):
        data = []
        for n in self.staffID.keys():
            a=[n]
            a+=self.training_matrices[self.staffID[n]]
            data.append(a)

        df = pd.DataFrame(np.array(data).reshape(-1, len(self.skills_axes)+1), columns=['staff']+list(self.skills_axes.keys()))
        df.to_csv(filename+'.csv', index=False, encoding='utf-8')
        return df