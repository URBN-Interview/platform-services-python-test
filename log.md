# Init
- created repo and branch
- launched images from docker files and verified initial endpoint and UI are able to load properly

# Review
- customer data is hardcoded on html file
- data is coming from a form that does not have a name at this time
- looking through db there does not appear to be a table for customer data

# Reflection
- design decision - what would be the best user experience for percentage towards progress? ssee customer handler for more notes at the point that this decision was made
- errors so far are generally handled through logic and mongodb, definitely need to test if possible

# Engineering notes
**1** customer_handler - percntage progress

  - I am calculating this as progress relative to current level so 100 is 0% to 200 because the user would see different percentages for the same progress as different levels (i should change this later but i will leave the calculation commented out)
  - Maybe i can make this into a visual experience bar on the front which would justify this decision as it would be better for an exp bar to start at 0

**2** Admin endpoint

  - Admin endpoint could be updated to parse query in the url to add more GET functionality (customer data, review data, purchase details and metrics)
  - viewing all customer data would be best to only be accessible for admins

**3** Sample Data

  - Added a file in handlers to show expected output, helpful for frontend integration


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
