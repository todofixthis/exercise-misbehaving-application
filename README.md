# exercise-misbehaving-application
Unit tests are failing, the app crashes after the first request... what's going on here?!

## Objective
One of your fellow developers is building a web application to collect information about bank loan applicants.  However,
  the application keeps crashing, and nobody can figure out why.  You have been tasked with hunting down the source of
  the bug and fixing the issue.

## Installation
1. Clone this repo and check out the `develop` branch.
2. [Create a virtualenv for the project.](http://virtualenvwrapper.readthedocs.org/en/latest/#introduction)
3. Run `pip install -r requirements.txt`.
4. Run `python manage.py migrate`.

## Reproducing the Bug
### Browser
1. Run `python manage.py runserver`.
2. Open <http://localhost:8000/applicant>.
3. Fill out the form fields and submit the form.
4. Reload the page.
5. You will get a weird error:

    > ### TypeError at /applicant  
    > must be string, not datetime.date
     
The only way to get the page to load again is to clear your session cookie.
    
### Unit tests
1. Run `python manage.py test`.
2. You will get two test failures when `ApplicantTestCase` runs.

Good luck!
