from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Student)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Hashtag)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post_id','photo_tag']
    
    def photo_tag(self, image):
        if image.image:
            return mark_safe(f'<img src="{image.image.url}" style="width:50px;" />')
        return None
    photo_tag.short_description = 'Image'