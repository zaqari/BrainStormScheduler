INPUT DOCUMENTS FORMAT

The following are examples of the columns required for the three data sheets required to run this program. The initial project required me to take in three documents to mine data from—
	(a) a csv that contained self-reported proficiencies in courses taught by 	BrainStorm Edu LLC,

	(b) a csv containing what courses were on the horizon for the summer, with names of Instructors and assistants per course, and

	(c) a sheet containing what proficiencies were required to teach the upcoming courses.

Two outputs were required: (a) a list of the courses that staff needed to be trained on, specific to what they would need to teach over the summer, and (b) a training schedule that would most efficiently use the number of rooms available to BrainStorm Edu LLC for training. The name of each sheet as it is coded for in the app are in square brackets adjacent to verbose descriptions of what the sheet contained below.

(For self-reported proficiencies sheet) [skills.csv]

	Topics	StaffName1	StaffName2	. . .  
	. . .	. . .		. . .


(For courses being taught by instructor sheet) [staff-1w.csv & staff-3w.csv]

	course	Instructor	Assistant1	Assistant2
	. . .	. . .		. . .		. . .


(For required skills to teach summer courses) [class_by_topic_1w.csv & class_by_topic_3w.csv]

	course	topic1	topic2	topic3	topic4	. . .
	. . .	. . .	. . .	. . .	. . .


TO RUN:

(1) in python console:
    import query.training_schedule.training_matrices as tm
    doc1 = tm.query()
    doc2 = tm.query(courses='input-data/staff-3w.csv', required_skills='input-data/class_by_topic_3w.csv')
    doc1_csv = doc1.matrices_to_csv('1w-needs')
    doc2_csv = doc1.matrices_to_csv('3w-needs')

(2) querying data structure:
    import query.training_schedule.training_sessions as ts
    w1 = ts.sess('1w-needs.csv')
    w2 = ts.sess('3w-needs.csv')

    #to find trainee training needs
    w1.find_training_needs('Sam Pasin')

    #to find who is in a class:
    w1.find_trainees('Python')

    #combine into one doc:

(3) Ad-hoc analytics
    #Creates dictionary of who needs to be trained on what . . .
    train_me = {}
    for col in list(doc)[1:]:
        s = doc['staff'].loc[doc[col].isin([str(1)])].values.tolist()
        if col in train_me.keys():
            train_me[col] += s
        else:
            train_me[col] = s
        train_me[col] = list(set(train_me[col]))

    no_need = []
    for k, v in train_me.items():

        if len(v) <= 0:
            no_need.append(k)

    print(len(no_need))

    len_trainees = []
    course_name = []

    for k, v in train_me.items():
        len_trainees.append(len(v))
        course_name.append(k)

    from collections import Counter
    data = counter(len_trainees)
    data.most_common()
