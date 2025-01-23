
from django.shortcuts import render,redirect
#from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .models import reviewer,team_admin,Marks,PID


def add_to_session(request,key,value):
    request.session[key] = value
    print("Added to session")

def get_from_session(request,key):
    return request.session.get(key,"Not Found")


# Create your views here.
@csrf_exempt
def login_view(request):
    
    if request.method == 'POST':
        user_category = request.POST.get('user-category')
        #print(user_category)
        username = request.POST.get('mail')
        password = request.POST.get('password')
        #print(username,password)
        #user = authenticate(request,username = username,password=password)
        #print(user)
        if user_category=='Reviewer':
            users = reviewer.objects.values('email','password')
        else:
            users = team_admin.objects.values('email','password')
        #print(users)
        if users:
            loggedIn = False
            for each_users in users:
                if each_users['email'] == username and each_users['password']==password:
                    loggedIn = True
                    add_to_session(request,key="UserCategory",value=user_category)
                    add_to_session(request,key="LoggedIn",value=True)
                    if user_category=='Reviewer':
                        return redirect('/reviewer_page/')
                    else:
                        return redirect('/admin_page')
            if not loggedIn:
                return render(request,'login.html',{'error_message': 'Email or Password is Wrong!'})

        """if user is not None:
            login(request, user)
            print("Logged in")
        else :
            return render(request,'login.html',{'error_message': 'Invalid credentials'})
        """

    """if "LoggedIn" in request.session and request.session["LoggedIn"] == False:
        return render(request,'login.html',{'error_message': 'Login Again!'})"""
    return render(request,'login.html')

@csrf_exempt
def admin_page(request):
    if get_from_session(request,key="LoggedIn") and get_from_session(request,key="UserCategory")=="Team-Admin":
        marks = Marks.objects.all()
        if request.method =="POST":
            if request.POST.get('form-id') == 'search-btn':
                pid = request.POST.get('search-bar')
                if pid =='':
                    marks = Marks.objects.all()
                    return render(request,'admin_page.html',{'marks':marks})
                else:
                    marks = Marks.objects.all().filter(PID = pid)
                    return render(request,'admin_page.html',{'marks':marks})
            if request.POST.get('form-id') == "logout-btn":
                request.session.flush()
                add_to_session(request,key="LoggedIn", value=False)
                return redirect('login')
            
            
            

            
        else:
            return render(request,'admin_page.html',{'marks':marks})
    else:
        return redirect('login')


@csrf_exempt
def reviewer_page(request):
    if 'LoggedIn' in request.session and request.session['LoggedIn']:
        if request.method == 'POST':
            if request.POST.get('form-id') == "mark-form":
                R1 = float(request.POST.get('R1'))
                R2 = float(request.POST.get('R2'))
                R3 = float(request.POST.get('R3'))
                R4 = float(request.POST.get('R4'))
                R5 = float(request.POST.get('R5'))
                R6 = float(request.POST.get('R6'))
                R7 = float(request.POST.get('R7'))
                R8 = float(request.POST.get('R8'))
                R9 = float(request.POST.get('R9'))
                R10 =float( request.POST.get('R10'))
                reviewer_mark_total = sum([R1,R2,R3,R4,R5,R6,R7,R8,R9,R10])
                print("Reviewer mark: ",reviewer_mark_total)
        
                T1 = float(request.POST.get('T1'))
                T2 = float(request.POST.get('T2'))
                T3 = float(request.POST.get('T3'))
                T4 = float(request.POST.get('T4'))
                T5 = float(request.POST.get('T5'))
                T6 = float(request.POST.get('T6'))
                team_communication_total = sum([T1,T2,T3,T4,T5,T6])
                print("Team comm: ",team_communication_total)

                current_student_in_assessment = Marks.objects.get(Student_RollNo = get_from_session(request,"current_student_in_review") )
                current_student_in_assessment.Reviewer_Mark = reviewer_mark_total * 0.6
                current_student_in_assessment.Team_communication_mark = team_communication_total * 0.1
                current_student_in_assessment.save()

                total_mark = (current_student_in_assessment.Initial_submission 
                + current_student_in_assessment.Final_submission
                + current_student_in_assessment.Plagiarism
                + current_student_in_assessment.Reviewer_Mark
                + current_student_in_assessment.Team_communication_mark
                + current_student_in_assessment.Worklog )

                current_student_in_assessment.Total = total_mark 

                current_student_in_assessment.save()
                student_details = Marks.objects.filter(Student_RollNo = get_from_session(request,"current_student_in_review")).values()
                add_to_session(request,key="details_of_current_student",value=list(student_details)[0])
                return render(request,'reviewer_page.html',{'pids':get_from_session(request,'pids'),'roll_nos':get_from_session(request,key="roll_nos_in_selected_pid"),'student_details':get_from_session(request,"details_of_current_student")})



            if request.POST.get('form-id') == "pid-form":
                pid_from_form = request.POST.get('pids')
                roll_no_with_pid = Marks.objects.filter(PID=pid_from_form).values('Student_RollNo')
                temp_roll_no = set()
                for roll_no in roll_no_with_pid:
                    temp_roll_no.add(list(roll_no.values())[0])
                add_to_session(request,key="roll_nos_in_selected_pid",value=list(temp_roll_no))
                return render(request,'reviewer_page.html',{'pids':get_from_session(request,'pids'),'roll_nos':get_from_session(request,key="roll_nos_in_selected_pid")})
                
            if request.POST.get('form-id') == "student-details-form":
                stud_roll_no = request.POST.get('stud-under-pid')
                print(stud_roll_no)
                student_details = Marks.objects.filter(Student_RollNo = stud_roll_no).values()
                print(student_details)
                add_to_session(request,key="current_student_in_review",value=stud_roll_no)
                add_to_session(request,key="details_of_current_student",value=list(student_details)[0])
                return render(request,'reviewer_page.html',{'pids':get_from_session(request,'pids'),'roll_nos':get_from_session(request,key="roll_nos_in_selected_pid"),'student_details':get_from_session(request,key="details_of_current_student")})
            if request.POST.get('form-id') == "logout-btn":
                request.session.flush()
                add_to_session(request,key="LoggedIn",value=False)
                return redirect('login')


                
        pids = PID.objects.values('PID')
        print(pids)
        temp = set()
        for pid in pids:
            temp.add(list(pid.values())[0])
        add_to_session(request,"pids",list(temp))
        
        return render(request,'reviewer_page.html',{'pids':list(temp)})
    else:
        return redirect('login')



@csrf_exempt
def helloworld(request):
    return render(request,'index.html')

@csrf_exempt
def create_review(request):
    if request.session["LoggedIn"]:
        if request.method == 'POST':
            pid = request.POST.get('pid-input')
            pid_details = PID.objects.all().filter(PID=pid)
            return render(request,'create_review.html',{'pid':pid,'pid_details':pid_details})
            print(pid)
        if request.method == 'POST':
            pid = request.POST.get('pid-input')
            stud_name = request.POST.get('student-selector')
            print(stud_name)
            pid_details = PID.objects.all().filter(PID=pid,Student_Name=stud_name)
            return render(request,'create_review.html',{'pid-details':pid_details})
        


        return render(request,'create_review.html')
    else:
        return redirect('login')