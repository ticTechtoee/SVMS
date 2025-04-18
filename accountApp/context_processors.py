from .models import Employee

def employee_company_context(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            return {'employee_company': employee.company}
        except Employee.DoesNotExist:
            return {}  # User is not an employee
    return {}
