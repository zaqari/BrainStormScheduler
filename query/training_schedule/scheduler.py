import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import query.training_schedule.training_matrices as ts

class scheduler():

    def __init__(self, new_session=[]):
        self.staff_conflicts = {}
        self.topicID = {}
        self.rev_topicID = {}
        self.concurrence_dic = {}
        #If '0' in position, then classes cannot run concurrently. If '1'
        # then class is safe to be run concurrently.
        self.conflict_matrices = []

        if bool(new_session):
            q1 = ts.query(courses=new_session[0][1],
                          required_skills=new_session[0][2])
            if len(new_session) > 1:
                for i in new_session[1:]:
                    q1.swap_courses(courses=new_session[i][1],
                                    required_skills=new_session[i][2])
            fluff = q1.matrices_to_csv('alltraining.csv')

        super(scheduler, self).__init__()

    #Pass this a list of people
    def trainee_names_conflict(self, topic1, topic2):
        a = set(topic1).intersection(set(topic2))
        self.staff_conflicts = {i: [topic1, topic2] for i in a}
        return self.staff_conflicts

    #pass topics as 1-hot arrays, where each "row" is a participant
    # in the training ... a staff member.
    def cosine_concurrency(self, topic1, topic2):
        a, b = np.array(topic1).reshape(1, -1), np.array(topic2).reshape(1, -1)
        result = cosine_similarity(a, b)
        if result[-1][-1] == 0.0:
            return True
        else:
            return False

    # goes through a document where you have staff training skills
    # identified and returns what topics can be taught concurrently
    def cosine_concurrency_doc(self, df, min_participants=3):
        df[list(df)[1:]].astype(float)

        ignore_cols = [col for col in list(df)[1:] if sum(df[col].values.tolist()) < min_participants]
        columns = [col for col in list(df)[1:] if sum(df[col].values.tolist()) >= min_participants]

        self.topicID = {col: columns.index(col) for col in columns}
        self.rev_topicID = {v: k for k, v in self.topicID.items()}
        self.conflict_matrices = [[0 for _ in range(len(columns))] for i in range(len(columns))]

        can_be_concurrent_dic = {}
        for col in columns:
            conflicts = list(columns)
            conflicts.remove(col)
            good = [conflict for conflict in conflicts if self.cosine_concurrency(df[col].values.tolist(), df[conflict].values.tolist())]
            can_be_concurrent_dic[col] = good
        self.concurrence_dic = can_be_concurrent_dic

        for k, v in can_be_concurrent_dic.items():
            for val in v:
                self.conflict_matrices[self.topicID[k]][self.topicID[val]] = 1


    #Takes an nD matrix of 1-hot vectors indicating topics that can
    # be taught concurrently and belts out a hypothetical schedule
    # according to the number of rooms available.
    def create_schedule_using_conflict_matrices(self, n_rooms=6):
        nrooms = n_rooms-1
        schedule = []
        already_sorted=set()
        rev_topicID = dict(self.rev_topicID)

        if bool(self.conflict_matrices) == False:
            self.cosine_concurrency_doc(pd.read_csv(input('Enter the path to your staff_x_training needs .csv file here: ')))

        ct=0
        for m in self.conflict_matrices:
            if ct in rev_topicID.keys():
                should_run = np.argpartition(np.array(m), -nrooms)[-nrooms:][:nrooms]
                topics = [rev_topicID[ct]]
                for i in should_run:
                    try:
                        topics.append(rev_topicID[i])
                        del rev_topicID[i]
                    except KeyError:
                        already_sorted.add(i)
                if len(topics) < nrooms+1:
                    topics += ['_' for _ in range(int(nrooms+1)-len(topics))]
                del rev_topicID[ct]
                already_sorted.add(ct)
                schedule.append(topics)
            ct+=1

        dfsched = pd.DataFrame(np.array(schedule).reshape(-1, nrooms+1), columns=['topic'+str(i+1) for i in range(nrooms+1)])
        dfsched = dfsched.loc[~dfsched['topic2'].isin(['_'])].copy()
        dfsched.index = range(len(dfsched))
        return dfsched

    def create_schedule(self, n_rooms=6, verbose=False):

        out_data=[]
        already_out=set()

        data = []
        for k, v in self.concurrence_dic.items():
            if len(v) > 0:
                for val in v:
                    data.append([k, val])
        df = pd.DataFrame(np.array(data).reshape(-1, 2), columns=['t1', 't2'])

        ts = list(df['t1'].unique())
        for topic in ts:
            a = [topic]
            b = df['t2'].loc[df['t1'].isin([topic])].unique()

            ct=0
            for it in b:
                if ct <= n_rooms-1:
                    if it in ts:
                        a3 = set(df['t2'].loc[df['t1'].isin([it])].unique())
                        if len(a3.intersection(set(a))) == len(set(a)):
                            a.append(it)
                            try:
                                ts.remove(it)
                            except ValueError:
                                already_out.add(it)
                ct+=1

            if len(a) < n_rooms:
                a+=['_' for _ in range(n_rooms-len(a))]
            out_data.append(a)

            try:
                ts.remove(topic)
            except ValueError:
                already_out.add(topic)

        if verbose:
            return already_out, pd.DataFrame(np.array(out_data).reshape(-1, n_rooms), columns=['topic'+str(i+1) for i in range(n_rooms)])
        else:
            return pd.DataFrame(np.array(out_data).reshape(-1, n_rooms), columns=['topic' + str(i + 1) for i in range(n_rooms)])