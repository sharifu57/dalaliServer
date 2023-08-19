from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class MainModel(models.Model):
    is_active = models.BooleanField(null=True, blank=True, default=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def softdelete(self):
        self.is_deleted = True
        self.is_active = False
        self.updated = pendulum.now()
        self.save()

    class Meta:
        abstract = True


IDTYPE = (
    (1, 'nida'),
    (2, 'birth certificate'),
    (3, 'TIN'),
    (4, 'license')
)


class UserProfile(MainModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE) #related table Owner
    phone_number = models.CharField(max_length=300, blank=True, null=True)
    gender = models.IntegerField(choices=((1, 'Male'), (2, 'Female')), null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    id_type = models.IntegerField(choices=IDTYPE, null=True, blank=True)
    id_number = models.CharField(max_length=300, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):

        return self.user.username if user else ''

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

PROPERTY_STATUS = (
    (1, 'available'),
    (2, 'rented'),
    (3, 'unavailable')
)

PROOPERTY_LOCATION = (
    ('mbezi', 'Mbezi'),
    ('kimara', 'Kimara')
)

class Property(MainModel):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, null=True, blank=True)
    property_number = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    property_type = models.ForeignKey("dalali.PropertyType", null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.IntegerField(choices=PROPERTY_STATUS, null=True, blank=True)
    location = models.CharField(choices=PROOPERTY_LOCATION, null=True, blank=True, max_length=200)

    def __str__(self):

        return self.property_number
    


class PropertyType(MainModel):
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    icon = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)

    def __str__(self):

        return self.title


class Amenity(MainModel):
    name = models.CharField(max_length=300, null=True, blank=True)
    decription = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class PropertyAmenity(MainModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id

class PropertyPhoto(MainModel):
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
    url = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)

    def __str__(self):
        return self.property.title


class Tennant(MainModel):
    first_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):

        return f"{self.first_name} {self.last_name}"

BOOKING_STATUS = (
    (1, 'Pending'),
    (2, 'Confirmed'),
    (3, 'Terminated'),
)

class Booking(MainModel):
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
    tennant = models.ForeignKey(Tennant, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=BOOKING_STATUS, null=True, blank=True)

    def __str__(self):
        return f"{self.property.title} {self.tennant.last_name}"


class Communication(MainModel):
    sender = models.ForeignKey(Tennant, on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.sender.first_name} {self.receiver.last_name}"


    
    
    
