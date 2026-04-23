from  flask import Flask,render_template,render_template_string,request,jsonify
import pybase64
import time
import smtplib
from email.message import EmailMessage
import threading
from dotenv import load_dotenv
import os

#----------------------------------------------------------------------
# tools 
def encodebase64(text):
    text = pybase64.encodebytes(text)
    text = text.decode()
    return text

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
            print(f"Error in EmailSender: {e}")#------------------------------------------------------
# all Pages 
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
    username = data.get('username')
    userphone = data.get('userphone')
    userquery = data.get('userquery')
    star = data.get('star')

    try:
        # 'a' (append) use karo taaki purana data delete na ho
        with open('userRequest.txt', 'a') as file:
            file.write("\n" + "-"*30 + "\n")
            file.write(f"Username: {username}\n")
            file.write(f"Phone: {userphone}\n")
            file.write(f"Star: {star}\n")
            file.write(f"Request: {userquery}\n")
        
        return jsonify({"Ans": "Success"}) # Success message bhejo
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'Ans': 'Fail'})
if __name__ == '__main__':
    #thread = threading.Thread(target=emailSender,daemon=True)
    #thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
