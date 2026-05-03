import random
from flask import Flask, render_template, request, jsonify, session, redirect, url_for ,render_template_string,send_from_directory
import pybase64
import time
import smtplib
from email.message import EmailMessage
import threading
from dotenv import load_dotenv
import os
import socket
from flask_sqlalchemy import SQLAlchemy
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
import requests
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


#------------------------------------------------------------------
# AI 
def Aiprocess(command):
    prompt = f"Answer in 1-2 lines. If it's a coding task, provide only the code without explanation: {command}"
    
    response = requests.get(f"https://text.pollinations.ai/{prompt}?model=openai")
    return response.text
#----------------------------------------------------------------------
#-----------------------------------------------------

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
app.secret_key = os.getenv('SECRET_KEY')
#---------------------------------------------------------------------
#connecting with data base # ... app = Flask(__name__) ke niche ...

basedir = os.path.abspath(os.path.dirname(__file__))
db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///' + os.path.join(basedir, "database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- PEHLE CLASS LIKHO ---
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    query = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)

# --- PHIR TABLE CREATE KARO ---
with app.app_context():
    db.create_all()
    print("Database synced! ✅")
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
@app.route("/getaians",methods=["POST","GET"])
def getans():
    data = request.get_json()
    command = data.get("command")
    try:
        response = Aiprocess(command)
        return jsonify({"ans":response})
    except:
        return jsonify({"ans":"Server Error !"})
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
#./well-known/securit.txt page 
@app.route('/.well-known/security.txt')
def security_txt():
    try:
        return send_from_directory(os.path.join(app.root_path, 'static', '.well-known'), 
                               'security.txt', mimetype='text/plain')
    except Exception as e:
        return "Contact: mailto:hardikprajapati242008@gmail.com", 404
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
@app.route("/news")
def news():
    return render_template("Cyber-News.html")
#----------------------------------------------------
#News Api 
@app.route('/get-news-data')
def get_news_data():
    api_key = os.getenv("VITE_NEWS_API_KEY")
    url = f'''https://newsapi.org/v2/everything?q=cybersecurity&pageSize=20&apiKey={api_key}'''
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    if not articles:
            return jsonify({"news": ">> ERROR: No fresh intel found in the database."})

        # In 30 articles mein se koi bhi ek random select karo
    selected_article = random.choice(articles)
        
    title = selected_article.get('title', 'No Title')
    description = selected_article.get('description', 'No Content')
    clean_data = f"Title: {title} | Description: {description}"
    command = f"Cyber Mentor: Summarize this hacking news. 1.Simple Explain, 2.Signs to Identify, 3.Safety Steps. Bullet points only, 4 how to do it for eithcaly practice in my local host , this is data - {clean_data} "
    news = Aiprocess(command)
    if "Support Pollinations.AI" in news:
        news = news.split("Support Pollinations.AI")[0]
    news = news.strip()
    return jsonify({"news": news})
