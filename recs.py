import numpy as np
from scipy.optimize import nnls
import csv

"""CLASSES"""

"""
Course class. Takes in a course name, its id, aliases and ratings. Can create default ratings for courses
by creating normal distributions based on Penn Labs API data (course rating info). Ratings are all assumed to be
done on a 1-5 scale
"""


class Course(object):
    def __init__(self, name, id, aliases, ratings):
        self.name = name
        self.id = id
        self.aliases = aliases
        self.courseQuality = float(ratings[0])
        self.courseQualityDist = []
        self.instructorQuality = float(ratings[1])
        self.instructorQualityDist = []
        self.difficulty = float(ratings[2])
        self.difficultyDist = []
        self.amountLearned = float(ratings[3])
        self.amountLearnedDist = []
        self.workRequired = float(ratings[4])
        self.workRequiredDist = []
        self.recommendToMajor = float(ratings[5])
        self.recommendToMajorDist = []
        self.recommendToNonMajor = float(ratings[6])
        self.recommendToNonMajorDist =[]
        self.numReviewers = float(ratings[7])
        self.masterDist = []

    def __str__(self):
        return self.name + ": " + str(self.id)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_aliases(self):
        return self.aliases

    def get_course_quality(self):
        return self.courseQuality

    def get_instructor_quality(self):
        return self.instructorQuality

    def get_difficulty(self):
        return self.difficulty

    def get_amount_learned(self):
        return self.amountLearned

    def get_work_required(self):
        return self.workRequired

    def get_recommend_major(self):
        return self.recommendToMajor

    def get_recommend_non_major(self):
        return self.recommendToNonMajor

    def get_number_reviewers(self):
        return self.numReviewers

    # helper method for distribution builder based on rating data
    def dist_helper(self, val):
        a = np.array([[1, 2, 3, 4, 5], [1, 1, 1, 1, 1]])
        if val > 0 and self.numReviewers > 0:
            b = np.array([val * self.get_number_reviewers(), self.get_number_reviewers()])
            pref = np.linalg.lstsq(a, b)
            l = []
            clear = True
            for j in pref[0]:
                if j < 0:
                    clear = False
                    break
            if clear:
                for k in pref[0]:
                    l.append(round(k))
            else:
                sec = nnls(a, b)
                for k in sec[0]:
                    l.append(round(k))
            return l
        else:
            return [0, 0, 0, 0, 0]

    # method creates course quality distribution
    def course_qual_dist(self):
        self.courseQualityDist = self.dist_helper(self.courseQuality)

    # method returns course quality distribution
    def get_course_qual_dist(self):
        return self.courseQualityDist

    # method creates instructor quality distribution
    def instructor_qual_dist(self):
        self.instructorQualityDist = self.dist_helper(self.instructorQuality)

    # method returns instructor quality distribution
    def get_instructor_qual_dist(self):
        return self.instructorQualityDist

    # method creates difficulty distribution
    def difficulty_dist(self):
        self.difficultyDist = self.dist_helper(self.difficulty)

    # method returns difficulty distribution
    def get_difficulty_dist(self):
        return self.difficultyDist

    # method creates amount learned distribution
    def amount_learned_dist(self):
        self.amountLearnedDist = self.dist_helper(self.amountLearned)

    # method returns amount learned distribution
    def get_amount_learned_dist(self):
        return self.amountLearnedDist

    # method creates work required distribution
    def work_required_dist(self):
        self.workRequiredDist = self.dist_helper(self.workRequired)

    # method returns work required distribution
    def get_work_required_dist(self):
        return self.workRequiredDist

    # method creates recommend to major distribution
    def rec_maj_dist(self):
        self.recommendToMajorDist = self.dist_helper(self.recommendToMajor)

    # method returns recommend to major distribution
    def get_rec_maj_dist(self):
        return self.recommendToMajorDist

    # method creates recommend to non major distribution
    def rec_nonmaj_dist(self):
        self.recommendToNonMajorDist = self.dist_helper(self.recommendToNonMajor)

    # method returns recommend to non major distribution
    def get_rec_nonmaj_dist(self):
        return self.recommendToNonMajorDist

    # aggregates all normal distributions
    def update_master_dist(self):
        self.masterDist = [self.courseQualityDist, self.instructorQualityDist, self.difficultyDist, self.amountLearnedDist, self.workRequiredDist, self.recommendToMajorDist, self.recommendToNonMajorDist]

    # returns master distributions
    def get_master_dist(self):
        return self.masterDist


