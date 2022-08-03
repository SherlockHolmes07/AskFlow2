from django.contrib import admin
from .models import  User, Question, Tags, Answer,  CommentsQ, upvotes_Question, downvotes_Question

# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Tags)
admin.site.register(Answer)
admin.site.register(CommentsQ)
admin.site.register(downvotes_Question)
admin.site.register(upvotes_Question)
