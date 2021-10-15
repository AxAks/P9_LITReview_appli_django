# P9_LITReview_appli_django

## Chapters

1. [Presentation](#presentation)
2. [Prerequisites (for developers)](#prerequisites)
3. [Installation](#installation)
4. [Execution](#execution)
5. [Usage](#usage)
6. [Generation of a code review report (for developers)](#generation_of_a_code_review_report)
***

## 1. Presentation <a name="presentation"></a>
This Django Project is the MVP version of a website for sharing reviews on books and articles.
The registered users can request a review and/or give their impressions on their readings.
They will also be able to follow other users.
***

## 2. Prerequisites (for developers) <a name="prerequisites"></a>
This program runs under python 3.9 in a virtual environment.  
Thus, it is usable on Windows, Unix-based operating systems
insofar as the followings are installed:
- python 3.9 (including pip3)
- virtualenv

__Linux__  
_installation of python3.9:_    
$ sudo add-apt-repository ppa:deadsnakes/ppa    
$ sudo apt update     
$ sudo apt install python3.9    
_installation of pip3:_     
$ wget https://bootstrap.pypa.io/get-pip.py     
$ python3.9 get-pip.py    
$ pip --version    
_Installation of virtualenv :_      
$ sudo apt install virtualenv    

__Mac__  
_installation of python3.9 and pip3:_  
$ brew install python@3.9    
(pip3 comes along with it) 
if not, download and install the file get-pip.py from https://bootstrap.pypa.io/get-pip.py    
$ py get-pip.py       
_Installation of virtualenv :_    
$ pip3 install virtualenv
  
__Windows__     
_installation of python3.9 and pip3:_  
Download and install python 3.9 for windows from python.org    
(pip3 comes along with it)     
if not, download and install the file get-pip.py from https://bootstrap.pypa.io/get-pip.py    
$ py get-pip.py     
_Installation of virtualenv :_   
$ pip install virtualenv    
***

## 3. Installation <a name="installation"></a>

__Download the project:__    
_Via Git_      
$ git clone https://github.com/AxAks/P9_LITReview_appli_django.git    
    
_Via the Web_     
- Visit the page : https://github.com/AxAks/P9_LITReview_appli_django     
- Click on the button "Code"     
- Download the project     

__Linux / Mac__       
in the project directory in a shell:       
_create the virtual environment_       
$ python3.9 -m virtualenv 'venv_name'        
_activate the environment:_        
$ source 'venv_name'/bin/activate         
_install project requirements:_       
$ pip install -r requirements.txt         
  
__Windows__    
in the project directory in a shell:        
_create the virtual environment_      
$ virtualenv 'venv_name'      
_activate the environment:_     
$ C:\Users\'Username'\'venv_name'\Scripts\activate.bat       
_install project requirements:_            
$ pip install -r requirements.txt
***

## 4. Execution <a name="execution"></a>
from the terminal, in the root directory of the project:

_activate the environment:_    
$ source 'venv_name'/bin/activate        
_launch the Django server_       
$ python LITReview/manage.py runserver    
_visit the website locally_       
Open your web browser and visit the URL:     
localhost:8000 (or 0.0.0.0:8000)       
-> You land on the Login/Signup page           
***

## 5. Usage <a name="usage"></a>

__Registration and/or Login__    
_If you do not have an account yet: "S'inscire"_        
- Fill out the form and submit     
-> If the form is valid, your account is created and you are redirected to the Home Page/Feed     

_If you already have an account: "Se connecter"_
- Enter your credentials and submit, you are then redirected to the Home Page/Feed

_Top Menu_   
- it is available thoughout the site and enables you to navigate from page to page on the website:        
-> General Feed (Flux) with the list of posts (Tickets and Reviewws) from you and the users you follow     
-> Your Posts (Posts) with only your Posts     
-> Subscriptions (Abonnements) is where you can see the users following you and manage your subscriptions to other users    
-> Logout (Se déconnecter) to logout. You are then redirected to the login page     


__Posts Lists (Flux/Posts)__    
_Flux_    
- Lists the Ticket and Reviews by you and the users you follow     
-> You can check what other user think of the books    
-> You can reply to the Tickets requesting a review by creating one if it is not already replied     

_Posts_     
- Lists your own posts only    
-> You can edit your tickets if they have not been replied to yet      
-> You can also delete your tickets if they have not been replied to yet    

_Commons_       
-> Two buttons on both pages enable you to create a ticket (Demander une Critique) 
or a non ticket-bound review (Créer une critique).      
In the latter case, you will have to provide ticket information AND the review in the form      


__Subscriptions (Abonnements)__         
_Search a user you want to follow_        
- Enter the Username (or part of it) of the user to research and submit       
(Note that you need to know their username)        
-> The list of matching users is returned excluding your profile and those of the users you already follow    
  
_Follow the user when found_    
- From the list of users found, you can choose the one you want to follow by clicking on "S'abonner"      
-> The user is added to your subscriptions and you will see their post appear in your feed        
 
_Unfollow a user you were following_       
- The table "Mes Abonnement" (My subscriptions) lists you subscriptions.       
- You can choose to unfollow a user by clicking on "Se désabonner" under their name.      
-> The user will be removed from the list and you will not see their posts in your feed any longer    

_See who is following you_
- The bottom table list the users currently following you.

## 6. Generation of a code review report (for developers) <a name="generation_of_a_code_review_report"></a>
__flake8_html__    
_Launch the Analysis_

- at the project root level           
$ flake8 --format=html --htmldir=flake-report . -v
format = format of the report (html)    
htmldir = name of the directory to be created to store the report (mandatory)    
. = current directory    
-v = verbose (optional)    

- from anywhere in the system    
$ flake8 --format=html --htmldir=flake-report --config=[path/to/config/file] [path/to/project/root/] -v          
config = 'setup.cfg', located at the root of the project (mandatory if not in the working directory)     

see more options here:  
https://flake8.pycqa.org/en/latest/user/options.html  
note: setup.cfg file excluding files from the analysis 
and setting te limit to 119 characters per line  

to read the reports:  
- browse files to the 'flake-report' directory
- open the file index.html in a web-browser
***
