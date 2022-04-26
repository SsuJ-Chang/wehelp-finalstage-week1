from flask import *
from mysql.connector import pooling
import boto3
from decouple import config

app=Flask(__name__, static_folder='public', static_url_path='/')

message_pool = pooling.MySQLConnectionPool(
    pool_name="message_pool",
    pool_size=10,
    # pool_reset_session=True,
    host=config('host'),
    user=config('user'),
    password=config('password'),
    database=config('database')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/message', methods=['POST'])
def save_message_data():
    message = request.form['message']
    print('留言', message)
    if(len(request.files) != 0):
        image = request.files['file'] # 接收檔案
        print('圖檔', image)
        print('圖檔名稱', image.filename)

    try:
        s3 = boto3.client('s3')
        s3.upload_fileobj(image, "rj728fun", image.filename)
    except:
        return {"error": True, "message": "伺服器內部錯誤"}, 500

    try:
        cnx = message_pool.get_connection()
        cursor = cnx.cursor(buffered = True, dictionary = True)
        cursor.execute("INSERT INTO message (message, image) VALUES (%s, %s)", (message, "https://dw8zcfe69riyr.cloudfront.net/"+image.filename))
    except:
        cnx.rollback()
        return {"error": True, "message": "伺服器內部錯誤"}, 500
    finally:
        cursor.close()
        cnx.commit()
        cnx.close()

    return {'ok': True}, 200

@app.route('/api/message', methods=['GET'])
def get_message_data():
    try:
        cnx = message_pool.get_connection()
        cursor = cnx.cursor(buffered = True, dictionary = True)
        cursor.execute("SELECT message, image FROM message")
        result = cursor.fetchall()
        print(result)
    except:
        return {"error": True, "message": "伺服器內部錯誤"}, 500
    finally:
        cursor.close()
        cnx.close()

    return {'data': result}, 200

app.run(host='0.0.0.0', port=3333, debug=False)