How to Run The ShowDekho App

1.) Pip install All the dependencies(Flask, flask_sqlalchemy, flask_cors, flask_jwt_extended, flask_restful, celery, pdfkit, Mailhog, Redis
2.) After all the Dependencies are installed, we have to start all the servers in wsl/ubuntu Machine
3.) Goto Root directory of the Project, python app.py
4.) Goto Frontend Directory, npm run dev
5.) Go to root directory, redis-server
6.)Start the celery beat server, celery -A app.celery beat --max-interval 5 -l info
7.) Start the celery worker, celery -A app.celery worker -l info
8.) Install Go and start the MailHog server, by ./MailHog from the directory of MailHog to receive the Mails

Then goto, localhost:5173/ and the Add is started, You are good to use the app.

Admin Credentials:
boss@xyz
pwd: 123