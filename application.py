from flask import Flask, request
from flask_restful import Resource, Api
import json
from surpriseRecommender import Recommender
from surpriseRecommender import RecType
from pymongo import MongoClient
client = MongoClient('mongodb://pcr_group:pcr123@ds137862.mlab.com:37862/pcr')
from recs import courses


application = Flask(__name__)
api = Api(application)

class student_recs(Resource):
    def get(self):
        args = request.args
        course1 = args['course1']
        course2 = args['course2']
        course3 = args['course3']
        course4 = args['course4']
        course5 = args['course5']
        rating1 = args['rating1']
        rating2 = args['rating2']
        rating3 = args['rating3']
        rating4 = args['rating4']
        rating5 = args['rating5']

        ratingMap = { str(course1): [str(rating1), "5", "5", "5", "5", "5", "5"],
                      str(course2): [str(rating2), "5", "5", "5", "5", "5", "5"],
                      str(course3): [str(rating3), "5", "5", "5", "5", "5", "5"],
                      str(course4): [str(rating4), "5", "5", "5", "5", "5", "5"],
                      str(course5): [str(rating5), "5", "5", "5", "5", "5", "5"]
                      }
        numRecs = 10
        r = Recommender(numRecs, RecType.COURSE_QUALITY)
        r.add_student_ratings(ratingMap)
        r.run_rec_alg()
        recs = client.pcr.recommendations
        sr = recs.find()
        z = {}
        for x in sr:
            y = list()
            if float(x['sid']) == float(r.newStudID):
                cu = []
                for i in range(numRecs):
                    key = 'course' + str(i + 1)
                    cu.append(x[key])
                for c in cu:
                    for course in courses:
                        if float(c) == float(course.get_id()):
                            obj = {}
                            obj['code'] = str(course.get_aliases())
                            obj['name'] = str(course.get_name())
                            obj['courseQuality'] = str(course.get_course_quality())
                            obj['difficulty'] = str(course.get_difficulty())
                            obj['instructorQuality'] = str(course.get_instructor_quality())
                            obj['description'] = str(course.get_desc())
                            y.append(json.dumps(obj))
                z[x['sid']] = y
        return json.dumps(z)


api.add_resource(student_recs, '/getrecs') # Route_1

if __name__ == '__main__':
    # application.run()
    application.run(port=5002)
