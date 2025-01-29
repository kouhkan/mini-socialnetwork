from django.contrib import admin

from apps.post.models import Post, Rate, Reaction

# Register your models here.
admin.site.register(Post)
admin.site.register(Rate)
admin.site.register(Reaction)
