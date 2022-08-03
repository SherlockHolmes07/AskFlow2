from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """joined_date(auto),
    answers(default=0), questions(default=0),
    """
    joined_date = models.DateTimeField(auto_now_add=True)
    answers = models.IntegerField(default=0)
    questions = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} created"

class Question(models.Model):
    """title, body(Text), upvotes(default=0), downvotes(default=0), user(Fk), date(auto), no_answer(default=0), verified_answer"""

    title = models.CharField(max_length=500)
    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_questions"
    )
    date = models.DateTimeField(auto_now_add=True)
    no_answer = models.IntegerField(default=0)
    verified_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} asked by {self.user.username}"


class Tags(models.Model):
    """tag(string), question(Fk)"""

    tag = models.CharField(max_length=50)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="get_tags"
    )

    class Meta:
        unique_together = (
            "tag",
            "question",
        )

    def __str__(self):
        return f"{self.tag} for {self.question.id}"


class Answer(models.Model):
    """body(Text), upvotes(default=0), downvotes(default=0), question(Fk), user(Fk), verified_answer(default=False), date(auto)"""

    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="get_answer"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_ans_user"
    )
    verified_answer = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answere for {self.question.title} by {self.user.name}"


class CommentsQ(models.Model):
    """body(Text), user(Fk), date(auto), question(Fk)"""

    body = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_comment_user_Q"
    )
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="get_comments_q"
    )

    def __str__(self):
        return f"Comment by {self.user.name} for {self.question.title}"


class upvotes_Question(models.Model):
    """user(Fk), question(Fk)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_upvotes_que")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="get_upvotes_que")

    class Meta:
        unique_together = (
            "user",
            "question",
        )
    
    def __str__(self):
        return f"{self.user.username} upvoted for {self.question.id}"

class downvotes_Question(models.Model):
    """user(Fk), question(Fk)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_downvotes_que")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="get_downvotes_que") 

    class Meta:
        unique_together = (
            "user",
            "question",
        )

    def __str__(self):
        return f"{self.user.username} downvoted for {self.question.id}"
