# CS50 Web Final Project: AskFlow
 Its a community based web application built using Django can be used for asking questions and answering to the questions of others.
<br /> You can relate it to applications like Quora or StackOverflow.

<br />

# Distinctiveness and Complexity
 Now this project which i have named <b>AskOverflow</b> is fairley distinct and even closely from any other applications in this course. <br />Below I have broken down its functionality to help assess its distinctiveness and complexity.

<br />

## Functionlities of the application
<ul>  
<li> User has ability to both register and login </li>

<li> Only authenticated users are allowed to post question, comments, answers, like and dislike the posts. While an unauthenticated user can Search for questions, filter them through tags and can see their answers.</li>

<li>It provides user with the functionality of Asking questions.
</li>
<li>
The questions asked by the user can be written in Markdown format and posted.
</li>
<li>User can also attach some tags of topics on which the question is based upon.
</li>
<li>
This tags also been used in way that users can filter questions related to a particular tag by clicking on it.
</li>

<li>
The index and the profile page also includes pagination feature.
</li>

<li>
It includes a search bar which could be used to search for questions.
</li>

<li>
Questions consits for title and description. Search bar results in the list of question-titles with their respective Author's name and number of answers posted by the community for that question.   
</li>

<li>
    By clicking on to the title user will be directed towards the Question page. Which consists of question with it's description, author, comments and a list of answers.
</li>

<li>
     Answers also has their author name with them by a click on them you will be directed to the profile page of the user.
</li>

<li>
    Profile page consists of User's details with number of questions and answer they have asked, replied to and all the posts created by them.
</li>

<li>
    Any user can post answer for any question or comment on question as long as they are logged in.
</li>

<li>
    Users can also like and dislike various question. Like and Dislike button both works asynchronously ustilizing <b>javascript</b>
</li>

<li>
    The creator of the post has the ability to edit or delete the post. Edit, Save and Close  button works <b>asynchronously</b>.
</li>

<li>
    The answers can also be both edited and deleted by their authors and both the buttons works asynchronously.
</li>

<li>User can use markdown syntax for posting questions and answers.
</li>

</ul>

<br />

The above functionalities  depicts the <b>distinctiveness and complexity</b> of the application and as for the other required features as mentioned  the  project utilizes<b> Django, Javascript and it has  7 models </b> including user model and the application is also <b> mobile responsive </b>.

<br />
<br />

 # Structure of the Application: Askflow

It's a Django based application the application directory Capstone consists 2 sub dirs capstone and overflow, 3 files manage.py, db.sqlite3 and readme.md. <br />
Let's start with manage.py

### manage.py <br /> 
This file is used as a command-line utility for the project. 
The file contains the code for running the server, makemigrations or migrations, and several other commands as well.

### db.sqlite3 <br />
This is a sqlite3 default database that django provides used as a database in our project.

<br />

### capstone Directory
 It consists of configuration files for the project. I have only made changes to <b>settings.py</b> and <b>urls.py</b> by adding a overflow as a installed app and including overflow/urls.py path in urls.py.

<br />

 ## overflow
 It's our main application.

 ### overflow/models.py
 Models.py represents the models of web applications in the form of classes. They defines the structure of the database. It has 7 django models. The 7 models are:
<br /> User - storing user data <br />
Question - storing question data <br />
Tags - storing tags and their relations. <br />
Answers - storing answers data. <br />
CommentsQ - storing comments <br />
upvotes_Question - storing upvotes <br />
downvotes_Question - storing downvotes <br />

 ### overflow/admin.py
 Contains code for registering models to the admin site. So we can access the models in the admin interface.

 ### overflow/apps.py
 It's a configuration file includes application configration.

 ### overflow/urls.py
 It consits of various url's path linking the users url request to various pages and it also consists of various api routes all the routes are inside of list <i> urlpatterns </i>.

 ### overflow/views.py
 It contains all the views in form of class and functions. <br /> It consists of various functions login, logout, index etc.
It also contains Django forms.

 ### oveflow/templates\overflow
 It's a template directory consists of various html files utitlizing django templating language. <br />
The <b>layout.html</b> is the base template every other file extends from layout.html. <br />
<b>index.html:</b> contains index page. <br /> <b>ask.html:</b> contains ask question form. <br />
<b>login.html:</b> contains login form. <br />
<b>profile.html:</b> contains profile page of user. <br />
<b>register.html:</b> contains registration form. <br />
<b>que.html:</b>  contains que page. <br />

 ### overflow/static\overflow
 It conatins .svg files having icons utilized in the application. <br />
Then it conatins 2 css files: 
<b> style.css </b> and <b> index.css </b> both are used for styling purposes for html pages in templates\oveflow folder.
<br /> This folder also contains 3 javascript files: <br />
 ### script.js:
 It implements like and dislike functionality asynchronously  and fetch's the backend Api for increasing like and dislikes.<br />
 ### edit.js:
It implements the edit question functionality asynchronously also implements save and close buttons.
 ### edit_ans.js:
It implements the edit, delete, save and close button for answer asynchronously.

<br />

 # How to run the Application
 Python, Pip and Django are need to be preinstalled. <br />
 Clone the application `git clone url`  <br />go to directory then<br /> `python manage.py makemigrations`
<br /> `python manage.py migrate`
<br /> `python manage.py runserver` <br />
 ### Create a super user: 
 `python manage.py createsuperuser`
