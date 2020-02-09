from flask import Flask 
from flask import render_template, request, flash, redirect, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = 'yeet4321'

@app.route('/')
def home(): 
    # if request.method == 'POST':  
    #     f = request.files['file']  
    #     f.save('uploads/' + f.filename)  

    #     # upload the the audio to google cloud and return the uri 
    #     upload_blob(cf.bucketname, 'uploads/'+f.filename , f.filename)

    #     # Build uri suing the filename suplied by user 
    #     gcs_uri = 'gs://' + cf.bucketname + '/' + f.filename

    #     # execute transcribe function on the gcs_uri save the transcript to full_transcript
    #     full_transcript = sample_long_running_recognize(gcs_uri, f.filename)
    
    # # Return template success.html save the name & contents of file to vars 
    # return render_template("success.html", name = f.filename, text = full_transcript)  
    
    return render_template('home.html')


# start of form classes
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, IntegerField

class PostformForm(FlaskForm):
    id = HiddenField()
    postTitle = StringField('Lecture Title')
    postBody = StringField('Comma Sepparated Keywords')
    submit = SubmitField("Save")

# Start of database classes
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/employee.db"
db = SQLAlchemy(app)

class Postform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postTitle = db.Column(db.String)
    postBody = db.Column(db.String)
    references = db.Column(db.String)
    
    def __repr__(self):
        return "(%r, %r)" %(self.postTitle,self.postBody)

# view


@app.route("/postform", methods=["GET", "POST"])
def createPostform():
    form = PostformForm(request.form)
    postforms = Postform.query.all()
    if form.validate_on_submit():
        postform = Postform(postTitle=form.postTitle.data, postBody=form.postBody.data)
        db.session.add(postform)
        db.session.commit()
        flash("Added Postform Successfully")
        return redirect(url_for("createPostform"))
    return render_template("postform.html", title="Postform", form=form, postforms=postforms)

@app.route("/updatePostform/<int:postform_id>", methods=["GET", "POST"])
def updatePostform(postform_id):
    postform = Postform.query.get(postform_id)
    form = PostformForm(request.form, obj=postform)
    if form.validate_on_submit():
        form.populate_obj(postform)
        db.session.commit()
        flash("Updated Postform Successfully")
        return redirect(url_for("createPostform"))
    return render_template("postform.html", title="Postform", form=form, postforms=Postform.query.all())

@app.route("/deletePostform/<int:postform_id>", methods=["GET", "POST"])
def deletePostform(postform_id):
    postform = Postform.query.get(postform_id)
    db.session.delete(postform)
    db.session.commit()
    return redirect(url_for("createPostform"))