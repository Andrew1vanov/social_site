from django.db import models
from django.conf import settings
from django.utils.text import slugify 

# Create your models here.

class Image(models.Model):
    
    #Указывается юзер, который сделал закладку на это изображение.
    #foreignKey - внешинй ключ
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             related_name = 'images_created', 
                             on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)#заголовок изображения
    slug = models.SlugField(max_length = 200, blank = True)
    url = models.URLField(max_length = 2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank = True)
    created = models.DateField(auto_now_add = True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, 
                                        related_name = 'images_liked',
                                        blank = True)

    class Meta:
        indexes = [models.Index(fields=['-created']),]
        ordering = ['-created'] #указывает django сортировать по созданному полю
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)#автоматическое формирование slug
        super().save(*args, **kwargs)