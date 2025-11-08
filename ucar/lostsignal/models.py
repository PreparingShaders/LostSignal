from django.db import models

class Allert(models.Model):
    STATUS_CHOICES = [
         ('open', 'Open'),
         ('resolved', 'Resolved')
     ]

    SOURCE_CHOICES = [
         ('operator', 'Operator'),
         ('monitoring', 'Monitoring'),
         ('partner', 'Partner'),
     ]

    create_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='open')
    source = models.CharField(max_length=40, choices=SOURCE_CHOICES, default='operator')
    device_id = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return f'{self.device_id} {self.status} {self.descriptions[:50]}'
