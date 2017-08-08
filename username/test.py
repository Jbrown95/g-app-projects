from google.appengine.ext import db

class Person(db.Model):
  name = db.StringProperty()
  age = db.IntegerProperty()

# We use a unique username for the Entity's key.
amy = Person(key_name='amym', name='Amy', age=48)
amy.put()
Person(key_name='bettyd', name='Betty', age=42).put()
Person(key_name='charliec', name='Charlie', age=32).put()
Person(key_name='charliek', name='Charlie', age=29).put()
Person(key_name='eedna', name='Edna', age=20).put()
Person(key_name='fredm', name='Fred', age=16, parent=amy).put()
Person(key_name='georgemichael', name='George').put()

q = Person.gql("SELECT * FROM Person WHERE age >= 18 AND age <= 35")
for i in q:
    print i.all()
