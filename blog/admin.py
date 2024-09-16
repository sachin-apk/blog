from django.contrib import admin
#imported manually
from .models import Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content','updated_at')
    list_filter = ('created_at', )
    serach_fields = ('title', 'content')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text')
    list_filter = ('created_at', )
    search_fields = ('title', 'text')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)