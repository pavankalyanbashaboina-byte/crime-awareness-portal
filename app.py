
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'crimeportal2024')

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://yuoimqqlcjxymohkitjg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1b2ltcXFsY2p4eW1vaGtpdGpnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ0OTQyNjQsImV4cCI6MjA5MDA3MDI2NH0.2tEHkVYeGJxt9qg_t9wyLG4xkqqYBA0JRSLlxl9Cuns')

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[OK] Supabase connected")
    except Exception as e:
        print(f"[ERROR] Supabase: {e}")

def get_db():
    if supabase is None:
        raise Exception("Database not configured.")
    return supabase


# ─── Crime Data ───────────────────────────────────────────────────────────────

CRIMES = {
    'ragging': {
        'title': 'Ragging',
        'subtitle': 'Harassment or bullying of junior students',
        'icon': '🚨',
        'color': 'linear-gradient(135deg, #6a1b9a, #8e24aa)',
        'definition': 'Ragging refers to any act that causes physical or psychological harm, discomfort, or humiliation to a student. It includes forcing students to do acts of a sexual nature, physical abuse, mental torture, or any form of humiliation. Ragging is strictly prohibited in all educational institutions across India.',
        'examples': ['Forcing juniors to perform degrading tasks', 'Physical abuse like slapping, punching, or forcing exercise', 'Mental torture including threats and humiliation', 'Forcing students to stay awake all night', 'Sexual abuse or forcing acts of sexual nature', 'Abusing on social media or online platforms'],
        'legal': ['Imprisonment up to 3 years under UGC Regulations', 'Fine up to ₹25,000', 'Suspension or expulsion from college', 'FIR under IPC sections for assault, wrongful confinement', 'Non-bailable offence in serious cases'],
        'academic': ['Immediate suspension from college', 'Cancellation of admission', 'Debarment from examinations', 'Withholding of results and certificates', 'Permanent expulsion in severe cases'],
        'laws': ['UGC Anti-Ragging Regulations 2009', 'IPC Section 339', 'IPC Section 340', 'IPC Section 352', 'State Anti-Ragging Act'],
        'how_to_report': 'Report ragging immediately to the Anti-Ragging Squad, Warden, or Principal. You can also call the UGC Anti-Ragging Helpline: 1800-180-5522 (toll-free). Reports can be filed anonymously.'
    },
    'drug': {
        'title': 'Drug Use/Distribution',
        'subtitle': 'Possession, use, or supply of illegal substances',
        'icon': '💊',
        'color': 'linear-gradient(135deg, #ad1457, #c2185b)',
        'definition': 'Drug-related offences include the possession, use, distribution, or sale of narcotic drugs and psychotropic substances. This is one of the most serious crimes under Indian law and carries severe penalties including long-term imprisonment.',
        'examples': ['Possessing marijuana, cocaine, heroin or other narcotics', 'Selling or distributing drugs to other students', 'Being under the influence of drugs on campus', 'Storing drugs in hostel rooms or lockers', 'Using prescription drugs without a prescription'],
        'legal': ['Imprisonment from 6 months to life under NDPS Act', 'Fine ranging from ₹10,000 to ₹1,00,000', 'Non-bailable and non-compoundable offence', 'Asset seizure and forfeiture', 'Criminal record affecting future employment'],
        'academic': ['Immediate rustication from college', 'Permanent expulsion', 'Cancellation of all academic records', 'Blacklisting from other institutions', 'Report sent to parents and guardians'],
        'laws': ['NDPS Act 1985', 'IPC Section 328', 'Prevention of Illicit Traffic in Narcotic Drugs Act', 'Juvenile Justice Act (for minors)'],
        'how_to_report': 'Report drug-related activities to the college security, warden, or principal immediately. You can also contact the local police (100) or the Narcotics Control Bureau.'
    },
    'violence': {
        'title': 'Physical Violence',
        'subtitle': 'Causing bodily harm through force or aggression',
        'icon': '👊',
        'color': 'linear-gradient(135deg, #e65100, #f4511e)',
        'definition': 'Physical violence includes any act of intentionally causing bodily harm to another person through force, assault, battery, or any form of physical aggression.',
        'examples': ['Punching, kicking, or slapping another student or faculty', 'Assault with objects or weapons', 'Group violence or mob attacks', 'Physical intimidation or threatening gestures', 'Causing grievous hurt requiring medical attention'],
        'legal': ['Simple assault: up to 3 months imprisonment (IPC 351)', 'Grievous hurt: up to 7 years imprisonment (IPC 325)', 'Assault with weapons: up to 10 years (IPC 326)', 'Attempt to murder: up to life imprisonment (IPC 307)', 'Police FIR and criminal trial'],
        'academic': ['Immediate suspension pending inquiry', 'Expulsion for serious cases', 'Academic year cancellation', 'Hostel eviction', 'Report to parents and law enforcement'],
        'laws': ['IPC Section 351-358', 'IPC Section 323-326', 'IPC Section 307', 'CrPC Section 107'],
        'how_to_report': 'Seek immediate medical attention if injured. Report to the college security, principal, or police (100) immediately. Preserve any evidence including photographs of injuries.'
    },
    'cyberbullying': {
        'title': 'Cyberbullying',
        'subtitle': 'Harassment and bullying using digital platforms',
        'icon': '💻',
        'color': 'linear-gradient(135deg, #880e4f, #ad1457)',
        'definition': 'Cyberbullying involves using digital technology to harass, intimidate, threaten, or humiliate another person. It includes posting false information, sharing private images without consent, or sending threatening messages.',
        'examples': ['Sending threatening or abusive messages on WhatsApp/Instagram', 'Creating fake profiles to harass someone', 'Sharing private photos or videos without consent', 'Posting false and defamatory content online', 'Online stalking or monitoring someone without consent'],
        'legal': ['Up to 3 years imprisonment under IT Act Section 66A', 'Up to 5 years for sharing private images (Section 66E)', 'Up to 3 years for identity theft (Section 66C)', 'Fine up to ₹5,00,000', 'Cybercrime police complaint and investigation'],
        'academic': ['Suspension from college', 'Expulsion for severe cases', 'Confiscation of devices used for harassment', 'Mandatory counselling', 'Parental notification'],
        'laws': ['IT Act 2000 Section 66A', 'IT Act Section 66C & 66E', 'IPC Section 499-500 (Defamation)', 'IPC Section 507 (Criminal Intimidation)'],
        'how_to_report': 'Report cyberbullying to the college IT cell or counsellor. File a complaint at cybercrime.gov.in or call the Cybercrime Helpline: 1930.'
    },
    'cheating': {
        'title': 'Exam Cheating',
        'subtitle': 'Using unfair means in academic evaluations',
        'icon': '📝',
        'color': 'linear-gradient(135deg, #2e7d32, #388e3c)',
        'definition': 'Exam cheating includes any act of academic dishonesty during examinations or assessments. This covers using unauthorized materials, copying, impersonation, and bribery of examiners.',
        'examples': ['Copying from another student during exams', 'Using cheat sheets, mobile phones, or electronic devices', 'Impersonating another student in exams', 'Plagiarism in assignments and projects', 'Bribing invigilators or faculty for marks'],
        'legal': ['Up to 3 years imprisonment under state malpractice acts', 'Fine up to ₹10,000', 'Debarment from public examinations', 'Criminal charges for impersonation (IPC 419-420)', 'FIR for bribery under Prevention of Corruption Act'],
        'academic': ['Zero marks in the subject/exam', 'Debarment from current semester exams', 'Debarment from all university exams for 1-3 years', 'Cancellation of degree if discovered after graduation', 'Permanent academic record notation'],
        'laws': ['Andhra Pradesh Malpractices Act', 'IPC Section 419-420', 'University Examination Rules', 'Prevention of Corruption Act 1988'],
        'how_to_report': 'Report exam malpractice to the chief superintendent of exams, the principal, or university examination controller.'
    },
    'theft': {
        'title': 'Theft',
        'subtitle': 'Stealing another person\'s property',
        'icon': '🔓',
        'color': 'linear-gradient(135deg, #6a1b9a, #8e24aa)',
        'definition': 'Theft is the dishonest taking of property belonging to another person with the intention of permanently depriving them of it.',
        'examples': ['Stealing money, phones, or laptops from hostels or classrooms', 'Pickpocketing in college premises', 'Stealing lab equipment or library books', 'Taking another student\'s assignments or intellectual work'],
        'legal': ['Simple theft: up to 3 years imprisonment (IPC 379)', 'Theft in a building: up to 3 years + fine (IPC 380)', 'Robbery: up to 10 years (IPC 392)', 'Dacoity: up to life imprisonment (IPC 395)', 'Police FIR and criminal prosecution'],
        'academic': ['Suspension from college', 'Expulsion for repeat offenders', 'Disciplinary committee inquiry', 'Restitution of stolen property or compensation', 'Parental notification'],
        'laws': ['IPC Section 378-382', 'IPC Section 392-402'],
        'how_to_report': 'Report theft immediately to college security and the principal\'s office. Also file an FIR at the nearest police station.'
    },
    'harassment': {
        'title': 'Sexual Harassment (Student)',
        'subtitle': 'Unwanted sexual behavior or advances',
        'icon': '⚠️',
        'color': 'linear-gradient(135deg, #ad1457, #c2185b)',
        'definition': 'Sexual harassment includes any unwelcome sexual advances, requests for sexual favors, or verbal or physical conduct of a sexual nature.',
        'examples': ['Unwanted physical contact or touching', 'Sending sexually explicit messages or images', 'Making sexual comments or jokes', 'Stalking or following someone persistently', 'Demanding sexual favors in exchange for grades or favors'],
        'legal': ['Up to 3 years imprisonment under POSH Act', 'Up to 7 years under IPC Section 354', 'Up to life imprisonment for rape (IPC 376)', 'Non-bailable offence', 'Mandatory inquiry by ICC within 90 days'],
        'academic': ['Immediate suspension pending inquiry', 'Expulsion after proven guilt', 'Debarment from campus activities', 'Report to police in serious cases', 'Perpetrator bears cost of legal proceedings'],
        'laws': ['POSH Act 2013', 'IPC Section 354', 'IPC Section 354A-D', 'IPC Section 376', 'UGC Regulations on Sexual Harassment 2015'],
        'how_to_report': 'Report to the Internal Complaints Committee (ICC) of the college in writing. Call Women Helpline 181 for immediate assistance.'
    },
    'vandalism': {
        'title': 'Vandalism',
        'subtitle': 'Damaging college or public property',
        'icon': '🏚️',
        'color': 'linear-gradient(135deg, #e65100, #f4511e)',
        'definition': 'Vandalism involves deliberately damaging or destroying property belonging to the college, government, or other individuals.',
        'examples': ['Breaking windows, doors, or furniture', 'Graffiti on college walls or buildings', 'Destroying lab equipment or computers', 'Damaging vehicles in the college parking', 'Setting fire to property'],
        'legal': ['Up to 2 years imprisonment (IPC 427)', 'Up to 5 years for substantial damage (IPC 435)', 'Full compensation for damage caused', 'Fine as determined by court', 'Criminal record'],
        'academic': ['Suspension from college', 'Mandatory payment of damages', 'Expulsion for serious cases', 'Community service as penalty', 'Permanent disciplinary record'],
        'laws': ['IPC Section 425-440', 'Prevention of Damage to Public Property Act 1984'],
        'how_to_report': 'Report vandalism to college security or administration. Photograph the damage as evidence.'
    },
    'sexualHarassmentFaculty': {
        'title': 'Sexual Harassment by Faculty',
        'subtitle': 'Professional misconduct of a sexual nature',
        'icon': '⚠️',
        'color': 'linear-gradient(135deg, #6a1b9a, #8e24aa)',
        'definition': 'Sexual harassment by faculty members is a serious abuse of power and professional trust.',
        'examples': ['Demanding sexual favors for grades or opportunities', 'Making inappropriate sexual comments to students', 'Unwanted physical contact during consultations', 'Sending inappropriate messages or emails', 'Threatening academic consequences for refusing advances'],
        'legal': ['Up to 3 years imprisonment under POSH Act', 'Up to 7 years under IPC Section 354', 'Termination of employment', 'Debarment from teaching profession', 'Non-bailable offence'],
        'academic': ['Immediate suspension pending inquiry', 'Dismissal from service', 'Forfeiture of pension and benefits', 'Blacklisting from academic institutions', 'Mandatory reporting to regulatory bodies'],
        'laws': ['POSH Act 2013', 'IPC Section 354A', 'UGC Regulations 2015', 'Service conduct rules'],
        'how_to_report': 'File a written complaint with the Internal Complaints Committee (ICC). Complaints must be addressed within 90 days.'
    },
    'bribery': {
        'title': 'Bribery/Corruption',
        'subtitle': 'Accepting or giving benefits for unfair advantage',
        'icon': '💰',
        'color': 'linear-gradient(135deg, #ad1457, #c2185b)',
        'definition': 'Bribery involves accepting or offering money, gifts, or favors in exchange for academic advantages such as marks, attendance, or exam results.',
        'examples': ['Accepting money to increase student marks or grades', 'Taking gifts for granting attendance', 'Sharing exam papers in exchange for payment', 'Favoritism in placement or scholarship recommendations'],
        'legal': ['Up to 7 years imprisonment under Prevention of Corruption Act', 'Fine as determined by court', 'Recovery of all assets acquired through corruption', 'Lifetime ban from government service'],
        'academic': ['Immediate dismissal from service', 'Forfeiture of all benefits', 'Debarment from academic appointments', 'Report to university and regulatory bodies'],
        'laws': ['Prevention of Corruption Act 1988', 'IPC Section 161-165', 'Anti-Corruption Bureau regulations'],
        'how_to_report': 'Report bribery to the Anti-Corruption Bureau, principal, or university ombudsman.'
    },
    'fraud': {
        'title': 'Academic Fraud',
        'subtitle': 'Manipulating academic records or research',
        'icon': '📄',
        'color': 'linear-gradient(135deg, #e65100, #f4511e)',
        'definition': 'Academic fraud by faculty includes manipulating grades, fabricating research data, plagiarizing research work, falsifying credentials, or misusing research funds.',
        'examples': ['Changing student grades without authorization', 'Fabricating or falsifying research data', 'Plagiarizing student work or others\' research', 'Misrepresenting academic qualifications'],
        'legal': ['Up to 7 years for fraud under IPC Section 420', 'Up to 2 years for forgery (IPC 463)', 'Fine and recovery of misappropriated funds', 'Retraction of research papers'],
        'academic': ['Immediate dismissal', 'Retraction of fraudulent publications', 'Cancellation of degrees obtained fraudulently', 'Report to UGC and professional bodies'],
        'laws': ['IPC Section 420', 'IPC Section 463-471', 'Research Integrity guidelines', 'UGC Regulations'],
        'how_to_report': 'Report academic fraud to the principal, university registrar, or UGC.'
    },
    'discrimination': {
        'title': 'Discrimination',
        'subtitle': 'Unfair treatment based on identity',
        'icon': '🚫',
        'color': 'linear-gradient(135deg, #880e4f, #ad1457)',
        'definition': 'Discrimination involves treating students unfairly based on caste, religion, gender, disability, language, or other protected characteristics.',
        'examples': ['Giving lower grades to students based on caste or religion', 'Denying opportunities based on gender or disability', 'Using casteist or communal language in class', 'Segregating students based on religion or caste'],
        'legal': ['Up to 5 years for caste discrimination (SC/ST Act)', 'Fine and compensation to victim', 'Up to 3 years under IPC Section 153A', 'Service termination'],
        'academic': ['Suspension and disciplinary inquiry', 'Dismissal from service', 'Mandatory sensitivity training', 'Report to Equal Opportunity Cell'],
        'laws': ['SC/ST Prevention of Atrocities Act 1989', 'Persons with Disabilities Act', 'IPC Section 153A', 'Constitution Article 15 & 16'],
        'how_to_report': 'Report discrimination to the Equal Opportunity Cell, SC/ST Cell, or principal.'
    },
    'authority': {
        'title': 'Misuse of Authority',
        'subtitle': 'Abusing power or position for personal gain',
        'icon': '👤',
        'color': 'linear-gradient(135deg, #2e7d32, #388e3c)',
        'definition': 'Misuse of authority involves faculty members using their position to gain personal benefits, intimidate students, or act in ways that violate professional ethics.',
        'examples': ['Forcing students to do personal work or errands', 'Threatening poor grades for non-compliance', 'Misusing departmental funds for personal use'],
        'legal': ['Criminal breach of trust: up to 7 years (IPC 405)', 'Misappropriation charges under Prevention of Corruption Act', 'Civil liability for damages'],
        'academic': ['Suspension and departmental inquiry', 'Dismissal from service', 'Recovery of misused funds'],
        'laws': ['IPC Section 405-409', 'Prevention of Corruption Act 1988', 'Service Conduct Rules'],
        'how_to_report': 'Report misuse of authority to the principal, department head, or university ombudsman.'
    },
    'leakage': {
        'title': 'Exam Paper Leakage',
        'subtitle': 'Unauthorized sharing of confidential exam content',
        'icon': '📋',
        'color': 'linear-gradient(135deg, #6a1b9a, #8e24aa)',
        'definition': 'Exam paper leakage involves the unauthorized disclosure of examination questions before the scheduled exam time.',
        'examples': ['Sharing question papers with students before exams', 'Photographing and distributing exam papers', 'Selling exam papers for monetary gain'],
        'legal': ['Up to 3 years imprisonment under examination act', 'Fine up to ₹1,00,000', 'Criminal breach of trust (IPC 405)', 'Cheating and fraud charges (IPC 420)'],
        'academic': ['Immediate dismissal', 'Cancellation of the compromised examination', 'Report to university and affiliating body'],
        'laws': ['State Examination Malpractices Acts', 'IPC Section 405', 'IPC Section 420'],
        'how_to_report': 'Report exam paper leakage immediately to the principal, controller of examinations, or university.'
    },
    'cybercrime': {
        'title': 'Cybercrime',
        'subtitle': 'Illegal activities conducted through digital means',
        'icon': '🖥️',
        'color': 'linear-gradient(135deg, #6a1b9a, #8e24aa)',
        'definition': 'Cybercrime encompasses a wide range of illegal activities committed using computers, networks, or the internet.',
        'examples': ['Hacking into college systems or student accounts', 'Phishing attacks to steal credentials', 'Spreading viruses or malware', 'Online financial fraud and scams'],
        'legal': ['Up to 3 years imprisonment under IT Act Section 66', 'Up to 7 years for attacking critical infrastructure', 'Fine up to ₹5,00,000'],
        'academic': ['Immediate suspension', 'Expulsion for serious cases', 'Confiscation of devices'],
        'laws': ['IT Act 2000', 'IT Amendment Act 2008', 'IPC Section 420'],
        'how_to_report': 'Report cybercrime at cybercrime.gov.in or call 1930.'
    },
    'defamation': {
        'title': 'Defamation',
        'subtitle': 'False statements that damage someone\'s reputation',
        'icon': '🗣️',
        'color': 'linear-gradient(135deg, #ad1457, #c2185b)',
        'definition': 'Defamation involves making false statements of fact that damage another person\'s reputation.',
        'examples': ['Spreading false rumors about a student or teacher', 'Publishing defamatory posts on social media', 'Sending defamatory messages in college WhatsApp groups'],
        'legal': ['Up to 2 years imprisonment under IPC Section 500', 'Fine as determined by court', 'Civil liability and damages to victim'],
        'academic': ['Disciplinary inquiry and suspension', 'Mandatory apology and retraction', 'Expulsion for severe cases'],
        'laws': ['IPC Section 499-500', 'IT Act Section 66A', 'Civil Defamation Law'],
        'how_to_report': 'Report defamation to the college disciplinary committee or directly to police.'
    },
    'forgery': {
        'title': 'Forgery of Documents',
        'subtitle': 'Creating or altering documents fraudulently',
        'icon': '📝',
        'color': 'linear-gradient(135deg, #e65100, #f4511e)',
        'definition': 'Forgery involves creating, altering, or using false documents with the intent to deceive.',
        'examples': ['Forging medical certificates for attendance', 'Altering grade sheets or mark cards', 'Creating fake scholarship or bonafide certificates'],
        'legal': ['Up to 2 years imprisonment under IPC Section 465', 'Up to 7 years for forging specific documents (IPC 467)', 'Fine and compensation'],
        'academic': ['Cancellation of admission or degree', 'Immediate expulsion', 'Recovery of any scholarships or benefits'],
        'laws': ['IPC Section 463-471', 'IPC Section 420'],
        'how_to_report': 'Report forgery to the college administration or police.'
    },
    'identity': {
        'title': 'Identity Theft',
        'subtitle': 'Using someone else\'s personal information illegally',
        'icon': '🪪',
        'color': 'linear-gradient(135deg, #880e4f, #ad1457)',
        'definition': 'Identity theft involves using another person\'s personal information without their consent, typically for fraudulent purposes.',
        'examples': ['Using another student\'s login to access college systems', 'Impersonating another student in exams', 'Using someone\'s Aadhar or ID for fraud'],
        'legal': ['Up to 3 years imprisonment under IT Act Section 66C', 'Fine up to ₹1,00,000', 'Up to 5 years for cheating by impersonation (IPC 419)'],
        'academic': ['Immediate suspension and inquiry', 'Expulsion', 'Cancellation of fraudulently obtained benefits'],
        'laws': ['IT Act Section 66C', 'IPC Section 419', 'IPC Section 420'],
        'how_to_report': 'Report identity theft immediately to college authorities and file a complaint at cybercrime.gov.in.'
    },
    'financial': {
        'title': 'Financial Fraud',
        'subtitle': 'Deceiving others for financial gain',
        'icon': '💸',
        'color': 'linear-gradient(135deg, #2e7d32, #388e3c)',
        'definition': 'Financial fraud involves any deceptive act for financial gain including misappropriating funds and creating fake receipts.',
        'examples': ['Creating fake fee receipts or financial documents', 'Misappropriating college funds or scholarship money', 'Running Ponzi schemes or fake investment groups'],
        'legal': ['Up to 7 years imprisonment under IPC Section 420', 'Full recovery of defrauded amount', 'Additional fine'],
        'academic': ['Immediate dismissal or expulsion', 'Recovery of all misappropriated funds', 'Report to police and regulatory bodies'],
        'laws': ['IPC Section 420', 'IPC Section 405-409', 'Prevention of Money Laundering Act'],
        'how_to_report': 'Report financial fraud to college administration, police, and the bank involved.'
    }
}


