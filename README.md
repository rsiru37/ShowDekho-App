# SHOWDEKHO APP(WEB2)

## Description
A Full-Stack Web2 App(Similar to Book My Show), that has two different views one for Admins & one for Users, Users can book Shows for their Desired Movies, selection of theatres and Different Shows for Movies, I have also added a Search Functionality that allows users to add filters and search for movies based on Director, Ratings, Searching for theatres based on location,etc.. and once all the tickets gets booked, we will stop taking the bookings further as the House is full.
For Admins, Admins can create,Edit, Delete New Movies, Theatres and Shows that will be visible on user's View.

I have also implemented JWT Token Based Authentication, during the Login.
We also have an option to export csv for theatre Admins, So that the Theatre Admin, Could analyse the bookings made, for a particular show movie, etc..
We also have background workers that will send all the users a monthly report stating the bookings they made in a particular month, and also send a daily reminder to login to the App if they haven't logged in.
I have also used redis for caching

## Execution

1. Pip install All the dependencies(Flask, flask_sqlalchemy, flask_cors, flask_jwt_extended, flask_restful, celery, pdfkit, Mailhog, Redis, node, npm install
2. After all the Dependencies are installed, we have to start all the servers in wsl/ubuntu Machine
3. Goto Root directory of the Project, python app.py
4. Goto Frontend Directory, npm run dev
5. Go to root directory, redis-server
6. Start the celery beat server, celery -A app.celery beat --max-interval 5 -l info
7. Start the celery worker, celery -A app.celery worker -l info
8. Install Go and start the MailHog server, by ./MailHog from the directory of MailHog to receive the Mails
9. Then goto, localhost:5173/ and the Add is started, You are good to use the app.

Admin Credentials:
boss@xyz
pwd: 123

## Authors
RAJ SIRUVANI
