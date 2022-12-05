from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class FamilyMembers(models.Model):
    familyLead = models.ForeignKey(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, default=None)
    lastName = models.CharField(max_length=100, default=None)
    profession = models.CharField(max_length=100, default=None)
    income = models.BigIntegerField(max_length=5000000000000000, default=0)

    def __str__(self):
        return self.firstName


class Expenses(models.Model):
    familyLead = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(FamilyMembers, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=100, default=None)
    expense = models.BigIntegerField(max_length=100000000000000000, default=0)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)
