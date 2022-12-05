from django.urls import path

from FamilyExpenseTrackerApp import views

urlpatterns = [

    path('', views.home_fun),

    path('login', views.login_fun, name='login'),   # redirect to login.html
    path('log_data', views.log_data_fun, name='log_data'),

    path('register', views.register_fun, name='register'),  # redirect to register.html
    path('register_data', views.register_data_fun),

    path('gotohome', views.go_to_home, name="gotohome"),  # redirect to family_person.html page

    path('addfamilymembers', views.add_family, name='addfamily'),   # redirect to add_member.html page
    path('addingmember', views.add_family_data, name='addingmember'),   # redirect to add_member.html page

    path('seefamily', views.seefamily, name='seefamily'),    # display family member details
    path('updatemem/<int:id>', views.update_family_mem, name="update"),  # update_family.html
    path('delet/<int:id>', views.del_family_mem, name="delete"),


    path('addexpense', views.add_expense_fun, name='addexpense'),
    path('add_expense_data', views.add_expense_data_fun, name='add_expense_data'),
    path('viewexpense', views.see_expense_fun, name='viewexpense'),
    path('updateexpense/<int:id>', views.update_expense_fun, name='updateexpense'),
    path('deletExp/<int:id>', views.delete_Exp_fun, name="deleteExp"),

    path('see_monthly_record', views.see_monthly_record_fun, name='see_monthly_record'),
    path('get_monthly_records', views.get_monthly_record_fun),

    path('see_yearly_record', views.see_yearly_record_fun, name='see_yearly_record'),
    path('get_yearly_records', views.get_yearly_record_fun),

    path('total_expense', views.total_expense_fun, name='total_expense'),
    path('get_total_expense', views.get_total_expense_fun, name='get_total_expense'),

    path('logout', views.logout_fun, name='logout'),

]