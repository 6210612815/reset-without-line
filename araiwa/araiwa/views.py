from django.shortcuts import render, redirect
from django.contrib import messages
from database.models import Employee,  EmployeeForm
import requests, json

def index(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        employee_id = request.POST.get('employee_id')
        personal_id = request.POST.get('personal_id')
        if form.is_valid:
            try:
                body = {
                    "UserName": "admin_ss",
                    "Password": "ss123456*"
                }
                getTokenURL = 'https://p701apsi01-la02skc.azurewebsites.net/skcapi/token'
                response_token = requests.post(getTokenURL, json=body).json()
                myToken = response_token["accessToken"]
                getEmpURL = f"https://p701apsi01-la01skc.azurewebsites.net/skcapi/empid/{employee_id}"
                auth = {"Authorization": "Bearer %s" %myToken}
                response = requests.get(getEmpURL, headers=auth).json()
                name_en = response[0]["nameEN"]
                per_id = int(response[0]["personal_Id"])
                title_name = response[0]["titleEN"]

                if (int(per_id) == int(personal_id)):
                    employee = Employee(
                        employee_id = employee_id,
                        name = name_en,
                        title = title_name,
                    )
                    employee.save()
                    return render(request, 'greet.html', {
                        'employee': employee,
                    })
                else:
                    messages.info(request, 'Your Personal ID miss match')
            except KeyError as e:
                messages.info(request, 'No Employee ID in database!')
    else:
        form = EmployeeForm()
    return render(request, 'index.html')

def reset(request, id):
    if request.method == "POST":
        employee = Employee.objects.get(id=id)
        pass_1st = request.POST['pass_1st']
        pass_2nd = request.POST['pass_2nd']
        if pass_1st == pass_2nd:
            loginName = 'itsupport'
            password = 'Kubota123'
            domainName = 'siamkubota.co.th'
            get_auth_token_url = f'http://172.31.83.190:88/RestAPI/APIAuthToken?loginName={loginName}&password={password}&domainName={domainName}'
            response = requests.get(get_auth_token_url).json()
            employee_id = employee.employee_id
            auth_token = response["AuthTicket"]
            new_pwd = pass_1st
            input = {"employeeID": employee_id}
            input_format = json.dumps(input)
            get_reset_pwd_url = f'http://172.31.83.190:88/RestAPI/ResetPwd?AuthToken={auth_token}&PRODUCT_NAME=RESTAPI&domainName={domainName}&pwd={new_pwd}&inputFormat=[{input_format}]'
            result = requests.get(get_reset_pwd_url).json()
            status = result[0]["status"]
            message = result[0]["statusMessage"]
            if status == '1':
                messages.info(request, 'Congrate')
                return render(request, 'reset.html', {
                    'employee': employee,
                    'employee_id': employee_id,
                    'message': message,
                })
            else:
                messages.info(request, message)
                return redirect('reset')
        else:
            messages.info(request, 'Your Password Not Match')
            return redirect('reset')
    return render(request, 'reset.html', {'employee': employee,})
