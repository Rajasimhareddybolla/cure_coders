from django.db import models




class MyUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
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
    location = models.TextField()
    specialists = models.ManyToManyField(Specialist)
    stats = models.TextField()
    description = models.TextField()


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
