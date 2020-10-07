#  # MyTwitter
Twitter authentication using Tweepy API using Django. The application can be used for the following purpose :

-   Fetching tweets of authenticated users containing URLs.
    
-   Viewing the tweets fetched till date.
    
-   Displaying the most shared Domain from the database.
    
-   Displaying the User who shared maximum URLs.


  ## Pre-requisites (to run App locally)
  -   Python 3.6 and pip should be preinstalled
    
-   Twitter developer Credentials
    
-   PostgreSQL database
    


## Tech Stack

-   Programming Languages
    

-   Python 3.6
    

-   Frameworks
    

-   Django 3.1.2
    

-   Database
    

-   PostgreSQL
    

-   Frontend
    

-   HTML 5
    
-   CSS 3
    
-   Jinja
    
-   Bootstrap 4
    

-   APIs
    

-   Tweepy Api



## SetUp
1.  The first thing to do is to clone the repository:
    

$ git clone https://github.com/Mansi25/MyTwitter_Assignment

2.  Generate CONSUMER_KEY and CONSUMER_KEY from Twitter Developer console and paste them in the .env file .
    

Enter Database credentials in .env file along with the seceret key.

3.  Create a virtual environment to install dependencies in and activate it:
    

$ virtualenv2 --no-site-packages env

$ source env/bin/activate

4.  Then install the dependencies:
    

(env)$ pip install -r requirements.txt

Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

5.  Once pip has finished downloading the dependencies:
    

Migrate the tables to the database.

python manage.py makemigrations

python manage.py migrate

And navigate to http://127.0.0.1:8000

## Link 
- The github repository link for the assignment can be found ([here](https://github.com/Mansi25/Cloudflare-summer-intern)).
      
   
    
