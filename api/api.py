from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json, os, shutil, time, datetime
from werkzeug.utils import secure_filename

from concurrent.futures import ThreadPoolExecutor
#from oldModel.model import predict
from model.predict_data import predict
executor = ThreadPoolExecutor(1)

'''
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/zombie_company?charset=UTF8MB4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'upload')

class BatchRecord(db.Model):
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    CreatTime = db.Column(db.DateTime, nullable=False, default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    FilePath = db.Column(db.String(20), nullable=False)
    PredictState = db.Column(db.Integer, nullable=False, default=0) # 0:识别中  1:识别成功  2:错误

'''使用线程池回调函数，解决了预测完成后的数据库预测状态更新的问题
def updatePredictState():
    #print('开始执行定时任务')
    records = BatchRecord.query.order_by(BatchRecord.ID).all()
    for record in records:
        filepath = record.FilePath
        RESULT_PATH = os.path.join(os.path.join(UPLOAD_PATH, filepath), 'predictResult.csv')
        if os.path.exists(RESULT_PATH):
            if record.PredictState == 0 or record.PredictState == 2:
                record.PredictState = 1
                db.session.commit()
        else:
            if record.PredictState == 1:
                record.PredictState = 2
                db.session.commit()
'''

CurrentFilePath = ''
def predict_callback(res):
    record = BatchRecord.query.filter_by(FilePath=CurrentFilePath).first()
    if res.exception() is not None:
        print('预测失败')
        record.PredictState = 2
        db.session.commit()
    else:
        print('预测成功')
        record.PredictState = 1
        db.session.commit()

@app.route('/Upload', methods=['POST'])
def Upload():
    if not os.path.exists(UPLOAD_PATH):
        os.mkdir(UPLOAD_PATH)
    file = request.files.get('file')
    filepath = request.form.get('filepath')
    type = request.form.get('type')
    FILE_PATH = os.path.join(UPLOAD_PATH, filepath)
    if not os.path.exists(FILE_PATH):
        os.mkdir(FILE_PATH)
    #filename = secure_filename(file.filename)
    file.save(os.path.join(FILE_PATH,type+'.csv'))
    # 判断4个文件是否上传完毕
    if len(os.listdir(FILE_PATH))== 4:
        #print('4个文件上传完毕！')
        record = BatchRecord()
        record.CreatTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        record.FilePath = filepath
        db.session.add(record)
        db.session.commit()

        MODEL_PATH = os.path.join(os.path.join(os.path.dirname(__file__), "model"), "verify_catboost.m")
        # 异步对文件进行预测
        global CurrentFilePath
        CurrentFilePath = filepath
        executor.submit(predict, FILE_PATH, MODEL_PATH).add_done_callback(predict_callback)
        # 添加定时任务, 检测提交状态
        '''
        try:
            scheduler.add_job(updatePredictState, 'interval', seconds=1, id='predictstate')
        except:
            pass
        '''
    return type + 'accept!'

@app.route('/getBatchRecord', methods=['GET'])
def getBatchRecord():
    records = BatchRecord.query.order_by(BatchRecord.ID).all()
    records_list = []
    for a in records:
        record = {}
        record['ID'] = a.ID
        record['CreatTime'] = a.CreatTime.strftime('%Y-%m-%d %H:%M:%S')
        record['FilePath'] = a.FilePath
        record['PredictState'] = a.PredictState
        records_list.append(record)
    return json.dumps(records_list)

@app.route('/getPredictState/<filepath>', methods=["GET"])
def getPredictState(filepath):
    record =  BatchRecord.query.filter_by(FilePath=filepath).first()
    if record.PredictState == 0:
        return 'False'
    else:
        try:
            scheduler.remove_job('predictstate')
        except:
            pass
        return 'True'

@app.route('/Download/<filepath>', methods=['GET'])
def Download(filepath):
    RESULT_PATH = os.path.join(UPLOAD_PATH,filepath)
    #print(RESULT_PATH)
    return send_from_directory(RESULT_PATH, 'predictResult.csv', as_attachment=True)

@app.route('/Delete', methods=['POST'])
def Delete():
    filepath = request.get_json()['FilePath']
    record = BatchRecord.query.filter_by(FilePath=filepath).first()
    db.session.delete(record)
    db.session.commit()
    shutil.rmtree(os.path.join(UPLOAD_PATH, filepath), ignore_errors=True)
    return 'delete' + filepath

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)