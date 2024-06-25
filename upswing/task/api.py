from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection details
client = MongoClient('localhost', 27017)
db = client.test
collection = db.mycollection

@app.route('/status_count', methods=['GET'])
def get_status_count():
    # Get start and end times from request arguments
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return jsonify({"error": "Please provide both start_time and end_time in ISO format"}), 400

    try:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
        
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format"}), 400

    # Use MongoDB aggregate pipeline to count statuses within the time range
    pipeline = [
        {"$match": {"message.timestamp": {"$gte": start_time, "$lt": end_time}}},
        {"$group": {"_id": "$message.status", "count": {"$sum": 1}}}
    ]

    result = list(collection.aggregate(pipeline))

    # Format the result to return as a JSON response
    status_count = {str(item['_id']): item['count'] for item in result}

    return jsonify(status_count)

if __name__ == "__main__":
    app.run(debug=True)
