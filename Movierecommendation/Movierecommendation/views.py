from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
# from .models import Poll
# from users.models import Profile
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
import random
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.models import User
from .utility import carousel_data,movie_name
import difflib
from django.views.decorators.csrf import csrf_exempt

from .summary import movie_summary
from .stream_sites import stream_link
from .colab_filter import recommend
from .closest_user import closest
from .textanalysis import returnlabel
# from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.contrib import auth
# # from django.core.context_processors import csrf
# from .forms import CustomUserCreationForm


import psycopg2
con = psycopg2.connect(
    host = "127.0.0.1",
    database = "movierecommender",
    user = "postgres",
    password = "admin",
    port="5432")

cur=con.cursor()

def index(request):
    lst = carousel_data()
    # print(lst[1],len(lst[1]))
    d = {'posts1': lst[0], 
         'posts2': lst[1], 
         'len': range(lst[2]),
         'l':range(lst[3]),
         'ns':range(4)}
    return render(request, 'index.html',d)


# def login(request):
#     # c = {}
#     # c.update(csrf(request))  
#     return render(request, 'login.html')

def get_details(sess):
    cur.execute("select * from public.user")
    rows = cur.fetchall()
    for row in rows:
        print ("ID = ", row[0])
        print ("firstNAME = ", row[1])
        print ("lastNAME = ", row[2])
        print ("phone = ", type(row[3]))
        print ("gender = ", row[4])
        t=row[5].split(',')
        t.append('emotional')
        print ("genre = ",row[5])
        print ("email = ", row[6])
        print ("password = ", row[7], "\n")
        print(sess)
        if sess == row[6]:
            print(row)
            return row

def movielink(request):
    displaypic=request.form.get('displaypic')
    name=request.POST.get('name')
    year=request.POST.get('year')
    rating=request.POST.get('rating')
    genre=request.POST.get('genre')
    print(displaypic,"\n",name,"\n",year,"\n",rating,"\n",genre,"\n")
    lst=[]
    lst.append(displaypic)
    lst.append(name)
    lst.append(year)
    lst.append(rating)
    lst.append(genre)
    movie_name = lst[1]
    movie_name = movie_name.strip()
    mlink = stream_link(movie_name)
    msummary=movie_summary(movie_name.strip())
    c={
        "displaypic":lst[0],
        "name":lst[1],
        "year":lst[2],
        "rating":lst[3],
        "genre":lst[4],
        "summary":msummary,
        "mstream":mlink
    }
    return render(request, 'movielink.html',c)
    return HttpResponse("404 - Not found")


def update_M_db(mname, email, uid, rating):
    temp_lst=[]
    cur.execute("select index,title from public.movie_database")
    mdata1 = cur.fetchall()
    movie_name_lst=[]
    for m in mdata1:
        movie_name_lst.append([m[0],m[1]])
    for i in movie_name_lst:
        temp_lst.append(i[1])
    t = difflib.get_close_matches(mname,temp_lst)
    for i in t:
        mlistindex = temp_lst.index(i)
        movie_id = movie_name_lst[mlistindex][0]
        try:
            cur.execute("INSERT INTO public.usermovie (email,userid,movieid,rating) VALUES (%s,%s::bigint,%s::bigint,%s::bigint)",(email,uid,movie_id,rating));
            con.commit()
        except:
            print("cannot enter data") 
            
def update_db(detail,a):
    cur.execute("select * from public.user Where email = '" + detail[6] +"'")
    row = cur.fetchone()
    lst=row[5].split(',')
    temp = 1
    for i in lst:
        if i == a:
            temp = 0
            break
    if temp ==1:
        lst.append(a)
        st=','.join(lst)
        cur.execute( " update  public.user set  genre ='" + st + "' Where email = '" + detail[6] +"'")
        con.commit()
        
