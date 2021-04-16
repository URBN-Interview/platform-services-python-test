# Init
- created repo and branch
- launched images from docker files and verified initial endpoint and UI are able to load properly

# Review
- customer data is hardcoded on html file
- data is coming from a form that does not have a name at this time
- looking through db there does not appear to be a table for customer data
- django admin template, need to create database/api call models and then register them in the admin console
- looking through this code, it looks like we are using ./clients for models to obtain data from our api server, and not the built in django sqlite database that is used by django admin

# Reflection
- design decision - what would be the best user experience for percentage towards progress? ssee customer handler for more notes at the point that this decision was made
- errors so far are generally handled through logic and mongodb, definitely need to test if possible
- filtering a table with django would likely refresh the page, this experience would likely be improved by using javascript

# Engineering notes
**1** customer_handler - percntage progress

  - I am calculating this as progress relative to current level so 100 is 0% to 200 because the user would see different percentages for the same progress as different levels (i should change this later but i will leave the calculation commented out)
  - Maybe i can make this into a visual experience bar on the front which would justify this decision as it would be better for an exp bar to start at 0

**2** Admin endpoint

  - Admin endpoint could be updated to parse query in the url to add more GET functionality (customer data, review data, purchase details and metrics)
  - viewing all customer data would be best to only be accessible for admins
  - update i am realizing that this would likely only be used as an internal tool so you would likely need admin access to use this anyway, maybe will refactor this into the customers endpoint

**3** Sample Data

  - Added a file in handlers to show expected output, helpful for frontend integration

**4** POST request endpoint return

  - thought we could make it so the endpoint returns a fully updated output of the database would minimize the amount of requests to the db, BUT the ideal experience may also be to be able to prevent default on this field and not rerender automatically
  - in-person example of this is if an employee was bulk adding transactions at the end of the day or a customer brought in receipts after the fact and wanted to add their transactions to their account, it would take a really long time to reload the whole customer list on render every time you submit
  - going to return the customers updated data instead and display it on the page

**5** datatype on get method in the customer handlers

  - intiially had to switch this to json_utils to send a single ObjectId object through the response
  - switched it back to json so that i could force the document into an array so that Django can iterate through it in the html doc

**6** Interface

 - created user interface, emulating a dashboard that some could use to interact regularly with the rewards database
 - a section reponds to POST and search requests with an easy to read card that shows core information, this can be clicked to make it disappear (as a means of privacy of customer information on a screen)
 - added system dialogue to provide explanation for reload (bad form, bad email)

# Feature possibilities

- email customer their total
- undo add a sale
- daily cache to review and rollback activity


# Tornado Links

- https://www.tornadoweb.org/en/stable/guide/structure.html
- https://www.tornadoweb.org/en/stable/web.html#entry-points
- https://www.tornadoweb.org/en/stable/template.html
- https://www.tornadoweb.org/en/stable/web.html

# Pymongo Links
- https://www.w3schools.com/python/python_mongodb_find.asp
  - return only second param in db.coll.find()
- https://pymongo.readthedocs.io/en/stable/api/bson/json_util.html
- https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html

# Django Links
- https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
- https://pypi.org/project/requests/
- https://docs.djangoproject.com/en/3.2/topics/forms/
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
- https://docs.djangoproject.com/en/1.11/topics/class-based-views/generic-editing/
- https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/
