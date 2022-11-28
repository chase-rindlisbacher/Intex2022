from django.db import models
#hi
# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=30)

    @property
    def __str__(self):
        return (f'{self.last_name}, {self.first_name}')

    class META:
        db_table = 'person'

class Patient(models.Model):
    patient_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    age = models.FloatField()
    height = models.IntegerField()
    weight = models.IntegerField()
    birthday = models.DateField()