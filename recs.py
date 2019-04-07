import numpy as np
import csv
from scipy.optimize import nnls
from pymongo import MongoClient
client = MongoClient('mongodb://pcr_group:pcr123@ds137862.mlab.com:37862/pcr')


"""CLASSES"""

"""
Course class. Takes in a course name, its id, aliases and ratings. Can create default ratings for courses
by creating normal distributions based on Penn Labs API data (course rating info). Ratings are all assumed to be
done on a 1-5 scale
"""


class Course(object):
    def __init__(self, name, desc, id, aliases, ratings):
        self.name = name
        self.desc = desc
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


    def get_desc(self):
        return self.desc

    def get_aliases(self):
        return self.aliases

    def get_f_alias(self):
        return self.aliases.split(' -- ')[0].replace('[', '').replace(']', '')

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

# list of all courses in graph
courses = []

cs = client.pcr.courses
for x in cs.find():
    courses.append(Course(x['name'], x['description'],x['cid'], x['aliases'], [ x['courseQuality'], x['professorQuality'], x['difficulty'], x['amountLearned'], x['workRequired'], x['RecommendToMajor'], x['RecommendToNonMajor'], x['numberReviewers']]))

# map of course ids to their aliases
idAliasMap = {}

for c in courses:
    idAliasMap[c.get_id()] = c.get_aliases()

"""SURVEY PARSING"""

# list of all students to build SVD matrix
students = []

def fill_students():
    rs = client.pcr.responses
    client.pcr.students.drop()
    st = client.pcr.students
    for x in rs.find():
        course1 = x['Course 1 Name']
        course1R = [x['Course 1 Evaluation [Course Quality]'], x['Course 1 Evaluation [Instructor Quality]'], x['Course 1 Evaluation [Difficulty]'], x['Course 1 Evaluation [Work Required]'], x['Course 1 Evaluation [Amount Learned]'], x['Course 1 Evaluation [Would recommend to someone in major]'], x['Course 1 Evaluation [Would recommend to someone not in major]']]
        course2 = x['Course 2 Name']
        course2R = [x['Course 2 Evaluation [Course Quality]'], x['Course 2 Evaluation [Instructor Quality]'], x['Course 2 Evaluation [Difficulty]'], x['Course 2 Evaluation [Work Required]'], x['Course 2 Evaluation [Amount Learned]'], x['Course 2 Evaluation [Would recommend to someone in major]'], x['Course 2 Evaluation [Would recommend to someone not in major]']]
        course3 = x['Course 3 Name']
        course3R = [x['Course 3 Evaluation [Course Quality]'], x['Course 3 Evaluation [Instructor Quality]'], x['Course 3 Evaluation [Difficulty]'], x['Course 3 Evaluation [Work Required]'], x['Course 3 Evaluation [Amount Learned]'], x['Course 3 Evaluation [Would recommend to someone in major]'], x['Course 3 Evaluation [Would recommend to someone not in major]']]
        course4 = x['Course 4 Name']
        course4R = [x['Course 4 Evaluation [Course Quality]'], x['Course 4 Evaluation [Instructor Quality]'], x['Course 4 Evaluation [Difficulty]'], x['Course 4 Evaluation [Work Required]'], x['Course 4 Evaluation [Amount Learned]'], x['Course 4 Evaluation [Would recommend to someone in major]'], x['Course 4 Evaluation [Would recommend to someone not in major]']]
        course5 = x['Course 5 Name']
        course5R = [x['Course 5 Evaluation [Course Quality]'], x['Course 5 Evaluation [Instructor Quality]'], x['Course 5 Evaluation [Difficulty]'], x['Course 5 Evaluation [Work Required]'], x['Course 5 Evaluation [Amount Learned]'], x['Course 5 Evaluation [Would recommend to someone in major]'], x['Course 5 Evaluation [Would recommend to someone not in major]']]
        allCourses = {}
        allCourses[course1] = course1R
        allCourses[course2] = course2R
        allCourses[course3] = course3R
        allCourses[course4] = course4R
        allCourses[course5] = course5R
        s = Student(x['sid'], allCourses)
        s.match_ratings_to_courses(idAliasMap)
        students.append(s)
        s_data = {
            'sid': x['sid'],
        }
        st.insert_one(s_data)



