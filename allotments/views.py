from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from allotments.models import *
from user.models import User
from django.urls import reverse
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
            if Allotment.objects.filter(branch=Branch.objects.get(branch_code=branch),batch=Batch.objects.get(id=batch),subject=Subject.objects.get(id=subject),faculty=User.objects.get(id=faculty)).first():
                messages.error(request, "Allotment Already Exists")
            else:
                Allotment.objects.create(branch=Branch.objects.get(branch_code=branch),batch=Batch.objects.get(id=batch),faculty=User.objects.get(id=faculty),subject=Subject.objects.get(id=subject))
                messages.success(request, "Allotment Saved")
            # branch=Branch.objects.get(branch_code=branch).branch_code
            return render(request,'NewAllotment.html',{'subjects':Subject.objects.all(),'faculties':User.objects.filter(is_faculty=True),'branches':Branch.objects.all(),'batches':Batch.objects.all(),'branch':branch,'batch':batch,'year':year,'semester':semester,'faculty_branch':faculty_branch,'programs':Program.objects.all(),'program':program})
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong")
        
def display_allotements(request):
    if request.method=='GET':
        try:
            branches = Branch.objects.all()
            faculties = User.objects.filter(is_faculty=True)
            # batch = Batch.objects.order_by("batch_name")
            # starting_year = batch[0].batch_name.split("-")[0]
            # ending_year = batch[len(batch)-1].batch_name.split("-")[1]
            # academic_years = []
            # for i in range(int(starting_year),int(ending_year)+1):
            #     academic_years.append(str(i)+"-"+str(i+1))
            programs = Program.objects.all()
            academic_years = AcademicYear.objects.order_by("year").values_list('year',flat=True).distinct()
            return render(request,'AllotmentFilter.html',{'branches':branches,'faculties':faculties,'academic_years':academic_years,'programs':programs})
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong")
    if request.method == 'POST':
        try:
            if request.POST.get('submit')=='faculty':
                filter_kwargs = {}
                branch = request.POST.get('branch')
                faculty = request.POST.get('faculty')
                academic_year = request.POST.get('academic_year')
                semester = request.POST.get('semester')
                print(branch,faculty,academic_year,semester)
                # starting_year = academic_year.split("-")[0]
                # for i in range(4):
                #     year=str(int(starting_year)-i)
                #     batch=Batch.objects.get(batch_name=year+"-"+str(int(year)+4))
                if branch:
                    filter_kwargs['branch__branch_code'] = branch
                if semester:
                    filter_kwargs['subject__semester'] = semester
                if academic_year:
                    batches = AcademicYear.objects.filter(year=academic_year).values_list('batch',flat=True)
                    print(batches)
                    filter_kwargs['batch__id__in'] = batches
                # if request.POST.get('branch'):
                #     branch = Branch.objects.get(branch_code=request.POST.get('branch'))
                #     filter_kwargs['branch__branch_code'] = request.POST.get('branch')
                if request.POST.get('faculty'):
                    faculty = User.objects.get(id=request.POST.get('faculty'))
                    if not branch:
                        branch = Branch.objects.get(branch_code=faculty.faculty_branch.branch_code)
                    else:
                        branch = Branch.objects.get(branch_code=branch)
                    filter_kwargs['faculty__id'] = request.POST.get('faculty')
                    allotments=Allotment.objects.filter(**filter_kwargs).select_related('subject','batch','branch','faculty')
                    return render(request,'Allotments.html',{'allotments':allotments,'branch':branch,'faculty':faculty,'type':'faculty'})
                
                else:
                    messages.error(request, "Please select a faculty")
                    return HttpResponseRedirect(reverse('allotments:display_allotements'))
            elif request.POST.get('submit')=='class':
                filter_kwargs = {}
                program = request.POST.get('program')
                academic_year = request.POST.get('academic_year')
                year=request.POST.get('year')
                branch = request.POST.get('branch')
                semester = request.POST.get('semester')
                print(branch,academic_year,semester)
                # starting_year = academic_year.split("-")[0]
                # for i in range(4):
                #     year=str(int(starting_year)-i)
                #     batch=Batch.objects.get(batch_name=year+"-"+str(int(year)+4))
                if program:
                    filter_kwargs['batch__program__id'] = program
                if branch:
                    filter_kwargs['branch__branch_code'] = branch
                if year:
                    filter_kwargs['subject__year'] = year
                if semester:
                    filter_kwargs['subject__semester'] = semester
                if academic_year:
                    batches = AcademicYear.objects.filter(year=academic_year).values_list('batch',flat=True)
                    print(batches)
                    filter_kwargs['batch__id__in'] = batches
                # if request.POST.get('branch'):
                #     branch = Branch.objects.get(branch_code=request.POST.get('branch'))
                #     filter_kwargs['branch__branch_code'] = request.POST.get('branch')
                allotments=Allotment.objects.filter(**filter_kwargs).select_related('subject','batch','branch','faculty')
                return render(request,'Allotments.html',{'allotments':allotments,'branch':branch,'type':'class'})
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong")