"""
Student class. Takes in an id, and a map of student-course ratings. Students each maintain their ratings for 
each course they have input
"""


class Student(object):
    def __init__(self, idnum, ratings):
        self.id = idnum
        self.ratings = ratings
        self.courseRating = []
        self.instructorRating = []
        self.diffRating = []
        self.workRating = []
        self.learnedRating = []
        self.majRating = []
        self.nonMajRating = []

    def get_course_rating(self):
        return self.courseRating

    def get_instructor_rating(self):
        return self.instructorRating

    def get_diff_rating(self):
        return self.diffRating

    def get_work_required_rating(self):
        return self.workRating

    def get_amount_learned_rating(self):
        return self.learnedRating

    def get_maj_rating(self):
        return self.majRating

    def get_non_maj_rating(self):
        return self.nonMajRating

    # method to match google form ratings to courses by ID, and create various rating breakdowns
    def match_ratings_to_courses(self, courses):
        for rating in self.ratings.keys():
            for item in courses:
                if rating in courses[item]:
                    self.courseRating.append([self.id, item, self.ratings[rating][0]])
                    self.instructorRating.append([self.id, item, self.ratings[rating][1]])
                    self.diffRating.append([self.id, item, self.ratings[rating][2]])
                    self.workRating.append([self.id, item, self.ratings[rating][3]])
                    self.learnedRating.append([self.id, item, self.ratings[rating][4]])
                    self.majRating.append([self.id, item, self.ratings[rating][5]])
                    self.nonMajRating.append([self.id, item, self.ratings[rating][6]])

    def __str__(self):
        return str(self.id) + " " + str(self.ratings) + " " + str(self.courseRating)


"""COURSE PARSING"""

course_list = [i.strip().split("\t\t") for i in open('./neo4jCourses.csv').readlines()]
course_list = course_list[1:]

# list of all courses in graph
courses = []

# create maps of course names to ids and vice versa
for i in course_list:
    for j in i:
        arr = j.split(',')
        aset = arr[5]
        aset = aset[1:len(aset) - 1]
        aliases = aset.split(' -- ')
        ratings = arr[6:14]
        courses.append(Course(arr[0],arr[2], aliases, ratings))

# map of course ids to their aliases
idAliasMap = {}

for c in courses:
    idAliasMap[c.get_id()] = c.get_aliases()

"""SURVEY PARSING"""

responses = [i.strip().split("\t\t") for i in open('./responses.csv').readlines()]
responses = responses[1:]

# list of all students to build SVD matrix
students = []


for i in range(len(responses)):
    info = responses[i][0].split(",")
    allCourses = {}
    course1 = info[2].replace(" ", "-").upper()
    course2 = info[10].replace(" ", "-").upper()
    course3 = info[18].replace(" ", "-").upper()
    course4 = info[26].replace(" ", "-").upper()
    course5 = info[34].replace(" ", "-").upper()
    if '-' not in course1:
        course1 = course1[0:len(course1)-3] + "-" + course1[len(course1) - 3:]
    if '-' not in course2:
        course2 = course2[0:len(course2)-3] + "-" + course2[len(course2) - 3:]
    if '-' not in course3:
        course3 = course3[0:len(course3)-3] + "-" + course3[len(course3) - 3:]
    if '-' not in course4:
        course4 = course4[0:len(course4)-3] + "-" + course4[len(course4) - 3:]
    if '-' not in course5:
        course5 = course5[0:len(course5) - 3] + "-" + course5[len(course5) - 3:]
    c1r = info[3:10]
    c2r = info[11:18]
    c3r = info[19:26]
    c4r = info[27:34]
    c5r = info[35:42]
    allCourses[course1] = c1r
    allCourses[course2] = c2r
    allCourses[course3] = c3r
    allCourses[course4] = c4r
    allCourses[course5] = c5r
    s = Student(i, allCourses)
    s.match_ratings_to_courses(idAliasMap)
    students.append(s)