""" CSV file writing for SVD recs"""


# method to write rating files based on student input (google survey). Takes in student list (students)
def write_rec_files_from_users(s):
    client.pcr.courseRating.drop()
    client.pcr.profRating.drop()
    client.pcr.diffRating.drop()
    client.pcr.workRating.drop()
    client.pcr.learnRating.drop()
    client.pcr.majRating.drop()
    client.pcr.nomRating.drop()
    course_rating = client.pcr.courseRating
    for student in s:
        for li in student.get_course_rating():
            s_data = {
                'user': li[0],
                'course': li[1],
                'rating': li[2]
            }
            course_rating.insert_one(s_data)

    ins_rating = client.pcr.profRating
    for student in s:
        for li in student.get_instructor_rating():
            s_data = {
                'user': li[0],
                'course': li[1],
                'rating': li[2]
            }
            ins_rating.insert_one(s_data)

    diff_rating = client.pcr.diffRating
    for student in s:
        for li in student.get_diff_rating():
            s_data = {
                'user': li[0],
                'course': li[1],
                'rating': li[2]
            }
            diff_rating.insert_one(s_data)

    work_rating = client.pcr.workRating
    for student in s:
        for li in student.get_work_required_rating():
            s_data = {
                'user': li[0],
                'course': li[1],
                'rating': li[2]
            }
            work_rating.insert_one(s_data)

    learn_rating = client.pcr.learnRating
    for student in s:
        for li in student.get_amount_learned_rating():
            s_data = {
                'user': li[0],
                'course': li[1],
                'rating': li[2]
            }
            learn_rating.insert_one(s_data)

    maj_rating = client.pcr.majRating
    for student in s:
        for li in student.get_maj_rating():
            s_data = {
                'user': li[0],
                'course': li[1],
                'rating': li[2]
            }
            maj_rating.insert_one(s_data)


    nom_rating = client.pcr.nomRating
    for student in s:
        for li in student.get_non_maj_rating():
            s_data = {
                'user': li[0],
                'course': li[1],
                'rating': li[2]
            }
            nom_rating.insert_one(s_data)


def write_rec_files_from_stud(s):
    course_rating = client.pcr.courseRating
    for li in s.get_course_rating():
        s_data = {
            'user': li[0],
            'course': li[1],
            'rating': li[2]
        }
        course_rating.insert_one(s_data)

    ins_rating = client.pcr.profRating
    for li in s.get_instructor_rating():
        s_data = {
            'user': li[0],
            'course': li[1],
            'rating': li[2]
        }
        ins_rating.insert_one(s_data)

    diff_rating = client.pcr.diffRating
    for li in s.get_diff_rating():
        s_data = {
            'user': li[0],
            'course': li[1],
            'rating': li[2]
        }
        diff_rating.insert_one(s_data)

    work_rating = client.pcr.workRating
    for li in s.get_work_required_rating():
        s_data = {
            'user': li[0],
            'course': li[1],
            'rating': li[2]
        }
        work_rating.insert_one(s_data)

    learn_rating = client.pcr.learnRating
    for li in s.get_amount_learned_rating():
        s_data = {
            'user': li[0],
            'course': li[1],
            'rating': li[2]
        }
        learn_rating.insert_one(s_data)

    maj_rating = client.pcr.majRating
    for li in s.get_maj_rating():
        s_data = {
            'user': li[0],
            'course': li[1],
            'rating': li[2]
        }
        maj_rating.insert_one(s_data)

    nom_rating = client.pcr.nomRating
    for li in s.get_non_maj_rating():
        s_data = {
            'user': li[0],
            'course': li[1],
            'rating': li[2]
        }
        nom_rating.insert_one(s_data)


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

