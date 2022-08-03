import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from flask import request_finished
from .models import (
    Answer,
    CommentsQ,
    User,
    Question,
    Tags,
    upvotes_Question,
    downvotes_Question,
)
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.core.paginator import Paginator
import markdown2

# Form to Ask Question
class askForm(forms.Form):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ask",
                "placeholder": "Write a title for the question",
            }
        ),
    )
    body = forms.CharField(
        label="Body",
        widget=forms.Textarea(
            attrs={
                "class": "form-control ask",
                "placeholder": "You may write description in markdown syntex and include all the information someone would need to answer your question.",
            }
        ),
    )
    tags = forms.CharField(
        label="Tags",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ask",
                "placeholder": "example: (django php mysql)",
            }
        ),
    )


# Create your views here.
def index(request):

    if request.method == "POST":
        # If accessed via post for search
        sample = request.POST["search"].strip()

        # Checking if its empty
        if sample == None or sample == "":
            return HttpResponseRedirect(reverse("index"))
        # Getting all the Questions
        questions = Question.objects.all().order_by("-date")
        obj = []
        # Looping over the questions an checking for a match
        for q in questions:
            if sample.lower() in q.title.lower():
                t = Tags.objects.filter(question=q)  # Filtering tags
                # print(t)
                # Computing date time and stuff and appending it in an object
                dd = datetime.now(timezone.utc) - q.date
                min = int(round(dd.total_seconds() / 60, 0))
                time = int(round(dd.total_seconds() / 3600, 0))
                # print(time)
                if time < 1:
                    time = f"{min} minutes"
                else:
                    time = f"{time} hours"
                obj.append(
                    {
                        "que": q,
                        "tags": t,
                        "days": f"{(datetime.now(timezone.utc) - q.date).days} days",
                        "time": time,
                    }
                )
        #print(obj)

        # Applying Pagination
        paginator = Paginator(obj, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "overflow/index.html",
            {
                "objects": page_obj,
            },
        )

    # If accessed via GET
    else:

        que = Question.objects.all().order_by("-date")
        obj = []
        # Looping over the questions
        for q in que:
            t = Tags.objects.filter(question=q)
            # print(t)
            # Computing date time stuff and appending in an object
            dd = datetime.now(timezone.utc) - q.date
            min = int(round(dd.total_seconds() / 60, 0))
            time = int(round(dd.total_seconds() / 3600, 0))
            # print(time)
            if time < 1:
                time = f"{min} minutes"
            else:
                time = f"{time} hours"
            obj.append(
                {
                    "que": q,
                    "tags": t,
                    "days": f"{(datetime.now(timezone.utc) - q.date).days} days",
                    "time": time,
                }
            )

        # Applying Pagination
        paginator = Paginator(obj, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "overflow/index.html",
            {
                "objects": page_obj,
            },
        )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "overflow/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "overflow/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "overflow/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "overflow/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "overflow/register.html")


@login_required(login_url="login")
def askQuestion(request):
    # Just renders the empty question Form
    return render(request, "overflow/ask.html", {"form": askForm()})


@login_required(login_url="login")
def saveQue(request):
    # Saves the Question form subbmited
    if request.method == "POST":

        form = askForm(request.POST)
        # Checks forms validity
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            tags = form.cleaned_data["tags"]
            user = User.objects.get(id=request.user.id)
            list_tags = tags.split()
            user.questions += 1
            user.save()
            q = Question(title=title, body=body, user=user)
            q.save()

            for tag in list_tags:
                t = Tags(tag=tag, question=q)
                t.save()

            return HttpResponseRedirect(reverse("index"))


def tag(request, name):

    # Renders index.html page with all the question related to the tag passed as "name"
    tags = Tags.objects.filter(tag=name)

    if len(tags) == 0:
        return HttpResponseRedirect(reverse("index"))
    else:
        obj = []
        for tag in tags:
            t = Tags.objects.filter(question=tag.question)
            # print(t)
            dd = datetime.now(timezone.utc) - tag.question.date
            min = int(round(dd.total_seconds() / 60, 0))
            time = int(round(dd.total_seconds() / 3600, 0))
            # print(time)
            if time < 1:
                time = f"{min} minutes"
            else:
                time = f"{time} hours"
            obj.append(
                {
                    "que": tag.question,
                    "tags": t,
                    "days": f"{(datetime.now(timezone.utc) - tag.question.date).days} days",
                    "time": time,
                }
            )
        print(obj)

        # Applying Pagination
        paginator = Paginator(obj, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "overflow/index.html",
            {
                "objects": page_obj,
            },
        )


