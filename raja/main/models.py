from django.db import models




class MyUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    age = models.IntegerField(default=18)
    email = models.EmailField(default="raja@gmail.com")
    image = models.TextField(default="https://www.bing.com/ck/a?!&&p=da0861fa735626ffJmltdHM9MTcxNzM3MjgwMCZpZ3VpZD0xMGVmODQyZC0wNDI0LTZhMmQtMjQwMC05MDU5MDVmNjZiYzMmaW5zaWQ9NTY3Mg&ptn=3&ver=2&hsh=3&fclid=10ef842d-0424-6a2d-2400-905905f66bc3&u=a1L2ltYWdlcy9zZWFyY2g_cT1pbWFnZSZGT1JNPUlRRlJCQSZpZD1GQjQ2NTBGODNCNDhBOEIyNjBGMUVDMUFBODlEQThGRTNFNzFFM0Q0&ntb=1")
    def __str__(self) -> str:
        return self.username

class Medical_stat(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='medical_stats')
    age = models.PositiveIntegerField()
    blood_pressure = models.CharField(max_length=100)
    diabetes = models.BooleanField(default=False)
    prev_stroke = models.DateField(null=True, blank=True)
    cholesterol_level = models.PositiveIntegerField()
    family_ethnicity = models.TextField()


class Specialist(models.Model):
    class Specialization(models.TextChoices):
        CARDIOLOGIST = 'CR', 'Cardiologist'
        DERMATOLOGIST = 'DR', 'Dermatologist'
        NEUROLOGIST = 'NR', 'Neurologist'
        
        # Add more specializations as needed

    name = models.CharField(max_length=200)
    specialized = models.CharField(
        max_length=2,
        choices=Specialization.choices,
        default=Specialization.CARDIOLOGIST,
    )
    description = models.TextField()
    education = models.TextField()
class Hospital(models.Model):
    name = models.CharField(max_length=255)
    url = models.TextField()
    location = models.TextField(null=True)
    specialists = models.ManyToManyField(Specialist)
    stats = models.TextField(null=True)
    description = models.TextField()
    password = models.CharField(max_length= 64 , default="raja")
    num_beds = models.PositiveIntegerField(default=0)
    schedule = models.TextField(default= "22")
    total_patients = models.PositiveIntegerField(default=0)
    total_doctors = models.PositiveIntegerField(default=0)
class Appointment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="appointments")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="appointments")
    datetime = models.DateTimeField()
    comments = models.TextField()
    

class Symptom(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="symptoms")
    symptoms = models.TextField()
    date = models.DateField()
    name = models.CharField(max_length=255)
    url = models.TextField()
    location = models.TextField()
    specialists = models.ManyToManyField(Specialist)
    stats = models.TextField()
    description = models.TextField()

class Review(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="reviews")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name= "reviews")
    STARS = [(i, i) for i in range(1, 6)]
    stars = models.IntegerField(choices=STARS)
    comments = models.TextField()
class comments(models.Model):
    user = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField()
    subject = models.CharField(max_length=444)
    resolved = models.BooleanField(default=False)