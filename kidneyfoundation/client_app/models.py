from django.db import models
from datetime import datetime, date

# Create your models here.
class Role(models.Model):
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'role'

class Condition(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return (f'{self.name}')
    
    class Meta:
        db_table = 'condition'

class Comorbidity(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return (f'{self.name}')
    
    class Meta:
        db_table = 'comorbidity'

class SiteUser(models.Model):
    username = models.CharField(max_length=150, default='')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=30)

    def __str__(self):
        return (f'{self.last_name}, {self.first_name}')

    class Meta:
        db_table = 'SiteUser'

class Sponsor(models.Model):
    sponsor = models.OneToOneField(SiteUser, primary_key=True, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)

    def __str__(self):
        return (f'{SiteUser.objects.get(id=self.sponsor).last_name}, {SiteUser.objects.get(id=self.sponsor).first_name}')

    class Meta:
        db_table = 'sponsor'

class Patient(models.Model):
    patient = models.OneToOneField(SiteUser, primary_key=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, default='')
    age = models.FloatField()
    height = models.IntegerField()
    weight = models.IntegerField()
    sex = models.CharField(max_length=10, default='non-binary')
    diagnosis = models.ForeignKey(Condition, on_delete=models.DO_NOTHING)
    birthday = models.DateField()
    sponsor = models.ManyToManyField(Sponsor, blank=True)
    comorbidity = models.ManyToManyField(Comorbidity, blank=True)

    def __str__(self):
        return (f'{SiteUser.objects.get(id=self.patient).last_name}, {SiteUser.objects.get(id=self.patient).first_name}')

    class Meta:
        db_table = 'patient'

class Nutrient(models.Model):
    name = models.CharField(max_length=30)
    frequency = models.CharField(max_length=30)
    gender_specific = models.CharField(max_length=10, blank=True)
    healthy_target_min = models.FloatField(blank=True)
    healthy_target_max = models.FloatField(blank=True)
    patient_target_min = models.FloatField(blank=True)
    patient_target_max = models.FloatField(blank=True)
    dialysis_target_min = models.FloatField(blank=True)
    dialysis_target_max = models.FloatField(blank=True)
    units = models.CharField(max_length=10)
    actively_track = models.BooleanField(default=True)

    def __str__(self):
        return (f'{self.name}')

    class Meta:
        db_table = 'nutrient'
        constraints = [
            models.UniqueConstraint(fields=['name', 'frequency', 'gender_specific'], name='nutrition_frequency_PK')
        ]

class Food_Units(models.Model):
    name = models.CharField(max_length=30)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return (f'{self.name}')
    
    class Meta:
        db_table = 'food_units'

class Drink_Units(models.Model):
    name = models.CharField(max_length=30)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return (f'{self.name}')
    
    class Meta:
        db_table = 'drink_units'

class Food_Type(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return (f'{self.name}')
    
    class Meta:
        db_table = 'food_type'

class Fluid_Type(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return (f'{self.name}')
    
    class Meta:
        db_table = 'fluid_type'

class Food_Item(models.Model):
    food_type = models.ForeignKey(Food_Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=500)
    units = models.ForeignKey(Food_Units, on_delete=models.DO_NOTHING)

    water = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    potassium = models.FloatField(default=0)
    phosphorus = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'food_item'

class Drink_Item(models.Model):
    fluid_type = models.ForeignKey(Fluid_Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='Water')
    description = models.CharField(max_length=500)
    units = models.ForeignKey(Drink_Units, on_delete=models.DO_NOTHING)

    water = models.FloatField()
    sodium = models.FloatField(blank=True)
    protein = models.FloatField(blank=True)
    potassium = models.FloatField(blank=True)
    phosphorus = models.FloatField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'drink_item'

class Report_Food(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, default='')
    date = models.DateField()
    eating_time = models.CharField(max_length=10, default='Snack')
    units_count = models.FloatField()
    food = models.ForeignKey(Food_Item, on_delete=models.DO_NOTHING)
    water = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    potassium = models.FloatField(default=0)
    phosphorus = models.FloatField(default=0)
    protein = models.FloatField(default=0)

    class Meta:
        db_table = 'report_food'

class Report_Drink(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, default='')
    date = models.DateField()
    eating_time = models.CharField(max_length=10, default='Snack')
    units_count = models.FloatField()
    drink = models.ForeignKey(Drink_Item, on_delete=models.DO_NOTHING)
    water = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    potassium = models.FloatField(default=0)
    phosphorus = models.FloatField(default=0)

    class Meta:
        db_table = 'report_drink'

class Report_Serum(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, default='')
    date = models.DateField()
    
    potassium = models.FloatField()
    phosphorus = models.FloatField()
    sodium = models.FloatField()
    creatinine = models.FloatField()
    abumin = models.FloatField()
    blood_sugar = models.FloatField()

    def __str__(self):
        return (f'{self.id}')

    class Meta:
        db_table = 'report_serum'