def get_question(request, id):
    if request.method == "POST":
        pass
    else:
        que = Question.objects.get(id=id)
        ans = Answer.objects.filter(question=que)

        # Votes
        upvotes = upvotes_Question.objects.filter(question=que).only("user")
        downvotes = downvotes_Question.objects.filter(question=que).only("user")

        upvote = False
        downvote = False

        for vote in upvotes:
            if request.user.id == vote.user.id:
                upvote = True

        for vote in downvotes:
            if request.user.id == vote.user.id:
                downvote = True

       # print(upvote)
       #print(downvote)

        # Calculating time since question is asked
        dd = datetime.now(timezone.utc) - que.date
        min = int(round(dd.total_seconds() / 60, 0))
        time = int(round(dd.total_seconds() / 3600, 0))
        print(time)
        if time < 1:
            time = f"{min} minutes"
        else:
            time = f"{time} hours"

        t = Tags.objects.filter(question=que)

        # Acessing Comments
        comments = CommentsQ.objects.filter(question=que)

        # Answers
        answers = Answer.objects.filter(question=que)

        for ans in answers:
            ans.body = markdown2.markdown(ans.body)

        return render(
            request,
            "overflow/que.html",
            {
                "question": que,
                "answers": ans,
                "days": f"{(datetime.now(timezone.utc) - que.date).days} days",
                "time": time,
                "body": markdown2.markdown(que.body),
                "upvote": upvote,
                "downvote": downvote,
                "tags": t,
                "comments": comments,
                "answers": answers,
            },
        )


# Decrease Up vote
def dislikeUpvote(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data["id"])
        que = Question.objects.get(id=data["id"])
        upvotes_Question.objects.filter(user=request.user, question=que).delete()
        que.upvotes -= 1
        que.save()
        return HttpResponse("Sucessfully Disliked Upvote", status=200)


# Increase Up vote
@login_required(login_url="login")
def likeUpvote(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data["id"])
        que = Question.objects.get(id=data["id"])
        vote = upvotes_Question(user=request.user, question=que)
        vote.save()
        que.upvotes += 1
        res = downvotes_Question.objects.filter(user=request.user, question=que)

        if len(res) != 0:
            print("inside up")
            que.downvotes -= 1
            res.delete()

        que.save()
        return HttpResponse("Sucessfully liked the Upvote", status=200)


@login_required(login_url="login")
def dislikeDownvote(request):
    if request.method == "POST":
        data = json.loads(request.body)
        que = Question.objects.get(id=data["id"])
        downvotes_Question.objects.filter(user=request.user, question=que).delete()
        que.downvotes -= 1
        que.save()
        return HttpResponse("Sucessfully Disliked Downvote", status=200)


@login_required(login_url="login")
def likeDownvote(request):
    if request.method == "POST":
        data = json.loads(request.body)
        que = Question.objects.get(id=data["id"])
        vote = downvotes_Question(user=request.user, question=que)
        vote.save()
        que.downvotes += 1
        # print(que.downvotes)

        res = upvotes_Question.objects.filter(user=request.user, question=que)

        if len(res) != 0:
            res.delete()
            que.upvotes -= 1

        que.save()
        return HttpResponse("Sucessfully Liked Downvote", status=200)


@login_required(login_url="login")
def addCommentQ(request):
    if request.method == "POST":
        # Just access the body of the comment and saves comment in the commentQ table
        comment = request.POST["comment"]
        id = request.POST["id"]
        que = Question.objects.get(id=id)
        c = CommentsQ(user=request.user, body=comment, question=que)
        c.save()
        return HttpResponseRedirect(reverse("question", args=(id,)))


@login_required(login_url="login")
def postAnswer(request):
    if request.method == "POST":
        body = request.POST["answer"]
        id = request.POST["id"]
        user = User.objects.get(id=request.user.id)
        que = Question.objects.get(id=id)
        ans = Answer(body=body, question=que, user=user)
        ans.save()
        que.no_answer += 1
        que.save()
        user.answers += 1
        user.save()
        return HttpResponseRedirect(reverse("question", args=(id,)))


@login_required(login_url="login")
def eSaveQue(request):
    if request.method == "POST":
        data = json.loads(request.body)
        que = Question.objects.get(id=data["id"])
        que.body = data["body"]
        que.save()
        return HttpResponse("Sucessfully saved edited question", status=200)


@login_required(login_url="login")
def deleteQue(request):
    if request.method == "POST":
        Question.objects.filter(id=request.POST["id"]).delete()
        user = User.objects.get(id=request.user.id)
        user.questions -= 1
        user.save()
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def saveAns(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ans = Answer.objects.get(id=data["id"])
        ans.body = data["body"]
        ans.save()
        return HttpResponse("Sucessfully saved the answer", status=200)


@login_required(login_url="login")
def deleteAns(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ans = Answer.objects.get(id=data["id"])
        que = Question.objects.get(id=ans.question.id)
        user = User.objects.get(id=request.user.id)
        user.answers -= 1
        que.no_answer -= 1
        que.save()
        ans.delete()
        user.save()
        return HttpResponse("Answer deleted sucessfully", status=200)


def profile(request,id):
    print(id)
    user = User.objects.get(id=id)
    print(user)
    ques = Question.objects.filter(user=user)

    obj = []
    # Looping over the questions
    for q in ques:
        t = Tags.objects.filter(question=q)
        # print(t)
        # Computing date time stuff and appending in an object
        dd = datetime.now(timezone.utc) - q.date
        min = int(round(dd.total_seconds() / 60, 0))
        time = int(round(dd.total_seconds() / 3600, 0))
        # print(time)
        if time < 1:
            time = f"{min} minutes"
        else:
            time = f"{time} hours"
        obj.append(
            {
                "que": q,
                "tags": t,
                "days": f"{(datetime.now(timezone.utc) - q.date).days} days",
                "time": time,
            }
        )

    # Applying Pagination
    paginator = Paginator(obj, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
            request,
            "overflow/profile.html",
            {
                "objects": page_obj,
                "User": user,
            },
    )

