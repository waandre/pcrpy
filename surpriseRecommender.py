import csv
from surprise import Dataset
from surprise import Reader
from recs import *

from collections import defaultdict

from surprise import SVD, KNNBasic, KNNWithZScore, KNNWithMeans, KNNBaseline, NormalPredictor, BaselineOnly, SVDpp, NMF, SlopeOne, CoClustering
from enum import Enum


class RecType(Enum):
    COURSE_QUALITY = 1
    INSTRUCTOR_QUALITY = 2
    DIFFICULTY = 3
    WORK_REQUIRED = 4
    AMOUNT_LEARNED = 5
    REC_MAJOR = 6
    REC_NON_MAJOR = 7


class Recommender(object):
    def __init__(self, numRecs, type):
        self.numRecs = numRecs
        self.type = type
        self.file = self.get_file_type()
        arr = [i.strip().split("\t") for i in open('./courseQualRating.csv').readlines()]
        self.newStudID = int(arr[len(arr) - 1][0]) + 1

    def get_file_type(self):
        file = ""
        if self.type == RecType.COURSE_QUALITY:
            file = "courseQualRating.csv"
        elif self.type == RecType.INSTRUCTOR_QUALITY:
            file = "profQualRating.csv"
        elif self.type == RecType.DIFFICULTY:
            file = "diffRating.csv"
        elif self.type == RecType.AMOUNT_LEARNED:
            file = "amtLearnedRating.csv"
        elif self.type == RecType.WORK_REQUIRED:
            file = "workReqRating.csv"
        elif self.type == RecType.REC_MAJOR:
            file = "recToMaj.csv"
        else:
            file = "recToNonMaj.csv"
        return file

    def add_student_ratings(self, map):
        s = Student(self.newStudID, map)
        s.match_ratings_to_courses(idAliasMap)
        students.append(s)
        write_rec_files_from_student(s)

    def write_recs(self, top_n):
        # Print the recommended items for each user
        with open('student_rec.csv', 'w', newline='') as csvfile:
            wrtr = csv.writer(csvfile, delimiter='\t')
            for uid, user_ratings in top_n.items():
                if int(uid) == self.newStudID:
                    arr = [iid for (iid, _) in user_ratings]
                    arr.insert(0, uid)
                    wrtr.writerow(arr)

    def run_rec_alg(self):
        # path to dataset file
        file_path = self.file

        reader = Reader(line_format='user item rating', sep='\t')

        data = Dataset.load_from_file(file_path, reader=reader)

        # We can now use this dataset as we please, e.g. calling cross_validate
        # cross_validate(BaselineOnly(), data, verbose=True)
        trainset = data.build_full_trainset()
        algo = SVD()
        algo.fit(trainset)
        testset = trainset.build_anti_testset()
        predictions = algo.test(testset)
        top_n = self.get_top_n(predictions, n=self.numRecs)
        self.write_recs(top_n)

    def get_top_n(self, predictions, n=10):
        '''Return the top-N recommendation for each user from a set of predictions.

        Args:
            predictions(list of Prediction objects): The list of predictions, as
                returned by the test method of an algorithm.
            n(int): The number of recommendation to output for each user. Default
                is 10.

        Returns:
        A dict where keys are user (raw) ids and values are lists of tuples:
            [(raw item id, rating estimation), ...] of size n.
        '''

        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n


# r = Recommender(10, RecType.COURSE_QUALITY)

# map = {'CIS-160': ['1','2','3','5','4','2', '2'],'CIS-110': ['1','2','3','5','4','2', '2'],'CIS-120': ['1','2','3','5','4','2', '2'],'CIS-240': ['1','2','3','5','4','2', '2'],'CIS-350': ['1','2','3','5','4','2', '2'] }

# r.add_student_ratings(map)

# r.run_rec_alg()

# check = [i.strip().split("\t") for i in open('./rec_builder.csv').readlines()]

# for stu in check:
#     print("for student " + stu[0] + " we recommend:")
#     for c in stu[1:]:
#         for course in courses:
#             if c == course.get_id():
#                 print(str(course.get_aliases()) + " " + course.get_name())
#     print()

