from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

CATERGORY_CHOICES = (
    ('S', 'Shirt'),   #(value in database, value displayed )
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATERGORY_CHOICES, max_length=2, default='S')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1,default='P')
    slug = models.SlugField(unique = True,blank=True)
    description = models.TextField(default='A Shirt')
    quantity = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product", kwargs = {
            'slug': self.slug
        })

class OrderItems(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItems)
    start_date = models.DateField(auto_now_add = True)
    ordered_date = models.DateField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    pass