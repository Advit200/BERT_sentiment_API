from flask_restful import Resource,Api
from flask import Flask,jsonify
from flask_cors import CORS
from Make_Predictions import BERTModel
import redis
import config

r = redis.Redis(host="redis_server",port=config.REDIS_PORT,db=0)

app = Flask(__name__)
CORS(app)
api = Api(app)

class Default(Resource):

    def get(self):
        return jsonify({"API Info":"This is the main page of the Sentiment Analysis API.","Contact":"aditya.gaurav@kochgs.com"})


class Sentiment(Resource):

    def get(self,text):

        if r.exists(text):
            print("Ran from cache...")
            return jsonify(r.get(text).decode())

        else:
            print('Ran from Main file...')
            model = BERTModel(text)
            sentiment = model.get_sentiment

            r.set(text,str(sentiment))
            # r.expire(text,5)  # If you want to delete the cache after mentioned seconds.

            return jsonify(str(sentiment))



api.add_resource(Default,"/")    
api.add_resource(Sentiment,'/sentiment/<string:text>')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=config.APP_PORT)