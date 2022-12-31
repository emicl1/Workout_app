# Workout App

### Thanks to Candito training for the workout plan

First of all I want to thank Candito training HQ, because my app uses the [Candito 6-week program](http://www.canditotraininghq.com/free-programs/)
as a base for the workouts. Feel free to contribute to Candito Training, because his 
workouts are awesome and I personally use them and they´ve helped me achieve my goals.


### Why this app?

I´ve been using the Candito 6 week program for a while now and I´ve always been annoyed
by the fact that I need to open the Excel file to look at my workouts. Another issue is 
that when I finish the training cycle I need to manually change the weights for the next
cycle. To add to that, I also want to track my progress and I want to be able to write 
down notes for workouts, if i want to, or to just write down if i completed the workout. 
So I decided to create this app to solve all of these issues.

### How to use the app
This app is still in the process of writing, so it´s not finished yet, and there´s still
not a builder fot the app for the android platform. But you can still use the app by
cloning the repository and running the app on your computer device. The app uses the 
file named Candito 6-Week Program.xlsx, which is located in the root folder of the app.
That there are two python files excel_calculs.py and pd_excel_work.py. The first one
is used to interact with the Excel file, changing and reading it´s values. The second one 
is used to create the pandas dataframe to be able to interact with the data more conveniently.
Then there´s the main.py file, which is the main file of the app. It´s used to create the 
app and to run it. The app is created using the kivy framework, so you need to have kivy
installed on your computer to be able to run the app. Then there´s the file named my.kv 
which is used to create the layout of the app. 

When you first open the app, you will see the main_menu screen, which is the screen where you
can add an account ot login into your existing account. It uses a sqlite database to store
the accounts. The database is located in the root folder of the app and it´s named users.db.
When you login into your account, you will be redirected to the main screen, no further 
functionality is implemented yet.



