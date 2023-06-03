from django.contrib import admin
from .models import Author, Post, Tag


# Register your models here.
# make the slug field of Post read-only and populated automatically by the title field
class PostAdmin(admin.ModelAdmin):
    list_filter = ('author', 'tags', 'date')
    list_display = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