recommended_movies=None
class Login():
    # def __init__(self):
    userlst=[]
    login_flag=0
    d=None
    def user(request):
        det=Login.d
        if Login.login_flag==0 and det:
            try:
                cur.execute("select * from public.usermovie Where email = '" + det[6]+"'");
                usermoviedata = cur.fetchall()
            except:
                print("error in recommendation")
                #new user
            closest_u=closest(usermoviedata)
            global recommended_movies
            recommended = recommend(closest_u)
            recommended_movies=movie_name(recommended)
            Login.login_flag=int(1)
            ### colaborative model (pass userid and movie id format from code ...) 
        print(recommended_movies)
        if recommended_movies==None:
            return HttpResponseRedirect('/')
        lst = carousel_data()
        t = {'rdata':recommended_movies,
            'posts1': lst[0], 
            'posts2': lst[1], 
            'len': range(lst[2]),
            'len1':range(len(recommended_movies)),
            'ns':range(4),
            'det':det,
            
            }
        print("@@@@@@@@@@@@@@@@@@@@@@",t['len'])
        return render(request, 'user.html',t)
        # return render_template('user.html',rdata=recommended_movies,det=det,posts1=mdata,posts2=temp,len=n,ns=4,len1=len(recommended_movies))
    
    def text_analysis(request):
        det=Login.d
        if request.method == "POST":
            if request.POST.get('genrename') =='':
                return redirect('home')
            else:
                print("input") 
                
                moviename = request.POST.get('moviename')
                genrename = request.POST.get('genrename')
                comment = request.POST.get('comment')
                rating = request.POST.get('rating')
                label = returnlabel(comment)
                update_M_db(moviename, det[6], det[0], rating)
                if label==1:
                    update_db(det,genrename)
                return redirect('home')
        return redirect('home')
    
    def login(request):
        if request.method == "POST":
            email = request.POST.get('email')
            passwo = request.POST.get('password')
            if email=='':
                return render(request, 'login.html')
            print("email ",email,"pass ",passwo)
            try:
                cur.execute("select email from public.user Where email = '" + email +"'")
                db_userdata = cur.fetchone()
                userdata=""
                if db_userdata:
                    userdata = db_userdata[0]
                if userdata=='':
                    return render(request, 'login.html')
                cur.execute("select password from public.user Where email = '" + email +"'")
                db_passw = cur.fetchone()
                passw=""
                if db_passw:
                    passw = db_passw[0]
            except psycopg2.Error as e:
                t_message = e
                print(e," dsbsjd")
                return render(request, 'login.html')
                # return render_template("login.html", message = t_message)
            print("hello")
            if email is None:
                # flash("no username","danger")
                print("email")
                return render(request, 'login.html')
            else:
                if passw == passwo:
                    # flash("you are logged in")
                    print(email)
                    Login.userlst.append(email)
                    # login(request, email)
                    # session['user']=email
                    Login.d = get_details(email)
                    print(type(Login.d))
                    Login.login_flag =0
                    return HttpResponseRedirect('/home')
                    # return render_template("user.html")
                    # return redirect(url_for('user'))
                else:
                    # flash("incorrect password","danger")
                    return render(request, 'login.html')
        return render(request, 'login.html')
    
    def logout_view(request):
        Login.userlst.remove(Login.d[6])
        # logout(request)
        return redirect('index')
    
    def changeuser(request):
        return render(request, 'changeuser.html')

    def change_userdet(request):
        if request.method == "POST":
            if request.POST.get('password') =='':
                return redirect('home')
            else: 
                det=Login.d
                firstname = request.POST.get('firstname')
                if firstname=='':
                    firstname=det[1]
                lastname = request.POST.get('lastname')
                if lastname=='':
                    lastname=det[2]
                phone = request.POST.get('phone')
                if phone=='':
                    phone=det[3]
                Gender = request.POST.get('Gender')
                if Gender=='':
                    Gender=det[4]
                Genre = request.POST.get('genre')
                if Genre=='':
                    Genre=det[5]
                passw = request.POST.get('password')

                if passw=='':
                    passw=det[7]
                else:
                    passw=str(passw)
                print("\nuser ",det,firstname,lastname,phone,Gender,Genre)
                cur.execute( " update  public.user set firstname = '" + firstname + "', lastname = '" + lastname + "', phone = " + phone + ", gender = '" + Gender + "', genre ='" +Genre + "', password = '" + passw + "' Where email = '" + det[6] +"'")
                con.commit()
                return redirect('home')
        return redirect('home')

def register_success(request):
    return render(request, 'index.html')

def signup(request):
    print('success in ifbef')
    if request.method == "POST":
        # Get the post parameters
        print('success in ifbef')
        form = UserRegisterForm(request.POST)
        print('success in if', form.is_valid(), request.POST.get('passw'))

        print(form.errors)
        if form.is_valid():
            # Create the user
            form.save()
            print('success form saved')
            return HttpResponseRedirect('/register_success')
        else:
            form = UserRegisterForm()
            return render(request, 'signup.html')
    else:
        form = UserRegisterForm()
        # return HttpResponse("404 - Not found")
        return render(request, 'signup.html')

def forgotp(request):
    return render(request, 'forgot.html')

def movielink(request):
    return render(request, 'movielink.html')

def send_email(request):
    if request.method == "POST":
        if request.POST.get('email') =='':
            return redirect('index')
        else:
            print("input") 
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            cur.execute("INSERT INTO public.usermessage (email,phone,subject,message) VALUES (%s,%s::bigint,%s,%s)",(email,phone,subject,message));
            con.commit()
            return redirect('index')
    return redirect('index')

