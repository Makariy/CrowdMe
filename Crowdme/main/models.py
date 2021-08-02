from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django import forms

# from django.db.models.fields.files import ImageFieldFile
# Create your models here.


# s = ImageFieldFile(instance=None, field=FileField(), name='main/featured2.jpg')
# model.image_file = s

class Project(models.Model):
    title = models.CharField(max_length=40, null=False, db_index=True, verbose_name='Title')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    cost = models.IntegerField(verbose_name='Cost')
    funded = models.IntegerField(default=100, validators=[MinValueValidator(0, 'The funded value was not greater than 0'), \
                                 MaxValueValidator(100, 'The funded value was not less than 100')], verbose_name='Funded')
    days_left = models.IntegerField(null=True, blank=True, verbose_name='Days left')
    published_date = models.DateField(auto_now=True)
    is_new = models.BooleanField(null=False, verbose_name='Is new', default=True)

    image_file = models.ImageField(upload_to='main/', null=True, verbose_name='Image file name')

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-published_date']

    def __str__(self):
        s = 'Title: ' + str(self.title) + '\n'
        s += 'Description: ' + str(self.description) + '\n'
        s += 'Cost: ' + str(self.cost) + '\n'
        s += 'Funded: ' + str(self.funded) + '\n'
        s += 'Days left: ' + str(self.days_left) + '\n'
        s += 'Date: ' + str(self.published_date) + '\n'
        s += 'New: ' + str(self.is_new)
        return s


