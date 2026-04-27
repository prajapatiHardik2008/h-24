from  flask import Flask,render_template,render_template_string,request,jsonify
import pybase64
import time
import smtplib
from email.message import EmailMessage
import threading
from dotenv import load_dotenv
import os
import socket
from flask_sqlalchemy import SQLAlchemy

#----------------------------------------------------------------------
# tools 
#----------------------------------------------------------------------
# Port Scanner import socket
 #set bydefualt 1
def port_scanner(TargetIp, port):
    # Socket create kiya
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3) # Fast scanning ke liye thoda kam timeout
    
    try:
        # connect_ex 0 return karta hai agar connection success ho
        result = s.connect_ex((TargetIp, port))
        
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown Service"
            
            s.close() 
            return f"Port {port} ({service}) is Open"
        
        s.close()
        return None 
        
    except Exception as e:
        s.close()
        return f"Error scanning port {port}"

def encodebase64(text):
    text = pybase64.encodebytes(text)
    text = text.decode()
    return text
#-----------------------------------------------------------------------
def decodebase64(text):
    DecodeText = pybase64.b64decode(text)
    return DecodeText.decode()
def emailSender():
    load_dotenv()
    emailAdd = os.getenv('EMAIL_USER')
    Apppass = os.getenv('EMAIL_PASS')
    while True:
        # 1 din = 86400 seconds (par test karne ke liye 60-300 rakho)
        time.sleep(1200) 
        if not os.path.exists('userRequest.txt'):
            continue
        try:
            # File se data read karo
            with open('userRequest.txt', 'r') as file:
                log_data = file.read()

            if log_data.strip():
                msg = EmailMessage()
                msg['Subject'] = "H-24 Portal: Daily Activity Report"
                msg['From'] = emailAdd
                msg['To'] = "hardikprajapati242008@gmail.com"
                msg.set_content(f"Here is the feedback/activity logged in the last 24 hours:\n\n{log_data}")

                with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                    smtp.starttls()
                    smtp.login(emailAdd, Apppass)
                    smtp.send_message(msg)
                    print("Daily Report Sent!")

                # File clear kar do taaki agle din naya data aaye
                open("userRequest.txt", "w").close()
                
        except Exception as e:
            print(f"Error in EmailSender: {e}")

#------------------------------------------------------
# all Pages 
app = Flask(__name__)
#---------------------------------------------------------------------
#connecting with data base 
basedir = os.path.abspath(os.path.dirname(__file__)) # geting current folder path
db_url = os.getenv('DATABASE_URL')
if db_url:
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,"database.db")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    print("Database Tables Created! ✅")
#-------------------------------------------------------
#class for adding and Handling  the Feedback in data base 
class Feedback(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(50) , nullable=False)
    phone = db.Column(db.String(12) , nullable=False)
    stars = db.Column(db.Integer , nullable=False)
    query = db.Column(db.Text , nullable=False)
    ip_address = db.Column(db.String(50) , nullable=False)
#-------------------------------------------------------
#index  Page 
@app.route('/')
def index():
    total_feedbacks = db.session.query(Feedback).count() # count the total row in db 
    if total_feedbacks:
        all_stars = db.session.query(db.func.sum(Feedback.stars)).scalar()
        rating_val = all_stars / total_feedbacks
    else:
        rating_val = 0
    
    return render_template('index.html',Rating = round(rating_val,1))
#------------------------------------------------------
#Base 64 page 
@app.route('/base64_tool')
def base64():
    return render_template('base64.html')
#-------------------------------------------------------
#contacat Us page
@app.route('/contactus')
def contactus():
    return render_template("ContactUs.html")

#-------------------------------------------------------
#About Us 
@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")
#------------------------------------------------------
#Base 16 page 
@app.route('/base16')
def base16():
    return render_template('base16.html')
#-------------------------------------------------------
# Digtal forensics page 
@app.route('/Forensics_tool')
def dforensics():
    return render_template('digitalfor.html')
#-------------------------------------------------------
# certificates page
@app.route('/certificates')
def certificates():
    return render_template("certif.html")
#--------------------------------------------------------
# Web Terminal 
@app.route('/webTerminal')
def terminal():
    return render_template("webterminal.html")
#------------------------------------------------------
# Just a normal cyber security Challange 
@app.route('/challange')
def challange():
    return render_template('cybersecurity.html')
#-------------------------------------------------------
# image maker  
@app.route('/image')
def image():
    return render_template("createimage.html")
#------------------------------------------------------
# Help
@app.route('/help')
def help():
    return render_template("helpcenter.html")
#------------------------------------------------------
#Rot 
@app.route("/rot")
def rot():
    return render_template("rot.html")
#-----------------------------------------------------
#IP Look Up 
@app.route("/iplookup")
def iplookup():
    return render_template("IPlookup.html")
#-------------------------------------------------------
# Port Scanner 
@app.route("/portscan")
def portscanner():
    return render_template("portscan.html")
import socket
from flask import Flask, request, jsonify

@app.route('/scan_port', methods=['POST'])
def scan_port():
    data = request.json
    target = data.get('ip')
    port = data.get('port')
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.4) # Faster response
    
    result = s.connect_ex((target, port))
    
    if result == 0:
        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"
        s.close()
        return jsonify({"status": "open", "port": port, "service": service})
    
    s.close()
    return jsonify({"status": "closed", "port": port})
#-------------------------------------------------------
# All Api's 
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
    
@app.route('/base64D',methods=['POST'])
def base64Deco():
    data = request.get_json()
    encText = data.get('encText')
    try:
        DecodeText = decodebase64(encText)
        return jsonify({"DecodedText":DecodeText})
    except:
        return jsonify({"DecodedText": "Something went wrong !"})
@app.route('/feedBack', methods=["POST"])
def feedBack():
    data = request.get_json()
    user_ip = request.remote_addr
    already_voted = db.session.query(Feedback).filter_by(ip_address=user_ip).first()

    if already_voted:
        return jsonify({"Ans": "Fail", "msg": "You have already voted!"})
    try:
        new_entry =Feedback(
            username = data.get('username'),
            phone = data.get('userphone'),
            query = data.get('userquery'),
            stars = int(data.get('star')),
            ip_address = user_ip
        ) 
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"Ans": "Success"}) # Success message bhejo
    except Exception as e:
        db.session.rollback()
        return jsonify({'Ans': 'Fail',"msg":"Server Error"})
if __name__ == '__main__':
    #thread = threading.Thread(target=emailSender,daemon=True)
    #thread.start()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