def send_email1(request):
    if request.method == "POST":
        if request.POST.get('email') =='':
            return redirect('home')
        else:
            print("input") 
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            cur.execute("INSERT INTO public.usermessage (email,phone,subject,message) VALUES (%s,%s::bigint,%s,%s)",(email,phone,subject,message));
            con.commit()
            return redirect('home')
    return redirect('home')




    # def login(request):
    #     if request.method == "POST":
    #         email = request.form.get('email')
    #         passwo = request.form.get('password')
    #         if email=='':
    #             return render(request, 'login.html')
    #         try:
    #             cur.execute("select email from public.user Where email = '" + email +"'")
    #             db_userdata = cur.fetchone()
    #             userdata=""
    #             if db_userdata:
    #                 userdata = db_userdata[0]
    #             if userdata=='':
    #                 return render(request, 'login.html')

    #             cur.execute("select passw from public.user Where email = '" + email +"'")
    #             db_passw = cur.fetchone()
    #             passw=""
    #             if db_passw:
    #                 passw = db_passw[0]
            
    #         except psycopg2.Error as e:
    #             t_message = e
    #             return render(request, 'login.html')
    #         if email is None:
    #             # flash("no username","danger")
    #             return render(request, 'login.html')
    #         else:
    #             if sha256_crypt.verify(passwo,passw):
    #                 flash("you are logged in")
    #                 global login_flag
    #                 login_flag=int(0)
    #                 session['user']=email
    #                 d = get_details(email)

    #                 return redirect(url_for('user'))
    #             else:
    #                 flash("incorrect password","danger")
    #                 return render_template("login.html")

    #     return render_template('login.html')

# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         print("*****************",form.errors,form.is_valid())
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/register_success')  
#     else:
#         form = CustomUserCreationForm()
#     args = {}
#     # args.update(csrf(request))
#     args['form'] = form
#     return render(request, 'signup.html', args)

# @login_required
# def CreatePoll(request):
#     if request.method == 'POST':
#         form = PollForm(request.POST)
#         form.instance.creator = request.user
#         if form.is_valid():

#             bg_no = random.randint(1,15)
#             form.instance.image_bg =  "back"+str(bg_no)+".jpg"
#             form.save()
#             return redirect('poll-home')
#     else:
#         form = PollForm
#     return render(request, 'poll/createpoll.html', {'form': form})

# @login_required
# def DetailedPoll(request, pk):
#     if request.method == 'POST':
#         poll_connected = Poll.objects.filter(id=pk)[0]
#         if poll_connected.votedBy.filter(id=request.user.id).exists():
#             print("You have voted once")
#             messages.error(request, "You have already voted once")
#             return redirect('detail-poll', pk=pk)
#         else:
#             if "option1" in request.POST:
#                 print("Option 1")
#                 o1 = Poll.objects.filter(id=pk)[0].option1_count
#                 o1=o1+1
#                 Poll.objects.filter(id=pk).update(option1_count = o1)

#             else:
#                 print("option 2")
#                 o2 = Poll.objects.filter(id=pk)[0].option2_count
#                 o2=o2+1
#                 Poll.objects.filter(id=pk).update(option2_count = o2)
#             messages.error(request, "Thank you for voting. Your opinion matter!")
#             poll_connected.votedBy.add(request.user)
#             p_o1 = (Poll.objects.filter(id=pk)[0].option1_count/(Poll.objects.filter(id=pk)[0].option2_count+Poll.objects.filter(id=pk)[0].option1_count))*100
#             p_o2 = (Poll.objects.filter(id=pk)[0].option2_count/(Poll.objects.filter(id=pk)[0].option2_count+Poll.objects.filter(id=pk)[0].option1_count))*100
#             Poll.objects.filter(id=pk).update(percentage_o1 = p_o1)
#             Poll.objects.filter(id=pk).update(percentage_o2 = p_o2)
#             return redirect('detail-poll', pk=pk)

#     else:
#         poll= Poll.objects.filter(id= pk)
#         return render(request, 'poll/polldetail.html',{"poll":poll[0]})


# def home(request):
#     context ={
#     "polls": Poll.objects.all()
#     }
#     return render(request,'poll/home.html', context)


# def votedBy(request, pk):
#     poll = get_object_or_404(Poll, id=request.POST.get("poll_id"))
#     if poll.votedBy.filter

        # form=UserRegisterForm(request.POST)
        # form.first_name=request.POST.get('firstname')
        # form.last_name=request.POST.get('lastname')
        # form.phone=request.POST.get('phone')
        # form.gender=request.POST.get('gender')
        # form.genre=request.POST.get('genre')
        # form.password=request.POST.get('password')
        # form.email=request.POST.get('email')
