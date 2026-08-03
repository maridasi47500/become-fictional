from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_job_or_status", methods=["GET","POST"])
def add_one_job_or_status():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into job_or_status (name) values (:name)",hey)
        user = query_db('select * from job_or_status')

        return render_template("job_or_statusform.html", job_or_statuss=user, one_user=one_user, the_title="add new job_or_status")


    user = query_db('select * from job_or_status')
    one_user = query_db("select * from job_or_status limit 1", one=True)
    return render_template("job_or_statusform.html", job_or_statuss=user, one_user=one_user, the_title="add new job_or_status")

@app.route("/add_one_city", methods=["GET","POST"])
def add_one_city():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into city (name) values (:name)",hey)
        user = query_db('select * from city')

        return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city")


    user = query_db('select * from city')
    one_user = query_db("select * from city limit 1", one=True)
    return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city")

@app.route("/add_one_language", methods=["GET","POST"])
def add_one_language():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into language (name,short_name) values (:name,:short_name)",hey)
        user = query_db('select * from language')

        return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")


    user = query_db('select * from language')
    one_user = query_db("select * from language limit 1", one=True)
    return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        touslesjob_or_status= query_db("select * from job_or_status")

        one_user = query_db("insert into user (phone,country_id,username,email,password,job_or_status_id) values (:phone,:country_id,:username,:email,:password,:job_or_status_id)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['phone','country_id','username','email','password','job_or_status_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry, touslesjob_or_status=touslesjob_or_status)


    touslescountry= query_db("select * from country")

    touslesjob_or_status= query_db("select * from job_or_status")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry, touslesjob_or_status=touslesjob_or_status)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['phone','country_id','username','email','password','job_or_status_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['phone','country_id','username','email','password','job_or_status_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_voyage", methods=["GET","POST"])
def add_one_voyage():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        touslescity= query_db("select * from city")

        touslescountry= query_db("select * from country")

        one_user = query_db("insert into voyage (user_id,city_id,country_id) values (:user_id,:city_id,:country_id)",hey)
        user = query_db('select * from voyage')

        return render_template("voyageform.html", voyages=user, one_user=one_user, the_title="add new voyage", touslesuser=touslesuser, touslescity=touslescity, touslescountry=touslescountry)


    touslesuser= query_db("select * from user")

    touslescity= query_db("select * from city")

    touslescountry= query_db("select * from country")

    user = query_db('select * from voyage')
    one_user = query_db("select * from voyage limit 1", one=True)
    return render_template("voyageform.html", voyages=user, one_user=one_user, the_title="add new voyage", touslesuser=touslesuser, touslescity=touslescity, touslescountry=touslescountry)

@app.route("/add_one_post", methods=["GET","POST"])
def add_one_post():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        tousleslanguage= query_db("select * from language")

        one_user = query_db("insert into post (user_id,language_id,content) values (:user_id,:language_id,:content)",hey)
        user = query_db('select * from post')

        return render_template("postform.html", posts=user, one_user=one_user, the_title="add new post", touslesuser=touslesuser, tousleslanguage=tousleslanguage)


    touslesuser= query_db("select * from user")

    tousleslanguage= query_db("select * from language")

    user = query_db('select * from post')
    one_user = query_db("select * from post limit 1", one=True)
    return render_template("postform.html", posts=user, one_user=one_user, the_title="add new post", touslesuser=touslesuser, tousleslanguage=tousleslanguage)

@app.route("/add_one_product", methods=["GET","POST"])
def add_one_product():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into product (user_id,nom,description,prix,product_type,image,categories) values (:user_id,:nom,:description,:prix,:product_type,:image,:categories)",hey)
        user = query_db('select * from product')

        return render_template("productform.html", products=user, one_user=one_user, the_title="add new product", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from product')
    one_user = query_db("select * from product limit 1", one=True)
    return render_template("productform.html", products=user, one_user=one_user, the_title="add new product", touslesuser=touslesuser)

@app.route("/add_one_creation_or_activity", methods=["GET","POST"])
def add_one_creation_or_activity():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into creation_or_activity (type,name,description,pic,user_id) values (:type,:name,:description,:pic,:user_id)",hey)
        user = query_db('select * from creation_or_activity')

        return render_template("creation_or_activityform.html", creation_or_activitys=user, one_user=one_user, the_title="add new creation_or_activity", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from creation_or_activity')
    one_user = query_db("select * from creation_or_activity limit 1", one=True)
    return render_template("creation_or_activityform.html", creation_or_activitys=user, one_user=one_user, the_title="add new creation_or_activity", touslesuser=touslesuser)

