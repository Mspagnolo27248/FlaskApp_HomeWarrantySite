from project_files import app,db
from flask import render_template,url_for,redirect,flash,abort,request,session
from flask_login import login_user,logout_user,login_required
from project_files.models import User,TicketModel,CategoryModel
from project_files.forms import RegistrationForm,LoginForm,AddTicketForm


@app.route('/')
def index():
    return  render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
        username = form.username.data,
        password=form.password.data,
        address=form.address.data)

        db.session.add(user)
        db.session.commit()
        flash("Thanks for registation")
        return redirect(url_for('login'))

    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            user_id = user.id
        if not user:
            return redirect(url_for('register'))
        elif user.check_password(form.password.data) and user is not None:
            login_user(user) #This is implmented since we inheret the UserMixin
            flash("Logged In Successfully!")
            next = request.args.get('next') #This is if a user tried to access a page but was redirected
            
            if next == None or next[0]=='/':
                next = url_for('welcome_user',user_id=user_id)
            return redirect(next)
    return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You Logged Out")
    return redirect(url_for('index'))


#@app.route('/welcome_user')
@app.route('/welcome/<user_id>',methods=['GET','POST'])

def welcome_user(user_id=0):
    user_id = int(user_id)
    session['user_id']=user_id
    owner = User.query.get_or_404(user_id).username
    tickets = db.session.query(CategoryModel.category,TicketModel.id,TicketModel.desc,\
        TicketModel.create_date,TicketModel.close_date)\
        .outerjoin(CategoryModel,TicketModel.category_id==CategoryModel.id).filter(TicketModel.home_id==user_id).all()
    return render_template('welcome_user.html',tickets=tickets,user_id=user_id,owner=owner)


@app.route('/ticket/<ticket_id>',methods=['GET','POST'])   

def update_ticket(ticket_id=0):       
    ticket = db.session.query(TicketModel).get(ticket_id)
    user_id = ticket.home_id
    if  request.method =='GET':
        form  = AddTicketForm()
        form.category.choices = [(category.id,category.category) for category in 
        db.session.query(CategoryModel).all()]
        form.desc.data = ticket.desc
        form.closedate.data = ticket.close_date
        form.createdate.data = ticket.create_date
        form.category.data = ticket.category_id
    else:     
        form  = AddTicketForm()
        form.category.choices = [(category.id,category.category) for category in 
        db.session.query(CategoryModel).all()]
           
        if form.validate_on_submit():
            #owner = user_id
            ticket.desc = form.desc.data
            ticket.create_date =form.createdate.data
            ticket.close_date = form.closedate.data
            ticket.category_id = form.category.data
            user_id = ticket.home_id
            #update_item =TicketModel(user_id,desc,create_date,close_date)
            #db.session.add(update_item)
            db.session.commit()
            return redirect(url_for('welcome_user',user_id=user_id))
    return render_template('ticket.html',form=form,user_id=user_id)


    
@app.route('/ticket/<ticket_id>/delete',methods=['GET','POST'])   

def delete(ticket_id):
    ticket = db.session.query(TicketModel).get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Post has been deleted')
    user_id = session['user_id']
    return redirect(url_for('welcome_user',user_id=user_id))


@app.route('/items',methods=['GET','POST'])

def add_item():
    form = AddTicketForm()
    form.category.choices = [(category.id,category.category) for category in 
    db.session.query(CategoryModel).all()]
    user_id = session['user_id']
    if form.validate_on_submit():
        #owner = user_id
        desc = form.desc.data
        create_date =form.createdate.data
        close_date = form.closedate.data
        category = form.category.data

        new_item =TicketModel(user_id,desc,create_date,close_date,category)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('welcome_user',user_id=user_id))
    return render_template('item.html',form=form,user_id=user_id) 


@app.route('/reports')
def reports():
    query = \
        """
        SELECT Category
        ,count(home_id) as Counts
        FROM tickets 
        join category on tickets.category_id = category.id
        GROUP BY Category
        ORDER BY Counts
        
        """
    count_of_tickets = db.session.execute(query)
    mydict  = [{"category":i[0],"value":str(i[1])} for i in count_of_tickets]
    #print(mydict)
    return render_template("reports.html",data = mydict)


if  __name__ =='__main__':

    app.run(debug=True)