#---------------------------------------------------------
#OTP
def send_otp_email(otp):
    emailAdd = os.getenv('EMAIL_USER')
    Apppass = os.getenv('EMAIL_PASS')
    fakeotp = random.randint(100000, 999999) # 6 digit random
    
    msg = EmailMessage()
    msg['Subject'] = f"{fakeotp} is your H-24 Access Code"
    msg['From'] = emailAdd
    msg['To'] = "hardikprajapati242008@gmail.com"
    
    lines = [
        '18-year-old BCA student and Cybersecurity enthusiast at LJ University',
        'Python developer passionate about building secure portals and hacking tools.',
        'Active CTF player with a knack for network forensics and ethical hacking.',
        'Building the H-24 Portal: A blend of web development and advanced security.',
        'Self-taught coder focused on backend security and PostgreSQL databases',
        'Badminton player by day, Secure Code architect by night.'
    ]
    
    # Efficient content building
    content = ""
    for i in range(min(len(otp), len(lines))):
        content += f"\n{otp[i]}::--{lines[i]}"
        
    msg.set_content(f'''{content}\n\nYour one-time password for H-24 Admin Access is: {fakeotp}\n\nThis code will expire shortly.''')

    try:
        # 1. Timeout add kiya (10 seconds) taaki server hang na ho
        with smtplib.SMTP("smtp.gmail.com", 465, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(emailAdd, Apppass)
            smtp.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False
    return True
#---------------------------------------------------------
# --- Admin Login Page ---


# --- Login Route (Update) ---
@app.route('/h24_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        
        admin_user = os.getenv('ADMIN_USER') 
        admin_pass = os.getenv('ADMIN_PASS')

        if user == admin_user and check_password_hash(admin_pass, pwd):
            # 1. OTP Generate Karo
            otp = str(random.randint(100000, 999999))
            session['temp_otp'] = otp  # Temporarily save in session
            
            # 2. Email bhejo (Using your existing email logic)
            if send_otp_email(otp):
                 # Ek chota function bana lo iske liye
                return redirect(url_for('verify_2fa'))
            else:
                otp = os.getenv("MASTER_OTP")
                session['temp_otp'] = otp
                return redirect(url_for('verify_2fa'))
        else:
            return render_template("login.html", error="Invalid Credentials!")
            
    return render_template("login.html")

# --- 2FA Verification Route ---
@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'temp_otp' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if user_otp == session.get('temp_otp'):
            session['logged_in'] = True
            session.pop('temp_otp', None) # OTP remove kar do use hone ke baad
            return redirect(url_for('view_db'))
        else:
            return render_template("verify.html", error="Invalid OTP! ❌")

    return render_template("verify.html")# --- Secure Admin Dashboard ---
@app.route('/h24_admin_portal')
def view_db():
    # Check karo ki kya user logged in hai?
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    data = db.session.query(Feedback).all()
    # (Baki tumhara purana HTML table wala code yahan rahega)
   
    return render_template("view.html",data=data)

# --- Logout ---
@app.route('/h24_logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))
# --- CTF Challenge Route ---
@app.route('/challenge_lab')
def challenge_lab():
    return render_template("ctf_lab.html")

# --- Vulnerable API (Hacker ko ise exploit karna hai) ---
@app.route('/api/get_flag', methods=['POST'])
def get_flag():
    data = request.get_json()
    role = data.get('role', 'guest') # Default role 'guest' hai
    
    # Logic: Agar user ne JSON body mein 'role' ko change karke 'admin' kar diya
    # toh use flag mil jayega. Isse kehte hain "Insecure Parameter Handling".
    if role == 'admin':
        return jsonify({"status": "success", "flag": "H24{LOGIC_BYPASS_SUCCESS_2026}"})
    else:
        return jsonify({"status": "error", "message": "Access Denied: Only admins can see the flag!"})
@app.route("/git_config")
def git_config():
    return render_template("gitHub.html")
#-------------------------------------------------------
# All Api's 
#----------------------------------------------------
# Git hub analysis
@app.route("/Git_Hub", methods=["POST"])
def GITHUB():
    data = request.get_json()
    username = data.get("Username")
    
    user_res = requests.get(f"https://api.github.com/users/{username}")
    repo_res = requests.get(f"https://api.github.com/users/{username}/repos")
    
    user_data = user_res.json()
    repo_data = repo_res.json()

    if "message" in user_data and user_data['message'] == 'Not Found':
        return jsonify({"status": "error", "message": "User not found!"})
    
    # 1. Dictionary use karo, string nahi!
    user_final_data = {
        "Name": user_data.get('name') or username,
        "Followers": user_data.get('followers', 0),
        "PublicRepos": user_data.get('public_repos', 0),
        "Repos": [] # Capital R
    }

    # 2. Repo data ko Repos list mein dalo
    if isinstance(repo_data, list): # Check ki data list hi hai
        for repo in repo_data:
            user_final_data["Repos"].append({
                'Name': repo.get('name'),
                'Stars': repo.get('stargazers_count', 0),
                'Language': repo.get('language') or "None",
                'Forks': repo.get('forks_count', 0)
            })

    # 3. f-string mat lagana yahan!
    return jsonify({"status": "success", "User_information": user_final_data})


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
    if request.headers.getlist("X-Forwarded-For"):
        user_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
    else:
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
