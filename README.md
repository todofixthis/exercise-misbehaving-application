# exercise-misbehaving-application
Unit tests are failing, the app crashes after the first request... what's going on here?!

## Objective
One of your fellow developers is building a web application to collect information about bank loan applicants.  The user is
  presented with a field to enter details about an applicant (name, birthday, email, etc.), and then the values are stored in
  the user's session.
  
On subsequent page loads, the applicant details are retrieved from the session to pre-fill the form, display on the page, etc.

The app appears to work correctly the first time the user submits the form.  The applicant details appear correctly, and
  checking the database shows that the data were stored correctly in the session.

However, on all subsequent page views, the application crashes with a weird error, and the only way to recover from the
  error is to delete the browser's session cookie or clear out the contents of the session in the database.
  
You have been tasked with tracking down the source of the problem, and fixing it.

## Meta-Objective
Since this is an exercise, the approach(es) you take to sloving the problem are just as important as the solution itself.
  Just like a math test, you won't get credit if you don't show your work, so make sure to include with your solution a screen
  recording or other detailed description of the exact steps you took during the entirety of the exercise.
  
There are multiple ways to solve this problem, but some are objectively better (in terms of performance, reliability and
  maintainability) than others.  Be prepared to explain not just how your solution works, but also *why* you chose it.

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
