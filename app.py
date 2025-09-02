from flask import Flask,render_template,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
from data_sender_in_taligram import send_data_taligram
import quick_shot,img_uploder,os
from datetime import datetime
Local_server = True
# open json file and read
with open("config.json","r") as c:
    paramiter= json.load(c)["para"]

app = Flask(__name__)


# Set the upload folder path
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Set a secret key for session management
app.secret_key = 'your_secret_key_here'
# check server is local or not
if Local_server == True:
    app.config['SQLALCHEMY_DATABASE_URI'] = paramiter["local_url"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = paramiter["produ_url"]
#connect flask to data base
db = SQLAlchemy(app)


# define table in data base for contarct
class Contract(db.Model):
    __tablename__ = 'contract'
    slno = db.Column(db.Integer, primary_key=True)
    User_Name = db.Column(db.String(80), nullable=False)
    User_Email = db.Column(db.String(80), nullable=False)
    User_PhoneNo = db.Column(db.Integer, nullable=False)
    User_Msg = db.Column(db.String(80), nullable=False)

# define table in data base for post
class Post(db.Model):
    __tablename__ ='post'
    slno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Post_Title = db.Column(db.String(80), nullable=False)
    Post_Content = db.Column(db.String(80), nullable=False)
    Post_Author = db.Column(db.String(80), nullable=False)
    Post_Slug = db.Column(db.String(80), nullable=False)
    Post_Image = db.Column(db.String(80), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#for admin logout
@app.route("/logout")
def logout_():
    session.clear()
    return redirect("/login")

#for post delete
@app.route("/del/<int:post_slno>",methods=['GET'])
def post_delete(post_slno):
    username = session.get("log_name")
    userpass = session.get("log_pass")

    if username == paramiter["admin_name"] and userpass == paramiter["pass_word"]:
        post_value = Post.query.filter_by(slno = post_slno).first()
        db.session.delete(post_value)
        db.session.commit()
    
    return redirect("/dashboard")    

@app.route('/')
def index():
    paramiter["subtitle"]="Home"
    return render_template('index.html',paramiter=paramiter)

@app.route('/about')
def about():
    paramiter["subtitle"]="About"

    return render_template('about.html',paramiter=paramiter)

@app.route('/contact',methods =['GET','POST'])
def contact():
    name1=[]
    paramiter["subtitle"]="Contact"
    all_snos = Contract.query.filter_by().all()  # returns a list of tuples
  


    if(request.method == 'POST'):
        name1.append(request.form.get('name'))
        name1.append(request.form.get('email'))
        name1.append(request.form.get('phoneno'))
        name1.append(request.form.get('msg'))
        print(f"my name = {name1[0]} mail = {name1[1]} phone no = {name1[2]} msg = {name1[3]}" )
        entry = Contract(User_Name = name1[0] ,  User_PhoneNo= name1[2] ,User_Email= name1[1],User_Msg=name1[3] )
        db.session.add(entry)
        db.session.commit()
        print((all_snos[-1].slno )+1)
        # data send in taligram
        send_data_taligram(
            f"📄 New Form Submission\n\n"
            f"🔢 Serial No: {(all_snos[-1].slno )+1}\n" #for last value fisrt slno take
            f"👤 Name: {name1[0]}\n"
            f"📧 Email: {name1[1]}\n"
            f"📞 Phone: {name1[2]}\n"
            f"💬 Message: {name1[3]}"
        )
        flash(f" {name1[0]} Your form was submitted successfully!", "success")



    return render_template('contact.html',paramiter=paramiter)


@app.route('/blog')
def blog():
    naxt=[]
    page = request.args.get("name")
    print(  f" afva {(str(page))}")
    if not(str(page).isnumeric() ):
        page = "0"

    page=int(page)

    naxt1=[int(page) ,int(page+paramiter["post_no"]) ]
    if page <= 0:
        naxt=["/blog?name="+str(page) ,"/blog?name="+str(page+paramiter["post_no"]) ]
    elif page >=( (len(Post.query.filter_by().all()))-paramiter["post_no"] ) :
        naxt=["/blog?name="+str(page-paramiter["post_no"]) ,"/blog?name=" +str(page)]
      
    else:
        naxt=["/blog?name="+str(page-paramiter["post_no"]) ,"/blog?name="+str(page+paramiter["post_no"])]



    print(f"aaa {((naxt1[0]))}    asasa {((naxt[1]))} ")
    all_post = Post.query.filter_by().all()[  (naxt1[0]) : (naxt1[1])]
    paramiter["subtitle"]="Blogs"
    return render_template('blog.html',paramiter=paramiter,all_post=all_post,next=naxt)

  
@app.route('/post/<string:post_id>')
def post(post_id):
    post_value = Post.query.filter_by(Post_Slug = post_id).first_or_404()
    paramiter["subtitle"]=post_id
    
    return render_template('post.html',paramiter=paramiter,post_value=post_value)

@app.route('/login',methods =['GET','POST'])
def login():
    paramiter["subtitle"]="Login"
    username = session.get("log_name")
    userpass = session.get("log_pass")

    if username == paramiter["admin_name"] and userpass == paramiter["pass_word"]:
        return redirect("/dashboard") 
    
    if(request.method == 'POST'):
        log_name,log_pass=request.form.get('name'),request.form.get('pass')
        print(log_pass == paramiter['pass_word'])
        if( log_name == paramiter['admin_name'] and log_pass == paramiter['pass_word']):
            session["log_name"],session["log_pass"]= log_name,log_pass
            return redirect("/dashboard") 

    return render_template('login.html',paramiter=paramiter)

@app.route('/dashboard')
def admin_dashboard():
    
    username = session.get("log_name")
    userpass = session.get("log_pass")

    if username != paramiter["admin_name"] and userpass != paramiter["pass_word"]:
        paramiter["subtitle"]="Login"
        return redirect('/login')
    
    all_post = Post.query.filter_by().all() 
    sh_list=[]
    for i in all_post:
        
        sh_list.append(i.slno)
    print(sh_list)
    shot= (sh_list)
    ii=1
    for i in sh_list:
        Target_post = Post.query.filter_by(slno = i).first()
        Target_post.slno =ii
        db.session.commit()
        ii+=1
    # Target_post.slno =

    return render_template('admin-dashboard.html',paramiter=paramiter,all_post=all_post)

@app.route('/edit/<int:post_id>',methods =['GET','POST'])
def edit_post(post_id):
    username = session.get("log_name")
    userpass = session.get("log_pass")

    if username != paramiter["admin_name"] and userpass != paramiter["pass_word"]:
        paramiter["subtitle"]="Login"
        return redirect('/login')
    
    Target_post = Post.query.filter_by(slno = post_id).first()
    if(request.method == 'POST'):
        img= img_uploder.upload_file(app)
        paramiter["subtitle"]=post_id
        Target_post.Post_Title = request.form.get('postTitle')
        Target_post.Post_Content =request.form.get('postContent')
        Target_post.Post_Author=request.form.get('postAuthor')
        Target_post.Post_Slug=request.form.get('postSlug')
        Target_post.Post_Image=img
        db.session.commit()
        flash(f" {request.form.get('postTitle')} Your Post was Edited successfully!", "success")
        return redirect(f'/edit/{post_id}')


    return render_template('admin-post-edit-add.html',paramiter=paramiter,Target_post=Target_post,post_id=post_id,val=f'/edit/{post_id}',active1='')

@app.route('/add',methods =['GET','POST'])
def add_post():
    paramiter["subtitle"]="Post Add"
    username = session.get("log_name")
    userpass = session.get("log_pass")
    name1=[]

    if username != paramiter["admin_name"] and userpass != paramiter["pass_word"]:
        paramiter["subtitle"]="Login"
        return redirect('/login')
    
 

    if(request.method == 'POST'):
        img= img_uploder.upload_file(app)
        print(f' hi sdftgsd gsdgsdgsdgsdgdgs dsgsdg sd ggds{img}')
        name1.append(request.form.get('postTitle'))
        name1.append(request.form.get('postContent'))
        name1.append(request.form.get('postAuthor'))
        name1.append(request.form.get('postSlug'))
        name1.append(img)
        # print(f"my name = {name1[0]} mail = {name1[1]} phone no = {name1[2]} msg = {name1[3]}" )
        entry = Post(Post_Title = name1[0] ,  Post_Content= name1[1] ,Post_Author= name1[2],Post_Slug=name1[3],Post_Image=name1[4])
        db.session.add(entry)
        db.session.commit()
 
        flash(f" {name1[0]} Your Post was Added successfully!", "success")
    return render_template('admin-post-edit-add.html',paramiter=paramiter,Target_post=None,val='/add',active1='active')

# Don't forget this part 😉
if __name__ == '__main__':
        # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=10000, debug=True)




