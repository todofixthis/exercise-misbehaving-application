# Misbehaving Application Exercise
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

# Installation
1. Clone this repo and check out the `develop` branch.
2. [Create a virtualenv for the project.](http://virtualenvwrapper.readthedocs.org/en/latest/#introduction)
3. Run `pip install -r requirements.txt`.
4. Run `python manage.py migrate`.

# Reproducing the Bug
## Browser
1. Run `python manage.py runserver`.
2. Open <http://localhost:8000/applicant>.
3. Fill out the form fields and submit the form.
4. Reload the page.
5. You will get a weird error:

    > ### TypeError at /applicant  
    > must be string, not datetime.date
     
The only way to get the page to load again is to clear your session cookie.
    
## Unit tests
1. Run `python manage.py test`.
2. You will get two test failures when `ApplicantTestCase` runs.

**Important:**  If you are sure you installed the app correctly, but you get the wrong error when you try to reproduce the bug,
  please contact us before continuing the exercise.

## Hints
- This exercise has an easy solution and a hard solution.  The easly solution masks the real problem; the hard solution actually
  fixes it.