# ─── Auth Decorators ──────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user_id  = request.form.get('userId', '').strip()
        password = request.form.get('password', '').strip()
        role     = request.form.get('role', '').strip()

        if not user_id or not password or not role:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        try:
            db = get_db()
            result = db.table('users').select('*').eq('user_id', user_id).eq('role', role).execute()
            if not result.data:
                return jsonify({'success': False, 'message': 'Invalid ID or password'}), 401
            user = result.data[0]
            if user['password_hash'] != password:
                return jsonify({'success': False, 'message': 'Invalid ID or password'}), 401

            session['user_id'] = user['user_id']
            session['role']    = user['role']
            session['db_id']   = user['id']

            redirect_url = url_for('admin') if role == 'admin' else url_for('dashboard')
            return jsonify({'success': True, 'redirect': redirect_url})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    data     = request.get_json()
    user_id  = data.get('userId', '').strip()
    password = data.get('password', '').strip()
    role     = data.get('role', '').strip()

    if not user_id or not password or not role:
        return jsonify({'success': False, 'message': 'All fields required'}), 400
    if role not in ['student', 'faculty']:
        return jsonify({'success': False, 'message': 'Invalid role'}), 400

    try:
        db = get_db()
        existing = db.table('users').select('id').eq('user_id', user_id).execute()
        if existing.data:
            return jsonify({'success': False, 'message': 'User ID already exists'}), 409
        db.table('users').insert({'user_id': user_id, 'role': role, 'password_hash': password}).execute()
        return jsonify({'success': True, 'message': 'Registered successfully! Please login.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    notifications = []
    try:
        db = get_db()
        result = db.table('notifications').select('*').eq('user_id', session['user_id']).order('created_at', desc=True).execute()
        notifications = result.data or []
        # Mark all as read
        db.table('notifications').update({'is_read': True}).eq('user_id', session['user_id']).eq('is_read', False).execute()
    except:
        pass
    return render_template('dashboard.html',
                           user_id=session['user_id'],
                           role=session['role'],
                           notifications=notifications)


@app.route('/student')
@login_required
def student():
    return render_template('student.html', user_id=session['user_id'], role=session['role'])


@app.route('/faculty')
@login_required
def faculty():
    return render_template('faculty.html', user_id=session['user_id'], role=session['role'])


@app.route('/both')
@login_required
def both():
    return render_template('both.html', user_id=session['user_id'], role=session['role'])


@app.route('/committees')
@login_required
def committees():
    return render_template('committees.html', user_id=session['user_id'], role=session['role'])


@app.route('/legal')
@login_required
def legal():
    return render_template('legal.html', user_id=session['user_id'], role=session['role'])


@app.route('/crime/<crime_id>')
@login_required
def crime_detail(crime_id):
    crime = CRIMES.get(crime_id)
    if not crime:
        return redirect(url_for('dashboard'))
    return render_template('crime_detail.html',
                           crime=crime,
                           user_id=session['user_id'],
                           role=session['role'])


@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        accused_name     = request.form.get('accusedName', '').strip()
        department       = request.form.get('department', '').strip()
        accused_role     = request.form.get('accusedRole', '').strip()
        violation_type   = request.form.get('violationType', '').strip()
        description      = request.form.get('description', '').strip()
        incident_date    = request.form.get('incidentDate', '').strip()
        anonymous        = request.form.get('anonymous') == 'on'
        reporter_name    = request.form.get('reporterName', '').strip()
        reporter_roll    = request.form.get('reporterRollNo', '').strip()
        reporter_dept    = request.form.get('reporterDept', '').strip()
        reporter_contact = request.form.get('reporterContact', '').strip()

        if not accused_name or not department or not violation_type or not description:
            return jsonify({'success': False, 'message': 'Accused name, department, violation type and description are required'}), 400

        try:
            db = get_db()
            db.table('reports').insert({
                'accused_name':     accused_name,
                'department':       department,
                'accused_role':     accused_role,
                'violation_type':   violation_type,
                'description':      description,
                'incident_date':    incident_date or None,
                'anonymous':        anonymous,
                'reported_by':      None if anonymous else session['user_id'],
                'reporter_role':    None if anonymous else session['role'],
                'reporter_name':    None if anonymous else reporter_name,
                'reporter_contact': None if anonymous else reporter_contact,
                'reporter_dept':    None if anonymous else reporter_dept,
                'reporter_roll':    None if anonymous else reporter_roll,
                'status':           'pending'
            }).execute()
            return jsonify({'success': True, 'message': 'Report submitted successfully! The admin will review your report and respond shortly.'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    return render_template('report.html', user_id=session['user_id'], role=session['role'])


@app.route('/admin')
@admin_required
def admin():
    try:
        db = get_db()
        reports     = db.table('reports').select('*').order('created_at', desc=True).execute()
        all_reports = reports.data or []
        total    = len(all_reports)
        pending  = sum(1 for r in all_reports if r.get('status') == 'pending')
        resolved = sum(1 for r in all_reports if r.get('status') == 'resolved')
        return render_template('admin.html',
                               reports=all_reports, total=total,
                               pending=pending, resolved=resolved,
                               user_id=session['user_id'])
    except Exception as e:
        return render_template('admin.html',
                               reports=[], total=0, pending=0, resolved=0,
                               user_id=session['user_id'], error=str(e))


@app.route('/api/report/<int:report_id>/action', methods=['POST'])
@admin_required
def take_action(report_id):
    data         = request.get_json()
    new_status   = data.get('status', 'resolved')
    action_taken = data.get('action_taken', '').strip()
    target_user  = data.get('user_id', '').strip()

    if not action_taken:
        return jsonify({'success': False, 'message': 'Action description is required'}), 400

    try:
        db = get_db()
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()

        # Update report status and action
        db.table('reports').update({
            'status':       new_status,
            'action_taken': action_taken,
            'action_by':    session['user_id'],
            'action_at':    now
        }).eq('id', report_id).execute()

        # Send notification to the student who reported
        if target_user:
            db.table('notifications').insert({
                'user_id':      target_user,
                'report_id':    report_id,
                'message':      f'Your misconduct report #{report_id} has been reviewed by the admin. Status updated to: {new_status.replace("_", " ").title()}.',
                'action_taken': action_taken,
                'is_read':      False
            }).execute()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/report/<int:report_id>/status', methods=['PATCH'])
@admin_required
def update_report_status(report_id):
    data       = request.get_json()
    new_status = data.get('status')
    if new_status not in ['pending', 'under_review', 'resolved']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    try:
        db = get_db()
        db.table('reports').update({'status': new_status}).eq('id', report_id).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
