from flask import Flask,render_template,request,jsonify,send_file
import base64
from io import BytesIO
from datetime import datetime

app=Flask(__name__)
photos=[]

@app.route('/')
def index():return render_template('photobooth.html',photos=photos,gallery_mode=False)

@app.route('/gallery')
def gallery():return render_template('photobooth.html',photos=photos,gallery_mode=True)

@app.route('/save-photo',methods=['POST'])
def save():
    try:
        p=request.json.get('photo','')
        if not p:return jsonify(success=False,message='No photo data')
        d={'id':len(photos),'data':p.split(',')[1] if ',' in p else p,'timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        photos.append(d);return jsonify(success=True,message='Saved!',photo_id=d['id'])
    except Exception as e:return jsonify(success=False,message=str(e))

@app.route('/download/<int:i>')
def download(i):
    return send_file(BytesIO(base64.b64decode(photos[i]['data'])),mimetype='image/png',as_attachment=True,download_name=f'photobooth_{i}.png') if i<len(photos) else ("Not found",404)

@app.route('/delete/<int:i>',methods=['POST'])
def delete(i):
    try:
        if i<len(photos):
            photos.pop(i)
            for j,p in enumerate(photos):p['id']=j
            return jsonify(success=True)
        return jsonify(success=False,message='Not found')
    except Exception as e:return jsonify(success=False,message=str(e))

if __name__=='__main__':app.run(debug=True,host='0.0.0.0',port=5000)