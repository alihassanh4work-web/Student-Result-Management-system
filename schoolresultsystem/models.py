from django.db import models

class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_numeric = models.IntegerField()
    section = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.class_name} - {self.section}"

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=20)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject_name} - {self.subject_code }"

class Student(models.Model):
    Choices = (('Male', 'Male'), ('Female', 'Female'))
    name = models.CharField(max_length=50)
    roll_id = models.CharField(max_length=30)
    Email=models.EmailField(max_length=50)
    gender = models.CharField(max_length=10, choices=Choices)
    Date_of_birth = models.DateField()
    Student_class = models.ForeignKey(Class, on_delete=models.SET_NULL,null=True) # keep record if student_class is deleted
    Reg_date = models.DateField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    Status = models.CharField(default=1)
    def __str__(self):
        return self.name
    
    
class Subjectcombination(models.Model):
        student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True) # Keep record if student_class is deleted
        subjects = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True) # Keep record if subject is deleted
        creation_date = models.DateTimeField(auto_now_add=True)       
        updation_date = models.DateTimeField(auto_now=True)
        status = models.CharField(default=1)
        
        def __str__(self):
            return f"{self.student_class} - {self.subjects}"


class Result(models.Model):
        student = models.ForeignKey(Student, on_delete=models.CASCADE ) # Delete result if student is deleted
        student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True) # Keep record if student_class is deleted
        subjects = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True) #Keep record if subject is deleted
        marks = models.IntegerField()
        posting_date = models.DateTimeField(auto_now_add=True)       
        updation_date = models.DateTimeField(auto_now=True)
        def __str__(self):
            return f"{self.student} - {self.subjects}- {self.marks}"
        
class Notice(models.Model):
        title = models.CharField(max_length=100)
        details = models.TextField()
        posting_date = models.DateTimeField(auto_now_add=True)       
        updation_date = models.DateTimeField(auto_now=True)
        def __str__(self):
            return f"{self.title}"        
    

    
   
   
   
    