import string
import secrets
from flask import Flask, jsonify, request
from datetime import datetime, timezone
import threading

posts = []
lock = threading.Lock()
moderator_keys = ["key"]

app = Flask(__name__)



@app.route('/post', methods=['POST'])
def create_post():
    post = {}

    alphabet = string.ascii_letters + string.digits
    while True:
        key = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in key) and any(c.isupper() for c in key) and sum(c.isdigit() for c in key) >= 3):
            break
    
    now_utc = datetime.utcnow()
    iso_date_time = now_utc.replace(microsecond=0).isoformat() + 'Z'

    try:
        msg = request.json['msg']
    except:
        return jsonify({"error": "bad request"}), 400
    
    if not isinstance(msg, str):
        return jsonify({"error": "bad request"}), 400

    reply_to_id = request.json.get('reply_to_id', None)
    if reply_to_id is not None:
        reply_to_id = int(reply_to_id)

    with lock:
        post["id"] = len(posts) + 1
        post["key"] = key
        post["timestamp"] = iso_date_time
        post["msg"] = msg
        post["reply_to_id"] = reply_to_id
        post["replies"] = []

        # Add the post to the replies of the parent post, if specified
        if reply_to_id is not None:
            for p in posts:
                if p["id"] == reply_to_id:
                    p["replies"].append(post["id"])
                    break

        posts.append(post)
        res = {
            "id": post["id"],
            "key": key,
            "timestamp": iso_date_time,
            "msg": msg,
            "reply_to_id": reply_to_id
        }

    return jsonify(res)

@app.route('/post/threads/<int:id>', methods=['GET'])
def get_posts(id):
    # get thread parameter
    thread_id = id

    # find the root post for the thread
    root_post = None
    for post in posts:
        if post['id'] == thread_id:
            root_post = post
            break

    if root_post is None:
        return jsonify({'error': 'Post not found'}), 404

    # get all posts in the thread
    thread = [root_post]

    def traverse_replies(post_id):
        replies = []
        for post in posts:
            if post.get('reply_to_id') == post_id:
                replies.append(post)
                replies += traverse_replies(post['id'])
        return replies

    thread += traverse_replies(root_post['id'])

    return jsonify(thread)



@app.route('/post/<int:id>', methods=['GET'])
def post_by_id(id):
    with lock:
        for p in posts:
            if p["id"] == id:
                res = {
                    "id": p["id"],
                    "key": p["key"],
                    "timestamp": p["timestamp"],
                    "msg": p["msg"],
                    "reply_to_id": p["reply_to_id"],
                    "replies": p["replies"]
                }
                return jsonify(res)
        return jsonify({"error": "not found"}), 404

    

@app.route('/post/<int:id>/delete', methods=['DELETE'])
def delete_by_id(id):
    key = request.json.get('key', None)

    with lock:
        for i in range(len(posts)):
            if posts[i]["id"] == id:
                if key is None or posts[i]["key"] == key or key in moderator_keys:
                    res = {
                        "id": posts[i]["id"],
                        "key": posts[i]["key"],
                        "timestamp": posts[i]["timestamp"],
                        "msg": posts[i]["msg"],
                        "reply_to_id": posts[i]["reply_to_id"],
                        "replies": posts[i]["replies"]
                    }
                    del posts[i]

                    # Remove the deleted post from the replies of the parent post, if specified
                    if res["reply_to_id"] is not None:
                        for p in posts:
                            if p["id"] == res["reply_to_id"]:
                                p["replies"].remove(res["id"])
                                break

                    return jsonify(res)
        return jsonify({"error": "not found"}), 404







@app.route('/post/search', methods=['GET'])

def search_posts():

    start_date_time=request.args.get('start',None)
    end_date_time=request.args.get('end', None)

    if start_date_time:
        try:
            start_date_time = datetime.strptime(start_date_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        except ValueError:
            return jsonify({"error": "bad request"}), 400

    if end_date_time:
        try:
            end_date_time = datetime.strptime(end_date_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        except ValueError:
            return jsonify({"error": "bad request"}), 400

    if start_date_time is None and end_date_time is None:
        return jsonify({"error": "bad request"}), 400

    results = []
    with lock:
        for post in posts:
            post_time = datetime.strptime(post['timestamp'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if (start_date_time is None or post_time >= start_date_time) and (end_date_time is None or post_time <= end_date_time):
                results.append({
                    "id": post["id"],
                    "key": post["key"],
                    "timestamp": post["timestamp"],
                    "msg": post["msg"],
                    "reply_to_id": post["reply_to_id"],
                    "replies": post["replies"]
                })

    return jsonify(results)


import re
from flask import jsonify, request

@app.route('/post/search/fulltext', methods=['GET'])
def fulltext_search_posts():
    query = request.args.get('q', None)
    if query is None:
        return jsonify({"error": "bad request"}), 400

    results = []
    with lock:
        for post in posts:
            if re.search(query, post['msg'], re.IGNORECASE):
                results.append({
                    "id": post["id"],
                    "key": post["key"],
                    "timestamp": post["timestamp"],
                    "msg": post["msg"],
                    "reply_to_id": post["reply_to_id"],
                    "replies": post["replies"]
                })

    return jsonify(results)



