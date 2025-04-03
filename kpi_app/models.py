from django.db import models
from django.contrib.auth.models import User

class Division(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class KPI(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.CharField(max_length=20)
    cases_received = models.IntegerField(default=0)  # Default to 0 if missing
    cases_reported = models.IntegerField(default=0)  # Default to 0 if missing
    amount = models.FloatField(null=True, blank=True)  # Allow null for missing amounts
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    @property
    def resolution_rate(self):
        return min((self.cases_reported / self.cases_received) * 100, 100) if self.cases_received > 0 else 0

    def __str__(self):
        return f"{self.division} - {self.unit} - {self.year}-{self.month}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('director_general', 'Director General'),
            ('division_manager', 'Division Manager'),
            ('director', 'Director'),
            ('admin', 'Admin'),
        ],
        default='director'
    )
    def __str__(self):
        return f"{self.user.username} - {self.role}"