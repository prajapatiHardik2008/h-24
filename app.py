import random
from flask import Flask, render_template, request, jsonify, session, redirect, url_for ,render_template_string,send_from_directory , send_file
import pybase64
import time
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import socket
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask_talisman import Talisman
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
import resend
#----------------------------------------------------------------------
# tools 
#----------------------------------------------------------------------
# Port Scanner import socket
 #set bydefualt 1
def port_scanner(TargetIp, port):
    if TargetIp == '127.0.0.1':
        return 0
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

#-----------------------------------------------------------------------

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
is_render = os.environ.get("RENDER")
app.secret_key = os.getenv('SECRET_KEY')
if is_render:
    app.permanent_session_lifetime = timedelta(minutes=20)
else:
    app.permanent_session_lifetime = timedelta(seconds=50) # for only localy test a

#---------------------------------------------------------------------
#connecting with data base # ... app = Flask(__name__) ke niche ...

basedir = os.path.abspath(os.path.dirname(__file__))
db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///' + os.path.join(basedir, "database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    query = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)

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
# #------------------------------------------------------
# #Run Command
# @app.route('/run_command_page', methods=['POST'])
# def run_command():
#     return render_template("terminal.html")
# @app.route('/run_command', methods=['POST'])
# def execute_command():
#     command = request.form.get('command')
#     if not command:
#         return
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
#------------------------------------------------------
#Image Bg remover 
# @app.route("/bgremover")
# def imgremover():
#     return render_template("bgremover.html")
# @app.route("/remove_bg", methods=["POST"])
# def bgremover():
#     UPLOAD_FOLDER = "uploads"
#     OUTPUT_FOLDER = "outputs"
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     os.makedirs(OUTPUT_FOLDER, exist_ok=True)

#     file = request.files.get("file")
#     output_name = request.form.get("output_file") or "output.png"  # FIX 1: key name sahi kiya
    
#     if not output_name.lower().endswith(('.png', '.jpg', '.jpeg')):
#         output_name += ".png"  # FIX 2: extension auto-add

#     if not file or file.filename == '':
#         return jsonify({"status": "error", "message": "No file selected!"})

#     input_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     output_path = os.path.join(OUTPUT_FOLDER, output_name)  # FIX 3: custom naam use karo
#     file.save(input_path)

