from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime

from FamilyExpenseTrackerApp.models import FamilyMembers, Expenses


# Create your views here.

def home_fun(request):
    return render(request, 'index.html')

def login_fun(request):
    return render(request, 'login.html', {'data': ''})

def log_data_fun(request):
    uname = request.POST['txtN']
    request.session['user1'] = request.POST['txtN']
    pswd = request.POST['txtP']
    myuser = authenticate(username=uname, password=pswd)
    if myuser is not None:
        login(request, myuser)
        return render(request, 'family_person.html', {'data': uname})
    else:
        return render(request, 'login.html', {'data': 'failed'})


def register_fun(request):
    return render(request, 'register.html')

def register_data_fun(request):
    uname = request.POST['txtN']
    pswd = request.POST['txtP']
    mail = request.POST['txtM']
    if User.objects.filter(username=uname).exists():
        return render(request, 'register.html', {'user_available': True})
    elif User.objects.filter(email=mail).exists():
        return render(request, 'register.html', {'email_available': True})
    else:
        myuser = User.objects.create_user(username=uname, password=pswd, email=mail)
        myuser.save()
        return render(request, 'login.html', {'data': ''})


def go_to_home(request):
    uname = request.session['user1']
    return render(request, 'family_person.html', {'data': uname})


def add_family(request):
    uname = request.session['user1']
    return render(request, 'addmember.html')

def add_family_data(request):
    income = request.POST['income']
    if income == '':
        context = {
            'null': True
        }
        return render(request, 'addmember.html', context)
    else:
        income = float(income)

    family_mem = FamilyMembers()
    family_mem.firstName = request.POST['firstname']
    family_mem.lastName = request.POST['lastname']
    family_mem.profession = request.POST['profession']
    family_mem.income = income
    family_mem.familyLead = request.user               # request.user is to store particular admin data
    family_mem.save()
    return redirect('addfamily')


def seefamily(request):
    uname = request.session['user1']
    family_member = FamilyMembers.objects.filter(familyLead=request.user)       # request.user is to show particular admin data
    return render(request, 'seefamily.html', {'data': family_member})


def update_family_mem(request, id):
    family_member = FamilyMembers.objects.get(id=id)
    if request.method == 'POST':
        family_member.firstName = request.POST['firstname']
        family_member.lastName = request.POST['lastname']
        family_member.profession = request.POST['profession']
        family_member.income = float(request.POST['income'])
        family_member.save()
        return redirect('seefamily')
    return render(request, 'update_family.html', {'data': family_member})


def del_family_mem(request, id):
    family_member = FamilyMembers.objects.get(id=id)
    family_member.delete()
    return redirect('seefamily')


def add_expense_fun(request):
    uname = request.session['user1']
    family_member = FamilyMembers.objects.filter(familyLead=request.user)   # request.user is to show particular admin data
    return render(request, 'add_expense.html', {'data': family_member})

def add_expense_data_fun(request):
    family_expense = Expenses()
    family_expense.name = FamilyMembers.objects.get(firstName=request.POST['ddlN'])
    family_expense.expense = float(request.POST['txtEXP'])
    family_expense.purpose = request.POST['txtPRPS']
    family_expense.date = request.POST['txtD']
    family_expense.familyLead = request.user               # it is used to store the particular family member data to particular family
    family_expense.save()
    return redirect('addexpense')


def see_expense_fun(request):
    uname = request.session['user1']
    exp = Expenses.objects.filter(familyLead=request.user)
    return render(request, 'see_family_exp.html', {'data': exp})


def update_expense_fun(request, id):
    exp = Expenses.objects.get(id=id)
    if request.method == 'POST':
        exp.name = FamilyMembers.objects.get(firstName=request.POST['txtN'])
        exp.expense = float(request.POST['txtEXP'])
        exp.purpose = request.POST['txtPRPS']
        exp.date = request.POST['txtD']
        exp.save()
        return redirect('viewexpense')
    return render(request, 'update_expense.html', {'data': exp})


def delete_Exp_fun(request, id):
    exp = Expenses.objects.get(id=id)
    exp.delete()
    return redirect('viewexpense')



def see_monthly_record_fun(request):
    uname = request.session['user1']
    years_list = list(range(2002, datetime.now().year+1, 1))
    months_list = list(range(2, datetime.now().month + 1, 1))
    dict1 = {
        'years': years_list,
        'months': months_list,
        'records': "",
        'norecords': "",
        'start_month': 1,
        'start_year': 2001
    }
    return render(request, 'monthly_report.html', dict1)

def get_monthly_record_fun(request):
    month = int(request.POST['month'])
    year = int(request.POST['year'])
    data = Expenses.objects.filter(familyLead=request.user, date__year=year, date__month=month)
    if len(data) == 0:
        no_records = "oops! No records on that particular month and year"
        records = ""
    else:
        records = data
        no_records = ""
    years_list = list(range(2001, datetime.now().year + 1, 1))
    months_list = list(range(1, datetime.now().month + 1, 1))
    dict1 = {
        'years': years_list,
        'months': months_list,
        'records': records,
        'norecords': no_records,
        'start_month': month,
        'start_year': year
    }
    return render(request, 'monthly_report.html', dict1)


def see_yearly_record_fun(request):
    uname = request.session['user1']
    years_list = list(range(2002, datetime.now().year + 1, 1))
    dict1 = {
        'years': years_list,
        'records': "",
        'norecords': "",
        'start_year': 2001
    }
    return render(request, 'yearly_report.html', dict1)


def get_yearly_record_fun(request):
    year = int(request.POST['year'])
    data = Expenses.objects.filter(familyLead=request.user, date__year=year)
    if len(data) == 0:
        no_records = "oops! No records on that particular month and year"
        records = ""
    else:
        records = data
        no_records = ""
    years_list = list(range(2001, datetime.now().year + 1, 1))
    dict1 = {
        'years': years_list,
        'records': records,
        'norecords': no_records,
        'start_year': year
    }
    return render(request, 'yearly_report.html', dict1)


def total_expense_fun(request):
    uname = request.session['user1']
    years_list = list(range(2002, datetime.now().year + 1, 1))
    months_list = list(range(2, datetime.now().month + 1, 1))
    dict1 = {
        'start_month': 1,
        'start_year': 2001,
        'monthly_exp': "",
        'yearly_exp': "",
        'years': years_list,
        'months': months_list
    }
    return render(request, 'total_expense.html', dict1)

def get_total_expense_fun(request):
    year = int(request.POST['year'])
    month = int(request.POST['month'])
    month_data = Expenses.objects.filter(familyLead=request.user, date__year=year, date__month=month)
    month_exp = 0
    for i in month_data:
        month_exp = month_exp + i.expense

    year_data = Expenses.objects.filter(familyLead=request.user, date__year=year)
    year_exp = 0
    for i in year_data:
        year_exp = year_exp + i.expense

    years_list = list(range(2001, datetime.now().year + 1, 1))
    months_list = list(range(1, datetime.now().month + 1, 1))

    dict1 = {
        'start_month': month,
        'start_year': year,
        'monthly_exp': month_exp,
        'yearly_exp': year_exp,
        'years': years_list,
        'months': months_list
    }
    return render(request, 'total_expense.html', dict1)

def logout_fun(request):
    auth.logout(request)
    return redirect('login')