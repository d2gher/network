from django.contrib import admin

# Register your models here.
from .models import User
from .models import Post
from .models import Follow

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)