#     result = remove_background(input_path, output_path)
#     if "successfully" in result:
#         return send_file(output_path, mimetype='image/png', as_attachment=True, download_name=output_name)
#     else:
#         return jsonify({"status": "error", "message": result})#----------------------------------------------------------------------
#Image bg remover 

    
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
@app.route('/scan_port', methods=['POST'])
def scan_port():
    data = request.json
    target = data.get('ip')
    port = data.get('port')
    if target == '127.0.0.1':
        return jsonify({"status": "closed", "port": "Can't Scan Internal IP !"})
    
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
    fakeotp = random.randint(100000, 999999)
    
    lines = [
        ('🎓', 'BCA Student', '18-year-old Cybersecurity enthusiast at LJ University'),
        ('🐍', 'Python Dev', 'Building secure portals and hacking tools.'),
        ('🚩', 'CTF Player', 'Network forensics and ethical hacking specialist.'),
        ('🛡️', 'H-24 Portal', 'A blend of web development and advanced security.'),
        ('🗄️', 'Backend', 'Self-taught, focused on PostgreSQL and secure code.'),
        ('🏸', 'Fun Fact', 'Badminton player by day, Code architect by night.')
    ]

    rows = ""
    for i in range(min(len(otp), len(lines))):
        emoji, title, desc = lines[i]
        rows += f"""
        <tr>
            <td style="padding:8px 12px;font-size:20px">{emoji}</td>
            <td style="padding:8px 12px;color:#00ff88;font-weight:bold;
                       white-space:nowrap">{otp[i]} — {title}</td>
            <td style="padding:8px 12px;color:#aaaaaa">{desc}</td>
        </tr>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#0a0a0a;font-family:'Courier New',monospace">

      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" style="padding:40px 20px">
            <table width="600" style="background:#111;border:1px solid #00ff88;
                                      border-radius:12px;overflow:hidden">

              <!-- Header -->
              <tr>
                <td style="background:#00ff88;padding:24px;text-align:center">
                  <h1 style="margin:0;color:#0a0a0a;font-size:28px;
                             letter-spacing:4px">H-24 PORTAL</h1>
                  <p style="margin:4px 0 0;color:#0a0a0a;font-size:12px;
                            letter-spacing:2px">SECURE ACCESS SYSTEM</p>
                </td>
              </tr>

              <!-- OTP Box -->
              <tr>
                <td style="padding:32px;text-align:center">
                  <p style="color:#888;font-size:13px;letter-spacing:2px;
                            margin:0 0 12px">YOUR ONE-TIME ACCESS CODE</p>
                  <div style="display:inline-block;background:#0a0a0a;
                              border:2px solid #00ff88;border-radius:8px;
                              padding:16px 40px">
                    <span style="color:#00ff88;font-size:36px;
                                 letter-spacing:8px;font-weight:bold">{fakeotp}</span>
                  </div>
                  <p style="color:#555;font-size:11px;margin:12px 0 0">
                    ⏱ Expires in 5 minutes &nbsp;|&nbsp; Do not share this code
                  </p>
                </td>
              </tr>

              <!-- Divider -->
              <tr>
                <td style="padding:0 32px">
                  <hr style="border:none;border-top:1px solid #222">
                </td>
              </tr>

              <!-- About Section -->
              <tr>
                <td style="padding:24px 32px">
                  <p style="color:#555;font-size:11px;letter-spacing:2px;
                            margin:0 0 16px">// OPERATOR PROFILE</p>
                  <table width="100%" cellpadding="0" cellspacing="0">
                    {rows}
                  </table>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="background:#0a0a0a;padding:16px;text-align:center;
                           border-top:1px solid #222">
                  <p style="color:#333;font-size:11px;margin:0">
                    H-24 Portal &nbsp;•&nbsp; Hardik Prajapati 
                    &nbsp;•&nbsp; If you didn't request this, ignore it.
                  </p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>

    </body>
    </html>"""

    try:
        resend.api_key = os.getenv("RESEND_API")
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "hardikprajapati242008@gmail.com",
            "subject": f"{fakeotp} is your H-24 Access Code",
            "html": html
        })
        print("Email sent successfully")

    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


# ============================================================
# VIEWER LOGIN SYSTEM — Devang ke liye (Read-only access)
# ============================================================

# --- 1. IMPORTS (top pe add karo) ---
# --- 2. DB MODEL () ---

class BlockedIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), unique=True, nullable=False)
    reason = db.Column(db.String(200), nullable=True)

# ============================================================
# --- 3. BLOCKED IP MIDDLEWARE (add_security_headers ke pehle) ---
# ============================================================

@app.before_request
def check_blocked_ip():
    user_ip = request.remote_addr
    if request.headers.getlist("X-Forwarded-For"):
        user_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0]

    # Admin aur viewer login pages ko block mat karo
    allowed_routes = ['viewer_login', 'admin_login', 'static']
    if request.endpoint in allowed_routes:
        return

    blocked = db.session.query(BlockedIP).filter_by(ip_address=user_ip).first()
    if blocked:
        return render_template("blocked.html", ip=user_ip), 403

