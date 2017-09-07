_This exercise is based on a real problem that we had to solve at EFL.  It is
designed to show you an example of the kinds of challenges you would be working
on at EFL, as well as to help us understand how you approach these kinds of
challenges!  Good luck, and above all, have fun!_

# Misbehaving Application Exercise
You are building a web application to collect information about bank loan
applicants.

The user is presented with a form to  enter details about an applicant (name,
birthday, email, etc.), and then the values are stored in the user's session.

When the user first submits the form, the applicant details are stored correctly
in the session.

However, on all subsequent page views, the application crashes with a weird
error.

So far, the only way you've found to make the error go away is to delete the
browser's session cookie, or to clear out the session contents in the database.

**Your goal is to track down the root cause of the bug, and fix it.**

# Installation
This exercise is compatible with Python 2.7, 3.4, 3.5 and 3.6.

1. Clone this repo and check out the `develop` branch.
2. [Create a virtualenv for the project.](https://realpython.com/blog/python/python-virtual-environments-a-primer/#Using.virtual.environments)
3. Run `pip install -r requirements.txt`
4. Run `python manage.py migrate`

# Reproducing the Bug
**Important:**  If you are sure you installed the app correctly, but you get
the wrong error when you try to reproduce the bug, please contact us before
continuing the exercise!

## Browser
1. Run `python manage.py runserver`
2. Open <http://localhost:8000/applicant>.
3. Fill out the form fields and submit the form.
4. Reload the page.
5. You will get a weird error:

    > ### TypeError at /applicant
    > strptime() argument 1 must be string, not datetime.date

The only way to get the page to load again is to clear your session cookie or
delete the session from the database.

## Unit tests
1. Run `python manage.py test`
2. You will get two test errors when `ApplicantTestCase` runs (same error both
  times):

    > TypeError: strptime() argument 1 must be string, not datetime.date

## Hints
- This exercise has an easy solution and a hard solution.  The easy solution
  masks the real problem; the hard solution actually fixes it.
- Don't stress out about finding the hard solution within the time limit.
  Showcasing good technique and being on the right track when time runs out will
  get a better result than randomly stumbling upon the correct answer.  If you
  do find the hard solution, that's awesome, but we're more interested in seeing
  _how_ you found it, not just _that_ you found it.
