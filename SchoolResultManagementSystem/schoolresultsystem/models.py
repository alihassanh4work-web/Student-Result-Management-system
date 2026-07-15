from ast import mod

from django.db import models

class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_numeric = models.IntegerField()
    section = models.CharField(max_length=50)
    Creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.class_name} - {self.section}"

class Subject(models.Model):
    Subject_name = models.CharField(max_length=50)
    Subject_code = models.CharField(max_length=20)
    Creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.Subject_name} - {self.Subject_code }"

class Student(models.Model):
    name = models.CharField(max_length=50)
    roll_id = models.CharField(max_length=30)
    Email=models.EmailField(max_length=50)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')))
    Date_of_birth = models.DateField()
    Student_class = models.ForeignKey(Class, on_delete=models.SET_NULL,null=True)
    Reg_date = models.DateField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    Status = models.CharField(default=1)
    def __str__(self):
        return self.name
    
    
class Subjectcombination(models.Model):
        Student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
        Subjects = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
        Creation_date = models.DateTimeField(auto_now_add=True)       
        updation_date = models.DateTimeField(auto_now=True)
        Status = models.CharField(default=1)
        
        def __str__(self):
            return f"{self.Student_class} - {self.Subjects}"


class Result(models.Model):
        Student = models.ForeignKey(Student, on_delete=models.CASCADE )
        Student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
        Subjects = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
        Marks = models.IntegerField()
        posting_date = models.DateTimeField(auto_now_add=True)       
        updation_date = models.DateTimeField(auto_now=True)
        def __str__(self):
            return f"{self.Student} - {self.Subjects}- {self.Marks}"
        
class Notice(models.Model):
        title = models.CharField(max_length=100)
        details = models.TextField()
        posting_date = models.DateTimeField(auto_now_add=True)       
        updation_date = models.DateTimeField(auto_now=True)
        def __str__(self):
            return f"{self.title}"        
    

    
   
   
   
    