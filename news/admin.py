from django.contrib import admin

# Register your models here.


from .models import TravelNews

@admin.register(TravelNews)
class TravelNewsAdmin(admin.ModelAdmin):
    '''
    Admin View for TravelNews
    '''
    list_display = ('title', 'published_date', 'category', 'read_time', 'image_url', 'link', 'content')
    search_fields = ('title', 'category')
   

