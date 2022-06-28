from django.db import models
from PIL import Image
from django.urls import reverse
from django.contrib.auth.models import User
from offer.models import Gasstation

# Create your models here.
class Profile(models.Model):
    roles = (
        ('manager', 'Manager'), 
        ('cashier','Cashier'), 
        ('auditor','Auditor'), 
        ('finance','Finance'), 
        ('staff','Staff')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    manager_id = models.IntegerField(null=True, default=NULL)
    role = models.CharField(choices= roles, max_length=20, null= True, )
    gasstation = models.ForeignKey(Gasstation, on_delete=models.CASCADE, null= True, blank = True)#, default=NULL)
    image = models.ImageField(default='default.jpg', upload_to = 'profile_pics')

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def get_absolute_url(self): 
        return reverse('edit_cashier', args=[self.id])