from django.contrib import admin
from .models import Comment
from .models import Favorite
from .models import Lecture
from .models import Proposal
from .models import CustomeUser
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, PostAdmin)
admin.site.register(Favorite, PostAdmin)
admin.site.register(Lecture, PostAdmin)
admin.site.register(Proposal, PostAdmin)
admin.site.register(CustomeUser, PostAdmin)