# with open('student_data.pkl', 'wb') as output:
#     for s in students:
#         pickle.dump(s, output, pickle.HIGHEST_PROTOCOL)
#
# students = []
# def pickleLoader(pklFile):
#     try:
#         while True:
#             yield pickle.load(pklFile)
#     except EOFError:
#         pass
#
# with open('student_data.pkl', 'rb') as input:
#     for event in pickleLoader(input):
#         students.append(event)


""" CSV file writing for SVD recs"""


# method to write rating files based on student input (google survey). Takes in student list (students)
def write_rec_files_from_users(s):
    with open('courseQualRating.csv', 'w', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for student in s:
            # if student.id == len(students):
                for li in student.get_course_rating():
                    wrtr.writerow(li)

    with open('profQualRating.csv', 'w', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for student in s:
            # if student.id == len(students):
                for li in student.get_instructor_rating():
                    wrtr.writerow(li)

    with open('diffRating.csv', 'w', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for student in s:
            # if student.id == len(students):
                for li in student.get_diff_rating():
                    wrtr.writerow(li)

    with open('workReqRating.csv', 'w', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for student in s:
            # if student.id == len(students):
                for li in student.get_work_required_rating():
                    wrtr.writerow(li)

    with open('amtLearnedRating.csv', 'w', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for student in s:
            # if student.id == len(students):
                for li in student.get_amount_learned_rating():
                    wrtr.writerow(li)

    with open('recToMaj.csv', 'w', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for student in s:
            # if student.id == len(students):
                for li in student.get_maj_rating():
                    wrtr.writerow(li)

    with open('recToNonMaj.csv', 'w', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for student in s:
            # if student.id == len(students):
                for li in student.get_non_maj_rating():
                    wrtr.writerow(li)


# method to write rating files based on added student. Takes in student
def write_rec_files_from_student(s):
    with open('courseQualRating.csv', 'a', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for li in s.get_course_rating():
            wrtr.writerow(li)

    with open('profQualRating.csv', 'a', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for li in s.get_instructor_rating():
            wrtr.writerow(li)

    with open('diffRating.csv', 'a', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for li in s.get_diff_rating():
            wrtr.writerow(li)

    with open('workReqRating.csv', 'a', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for li in s.get_work_required_rating():
            wrtr.writerow(li)

    with open('amtLearnedRating.csv', 'a', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for li in s.get_amount_learned_rating():
            wrtr.writerow(li)

    with open('recToMaj.csv', 'a', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for li in s.get_maj_rating():
            wrtr.writerow(li)

    with open('recToNonMaj.csv', 'a', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for li in s.get_non_maj_rating():
            wrtr.writerow(li)


# method to write rating files based on normal distributions. Takes in master course list (courses)
def write_rec_files_from_dist(c):
    for course in c:
        course.course_qual_dist()
        course.instructor_qual_dist()
        course.difficulty_dist()
        course.work_required_dist()
        course.amount_learned_dist()
        course.rec_maj_dist()
        course.rec_nonmaj_dist()
        course.update_master_dist()

    filenames = ['courseQualRating', 'profQualRating', 'diffRating', 'amtLearnedRating', 'workReqRating',
                 'recToMaj', 'recToNonMaj']
    stud = 0

    # write ratings by student and course
    for ind in range(7):
        with open(filenames[ind] + '.csv', 'w', newline='') as csvfile:
            wrtr = csv.writer(csvfile, delimiter='\t',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for course in c:
                li = course.masterDist[ind]
                for num in li:
                    for k in range(int(num)):
                        wrtr.writerow([stud, course.get_id(), li.index(num) + 1])
                        stud += 1


write_rec_files_from_users(students)