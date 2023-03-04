from django.db import models
from allotment_system.settings import AUTH_USER_MODEL
# Create your models here.
class Branch(models.Model):
    branch_code=models.CharField(max_length=50,primary_key=True)
    branch_name=models.CharField(max_length=50)
    hod=models.ForeignKey(AUTH_USER_MODEL,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='branch')
    def __str__(self):
        return self.branch_name
    class Meta:
        verbose_name_plural='Branches'


class Program(models.Model):
    program_name=models.CharField(max_length=50)
    def __str__(self):
        return self.program_name

class Batch(models.Model):
    program=models.ForeignKey(Program,on_delete=models.DO_NOTHING,related_name='batches',null=True,blank=True)
    batch_name=models.CharField(max_length=50)
    def __str__(self):
        return self.batch_name
    class Meta:
        verbose_name_plural='Batches'
class Student(models.Model):
    name=models.CharField(max_length=50)
    rollno=models.CharField(max_length=50,primary_key=True)
    branch=models.ForeignKey(Branch,on_delete=models.DO_NOTHING,related_name='students')
    batch=models.ForeignKey(Batch,on_delete=models.DO_NOTHING,related_name='students')
    program=models.ForeignKey(Program,on_delete=models.DO_NOTHING,related_name='students')
    minor_branch=models.ForeignKey(Branch,on_delete=models.DO_NOTHING,related_name='minor_branch',null=True,blank=True)
    def __str__(self):
        return self.rollno+" ( "+self.name+" )"

class Subject_type(models.Model):
    type=models.CharField(max_length=50)
    max_marks=models.IntegerField()
    def __str__(self):
        return self.type

class Regulation(models.Model):
    regulation_name=models.CharField(max_length=50,primary_key=True)
    def __str__(self):
        return self.regulation_name

class Subject(models.Model):
    subject_name=models.CharField(max_length=150)
    subject_code=models.CharField(max_length=50)
    subject_type=models.ForeignKey(Subject_type,on_delete=models.DO_NOTHING,related_name='subjects')
    regulation=models.ForeignKey(Regulation,on_delete=models.DO_NOTHING,related_name='subjects')
    program=models.ForeignKey(Program,on_delete=models.DO_NOTHING,related_name='subjects')
    branch=models.ForeignKey(Branch,on_delete=models.DO_NOTHING,related_name='subjects')
    year=models.IntegerField()
    semester=models.IntegerField()
    credits=models.DecimalField(max_digits=3,decimal_places=1)
    def __str__(self):
        return self.subject_name+" ( "+self.branch.branch_name+" )"
    class Meta:
        unique_together = ('subject_code', 'branch')

class Allotment(models.Model):
    branch=models.ForeignKey(Branch,on_delete=models.DO_NOTHING,related_name='allotments')
    subject=models.ForeignKey(Subject,on_delete=models.DO_NOTHING,related_name='allotments')
    faculty=models.ForeignKey(AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name='allotments')
    batch=models.ForeignKey(Batch,on_delete=models.DO_NOTHING,related_name='allotments')
    def __str__(self):
        return self.faculty.first_name+" "+self.faculty.last_name+" ( "+self.subject.subject_name+" )"
    class Meta:
        unique_together = ('subject', 'faculty','batch')

class AcademicYear(models.Model):
    year=models.CharField(max_length=50)
    batch=models.ForeignKey(Batch,on_delete=models.DO_NOTHING,related_name='academic_years')
    
    def __str__(self):
        return self.year