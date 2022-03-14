from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid

# Create your models here.
COLOR_STATUS = (
    ('Open','Open'),
    ('Progress', 'Progress'),
    ('Declined', 'Declined'),
    ('Delivered','Delivered'),
    ('Completed','Completed'),
    ('Dispute','Dispute')
)

categotry = {
    ('Maths','Maths'),
    ('Science','Science'),
    ('Programming','Programming'),
    ('others','others'),
}


class Student(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    photo = models.FileField(null=True, blank=True)
    avtar=models.CharField(max_length=260,blank=True)
    is_tutor= models.BooleanField(default=False)
    def __str__(self):
        return str(self.username) + str(' | ') + str(self.fullname)
    
class Tutor(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Education_status = models.CharField(max_length=250, null=True)
    Drive_link = models.URLField(max_length=300)
    Area_of_Expertise = models.CharField(max_length=250, null=True)
    is_verified=models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    randomly_generated_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    # tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=30, choices=categotry ,default='others')
    urgency= models.CharField(max_length=250, null=True)
    description=models.CharField(max_length=250, null=True)
    upload = models.FileField(upload_to ='static/media/', null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return str(self.category)


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    is_selected = models.BooleanField(default=False)
    description=models.TextField(max_length=500, null=True)
    cost = models.CharField(max_length=50000, null=True)
    day = models.CharField(max_length=250, null=True)
    rating= models.IntegerField(blank=True,default=5)
    status = models.CharField(max_length=30, choices=COLOR_STATUS, default='Open')

    # priority = models.CharField(max_length=1, choices=PRIOTITIES, null=True, default='10')
    # PRIOTITIES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
    # ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'),
    # ('18', '18'), ('19', '19'), ('20', '20'))

    def __str__(self):
        return str(self.tutor.username) + str(' | ') + str(self.project.id) 

class TutorTicket(models.Model):
    question_id = models.CharField(max_length=250, null=True)
    project = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=250, null=True)
    
    def _str_(self):
        return str(self.tutor.username) + str(' | ') + str(self.question_id)
    
class StudentTicket(models.Model):
    question_id = models.CharField(max_length=250, null=True)
    project = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=250, null=True)
    
    def _str_(self):
        return str(self.student.username) + str(' | ') + str(self.question_id)