# ============================================================
# --- 4. VIEWER LOGIN ROUTES ---
# ============================================================
limiter = Limiter(
    get_remote_address,
    default_limits=[],
    app=app
)
@app.route('/viewer_login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def viewer_login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd  = request.form.get('password')

        viewer_user = os.getenv('VIEWER_USER')   # .env mein set karo
        viewer_pass = os.getenv('VIEWER_PASS')   # hashed password

        if user == viewer_user and check_password_hash(viewer_pass, pwd):
            session.permanent = True
            session['viewer_logged_in'] = True
            return redirect(url_for('viewer_dashboard'))
        else:
            return render_template("viewer_login.html", error="Invalid Credentials!")

    return render_template("viewer_login.html")


@app.route('/viewer_dashboard')
def viewer_dashboard():
    if not session.get('viewer_logged_in'):
        return redirect(url_for('viewer_login'))

    data     = db.session.query(Feedback).all()
    blocked  = db.session.query(BlockedIP).all()
    return render_template("viewer_dashboard.html", data=data, blocked=blocked)


@app.route('/viewer_logout')
def viewer_logout():
    session.pop('viewer_logged_in', None)
    return redirect(url_for('viewer_login'))

# ============================================================
# --- 5. IP BLOCK / UNBLOCK APIs (sirf ADMIN ke liye) ---
# ============================================================

@app.route('/admin/block_ip', methods=['POST'])
def block_ip():
    if not session.get('logged_in'):          # sirf main admin
        return jsonify({"status": "error", "msg": "Unauthorized"}), 403

    req_data  = request.get_json()
    ip        = req_data.get('ip', '').strip()
    reason    = req_data.get('reason', 'Blocked by admin')

    if not ip:
        return jsonify({"status": "error", "msg": "IP required"})

    existing = db.session.query(BlockedIP).filter_by(ip_address=ip).first()
    if existing:
        return jsonify({"status": "error", "msg": "IP already blocked"})

    new_block = BlockedIP(ip_address=ip, reason=reason)
    db.session.add(new_block)
    db.session.commit()
    return jsonify({"status": "success", "msg": f"{ip} blocked!"})


@app.route('/admin/unblock_ip', methods=['POST'])
def unblock_ip():
    if not session.get('logged_in'):          # sirf main admin
        return jsonify({"status": "error", "msg": "Unauthorized"}), 403

    req_data = request.get_json()
    ip       = req_data.get('ip', '').strip()

    record = db.session.query(BlockedIP).filter_by(ip_address=ip).first()
    if not record:
        return jsonify({"status": "error", "msg": "IP not found"})

    db.session.delete(record)
    db.session.commit()
    return jsonify({"status": "success", "msg": f"{ip} unblocked!"})

#---------------------------------------------------------
# --- Admin Login Page ---
# --- Login Route (Update) ---
@limiter.limit("5 per hour")
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
limiter =Limiter( 
    get_remote_address,
    app=app,
    default_limits=[]
    )

@app.errorhandler(RateLimitExceeded)
def rate_limit_handler(e):
    return render_template("login.html", 
           error="Too many attempts! Wait 1 minute. 🚫"), 429
@app.route('/verify_2fa', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def verify_2fa():
    if 'temp_otp' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if user_otp == session.get('temp_otp'):
            session.permanent = True
            session['logged_in'] = True

            session.pop('temp_otp', None) # OTP remove kar do use hone ke baad
            return redirect(url_for('view_db'))
        else:
            return render_template("verify.html", error="Invalid OTP! ❌")

    return render_template("verify.html")
# --- Secure Admin Dashboard ---
@app.route('/h24_admin_portal')
def view_db():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    data = db.session.query(Feedback).all()
   
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
    role = data.get('role', 'guest')
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
@app.route('/world')
def world_portal():
    return render_template('world_portal.html')

from flask import request, render_template_string, abort
import datetime

# Fake Login Page HTML (Attacker ko ullu banane ke liye)
FAKE_LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>H-24 Administrative Portal - Login</title>
    <style>
        body { background-color: #0d1117; color: #58a6ff; font-family: monospace; padding: 50px; text-align: center; }
        .login-box { border: 1px solid #21262d; padding: 40px; display: inline-block; background: #161b22; border-radius: 5px; }
        input { display: block; margin: 10px auto; padding: 10px; background: #0d1117; border: 1px solid #30363d; color: white; }
        button { background: #238636; color: white; padding: 10px 20px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🔒 H-24 INTERNAL SYSTEM ACCESS</h2>
        <p style="color: #f85149;">Authorized Personnel Only!</p>
        <form method="POST" action="/admin-auth-trap">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

# ------------------------------------------------------------
# Honey Pot Routes
@app.route('/admin')

@app.route('/administrator')
@app.route('/root')
@app.route('/adminlogin')
@app.route('/phpmyadmin')
@app.route('/wp-admin')
@app.route('/admin.php')   
def honey_pot():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attempted_url = request.path

    # 🚨 1. Terminal par Red Alert Print karo
    print("\n" + "="*60)
    print(f"🚨 [HONEYPOT TRIGGERED] 🚨")
    print(f"🕒 Time: {current_time}")
    print(f"🌐 IP Address: {ip}")
    print(f"📍 Target URL: {attempted_url}")
    print(f"🖥️ User-Agent: {user_agent}")
    print("="*60 + "\n")
    
    try:
        resend.api_key = os.getenv("RESEND_API")
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "hardikprajapati242008@gmail.com",
            "subject": f"🚨 Honeypot Alert: {ip} hit {attempted_url}",
            "html": f"""
            <h3>🚨 H-24 Honeypot Triggered 🚨</h3>
            <p><b>IP Address:</b> {ip}</p>
            <p><b>Target URL:</b> {attempted_url}</p>
            <p><b>User-Agent:</b> {user_agent}</p>
            """
        })
        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")
        return render_template_string(FAKE_LOGIN_TEMPLATE)
    # 📝 2. Isko ek log file me save karo taaki tum baad me analysis kar sako
    with open("honeypot_intruders.log", "a" , encoding="utf-8") as log_file:
        log_file.write(f"[{current_time}] IP: {ip} | URL: {attempted_url} | UA: {user_agent}\n")

    # 🎭 3. Attacker ko fake login page dikhao taaki woh aur ulajh jaye
    return render_template_string(FAKE_LOGIN_TEMPLATE)


# 🕵️‍♂️ 4. Fake Authorization Trap (Agar woh fake page pr credentials dale toh)
@app.route('/admin-auth-trap', methods=['POST'])
def admin_auth_trap():
    ip = request.remote_addr
    username = request.form.get('username')
    password = request.form.get('password')
    
    print("\n" + "💥"*20)
    print(f"💥 [HONEYPOT CREDENTIAL TRAP] 💥")
    print(f"🌐 IP: {ip}")
    print(f"👤 Attempted Username: {username}")
    print(f"🔑 Attempted Password: {password}")
    print("💥"*20 + "\n")

    with open("honeypot_intruders.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"  └─ [CREDENTIALS TRIED] User: {username} | Pass: {password}\n")
        
    # Uska mood kharab karne ke liye hamesha 'Invalid Credentials' ka error do
    return "<p style='color:red; font-family:monospace; text-align:center; padding-top:50px;'>Error 500: Database connection timed out. IP logged.</p>", 403
#-------------------------------------------------------------
#--------------------------------------------------------------
# For limited time admin panel 
# @app.before_request
# def make_session_parmanent():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(seconds=10)
#-------------------------------------------------------------
#Fix Click Jacking 
@app.after_request
def add_security_headers(response):
    # X - Frame for old browsers
     response.headers["X-Frame-Options"] = "SAMEORIGIN"

     # 2. Content-Security-Policy: FOR  Modern browsers  (MOST  Powerful)
     response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
     return response

permissions_policy = {
    'geolocation': '()',      # Not allowed to use geolocation 
    'microphone': '()',       # Not allowed to use Microphone
    'camera': '()',           # Not allowed to use camera in future i'll remove this
    'display-capture': '()',  # Screen recording block
    'payment': '()'           # Payment APIs block
    }


if is_render:
    Talisman(app, content_security_policy=None,permissions_policy=permissions_policy)
    debug_mode = False

else:
    Talisman(app, content_security_policy=None,force_https=False,permissions_policy=permissions_policy)
    debug_mode = True

with app.app_context():
        db.create_all()
if __name__ == '__main__':

    #thread = threading.Thread(target=emailSender,daemon=True)
    #thread.start()
    port = int(os.environ.get("PORT", 8000))

    app.run(host='0.0.0.0', port=port, debug=debug_mode)