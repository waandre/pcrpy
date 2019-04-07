from flask import Flask, request
from flask_restful import Resource, Api
import json
from surpriseRecommender import Recommender
from surpriseRecommender import RecType
from recs import courses


application = Flask(__name__)
api = Api(application)

## TODO: add ability to take in user input and send back recs
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

        r = Recommender(10, RecType.COURSE_QUALITY)
        r.add_student_ratings(ratingMap)
        r.run_rec_alg()
        check = [i.strip().split("\t") for i in open('./student_rec.csv').readlines()]
        x = {}
        for stu in check:
            y = list()
            for c in stu[1:]:
                for course in courses:
                    if c == course.get_id():
                        y.append(str(course.get_aliases()) + " " + course.get_name())
            x[stu[0]] = y
        return json.dumps(x)


api.add_resource(student_recs, '/getrecs') # Route_1

if __name__ == '__main__':
    application.run(debug=True)
