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
