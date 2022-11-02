from django.contrib import admin

# Register your models here.
from .models import User
from .models import Post
from .models import Follow
from .models import Like

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)