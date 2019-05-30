import pandas as pd
import numpy as np

nonce = 'kelilili'

class sess():

    def __init__(self, needs_doc=None, dataframe=pd.DataFrame()):
        if dataframe.empty == False:
            self.df=dataframe
        else:
            self.df = pd.read_csv(needs_doc)

        self.class_features = []
        self.class_name = []
        self.trainees_names = {}

        self.build_classes()
        super(sess, self).__init__()

    def build_classes(self):
        for i in list(self.df)[1:]:
            people = self.df[list(self.df)[0]].loc[self.df[i].isin([str(1)])]
            if len(people) > 0:
                self.class_name.append(i)
                self.class_features.append([len(people)])
                self.trainees_names[i] = list(people.unique())

    def find_trainees(self, class_name):
        return class_name, self.trainees_names[class_name]

    def find_training_needed(self, trainee):
        loc = self.df[list(self.df)[0]].isin([trainee])
        bools = list(loc.isin([str(1)]))

        ct=0
        indeces=[]
        for it in bools:
            if it:
                indeces.append(ct)
            ct+=1

        training_needed = [list(self.df)[i] for i in indeces]
        return training_needed