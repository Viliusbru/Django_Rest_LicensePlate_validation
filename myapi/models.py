from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



class Plate(models.Model):
    plate = models.CharField(
        max_length=6, 
        validators=[RegexValidator(
            regex=r'[a-zA-Z]{3}\d{3}',
            message='Invalid format', 
            code='Invalid input format')])
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.plate, self.date_added, self.user.username)

    def save(self, *args, **kwargs):                       # converts strings to uppercase
        self.plate = (self.plate).upper()
    
