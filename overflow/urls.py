from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("ask", views.askQuestion, name="askQuestion"),
    path("save", views.saveQue, name="saveQue"),
    path("tag/<str:name>", views.tag, name="tag"),
    path("question/<int:id>", views.get_question, name="question" ),
    path("addCommentQ", views.addCommentQ, name="addCommentQ"),
    path("postAnswer", views.postAnswer, name="postAnswer"),
    path("deleteQue", views.deleteQue, name="deleteQue"),
    path("profile/<int:id>", views.profile, name="profile"),

    #apis
    path("unlikeUpvote", views.dislikeUpvote, name="dislikeUpvote"),
    path("likeUpvote", views.likeUpvote, name="likeUpvote"),
    path("dislikeDownvote", views.dislikeDownvote, name="dislikeDownvote"),
    path("likeDownvote", views.likeDownvote, name="likeDownvote"),
    path("eSaveQue", views.eSaveQue, name="eSaveQue"),
    path("saveAns", views.saveAns, name="saveAns"),
    path("deleteAns", views.deleteAns, name="deleteAns"),
]
