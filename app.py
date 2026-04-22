from  flask import Flask,render_template,render_template_string,request,jsonify
import pybase64
#----------------------------------------------------------------------
# tools 
def encodebase64(text):
    text = pybase64.encodebytes(text)
    text = text.decode()
    return text

app = Flask(__name__)

#-------------------------------------------------------
#index  Page 
@app.route('/')
def index():
    return render_template('index.html')
#------------------------------------------------------
#Base 64 page 
@app.route('/base64_tool')
def base64():
    return render_template('base64.html')
#----------------------------------------------------
# base 64 Encoding and decoding API 
@app.route('/base64E',methods=['POST'])
def base64Enod():
    data = request.get_json()
    text = data.get('plainText')
    try:
        EText = encodebase64(text.encode())
        return jsonify({"EncodedText": EText})
    except:
        return jsonify({"EncodedText": "Something went wrong !"})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)