from flask import Blueprint, request, jsonify
from web.models import Video
from web import db
import datetime

video = Blueprint('video', __name__)


@video.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    start = datetime.datetime.strptime(data["start_time"], '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(data["end_time"], '%Y-%m-%d %H:%M:%S')
    new_task = Video(camera_id=data["camera_id"], start_time=start, end_time=end, filepath=data["filepath"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Video Data uploaded successfully"})


@video.route('/search', methods=['GET'])
def search():
    data = request.get_json()
    a = data['start_time']
    b = data['end_time']
    try:
        c = data['camera_id']
    except:
        c = None

    if c is None:
        qry1 = Video.query.filter(Video.start_time >= a, Video.end_time <= b).order_by(Video.camera_id,
                                                                                       Video.start_time)
        qry2 = Video.query.filter(Video.start_time >= a, Video.start_time <= b).order_by(Video.start_time)
        qry3 = Video.query.filter(Video.end_time >= a, Video.end_time <= b).order_by(Video.camera_id,
                                                                                     Video.start_time)
    else:
        qry1 = Video.query.filter(Video.camera_id == c, Video.start_time <= a, Video.end_time >= b).order_by(
            Video.camera_id, Video.start_time)
        qry2 = Video.query.filter(Video.camera_id == c, Video.start_time >= a, Video.start_time <= b).order_by(
            Video.start_time)
        qry3 = Video.query.filter(Video.camera_id == c, Video.end_time >= a, Video.end_time <= b).order_by(
            Video.start_time)
    qry1 = set(qry1)
    qry2 = set(qry2)
    qry3 = set(qry3)
    qry4 = qry1.union(qry2)
    qry5 = qry4.union(qry3)
    output = []
    for link in qry5:
        data = {}
        data['camera_id'] = link.camera_id
        data['start_time'] = link.start_time
        data['end_time'] = link.end_time
        data['filepath'] = link.filepath
        output.append(data)
    return jsonify({'files': output})
