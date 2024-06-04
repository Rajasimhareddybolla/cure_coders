from django.contrib import admin
from .models import MyUser, Medical_stat, Specialist, Hospital, Review, Appointment, Symptom

admin.site.register(MyUser)
admin.site.register(Medical_stat)
admin.site.register(Specialist)
admin.site.register(Hospital)
admin.site.register(Review)
admin.site.register(Appointment)
admin.site.register(Symptom)