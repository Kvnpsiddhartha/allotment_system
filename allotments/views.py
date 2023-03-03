from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from allotments.models import Subject,Branch,Batch,Allotment,Regulation,Program
from user.models import User
# Create your views here.
def new_allotment(request):
    if request.method=='GET':
        try:
            return render(request,'NewAllotment.html',{'subjects':Subject.objects.all(),'faculties':User.objects.filter(is_faculty=True),'branches':Branch.objects.all(),'batches':Batch.objects.all(),'programs':Program.objects.all(),'regulations':Regulation.objects.all()})
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong")
    elif request.method=='POST':
        try:
            program=request.POST.get('program')
            branch = request.POST.get('branch')
            batch = request.POST.get('batch')
            faculty = request.POST.get('faculty')
            subject = request.POST.get('subject')
            year = request.POST.get('year')
            semester = request.POST.get('semester')
            faculty_branch=request.POST.get('faculty_branch')
            if Allotment.objects.filter(branch=Branch.objects.get(branch_code=branch),batch=Batch.objects.get(id=batch),subject=Subject.objects.get(id=subject)).first():
                messages.error(request, "Allotment Already Exists")
            else:
                Allotment.objects.create(branch=Branch.objects.get(branch_code=branch),batch=Batch.objects.get(id=batch),faculty=User.objects.get(id=faculty),subject=Subject.objects.get(id=subject))
                messages.success(request, "Allotment Saved")
            branch=Branch.objects.get(branch_code=branch).branch_name
            return render(request,'NewAllotment.html',{'subjects':Subject.objects.all(),'faculties':User.objects.filter(is_faculty=True),'branches':Branch.objects.all(),'batches':Batch.objects.all(),'branch':branch,'batch':batch,'year':year,'semester':semester,'faculty_branch':faculty_branch})
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong")
        
def display_allotements(request):
    if request.method=='GET':
        try:
            programs = Program.objects.all()
            branches = Branch.objects.all()
            batches  = Batch.objects.all()
            return render(request,'AllotmentFilter.html',{'branches':branches,'batches':batches,'programs':programs})
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong")
    if request.method == 'POST':
        try:
            programs= request.POST.get('program')
            branch = request.POST.get('branch')
            batch = request.POST.get('batch')
            year = request.POST.get('year')
            semester = request.POST.get('semester')
            branch=Branch.objects.get(branch_code=branch)
            batch=Batch.objects.get(id=batch) 
            program=Program.objects.get(id=programs)
            allsubjects=Subject.objects.filter(branch=branch,year=year,semester=semester,program=program)  
            allotments=Allotment.objects.filter(branch=branch,batch=batch,subject__year=year,subject__semester=semester).select_related('subject','faculty')
            return render(request,'Allotments.html',{'allotments':allotments,'branch':branch,'batch':batch,'year':year,'semester':semester,'subjects':allsubjects})
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong")
