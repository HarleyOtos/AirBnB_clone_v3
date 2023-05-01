#!/usr/bin/python
"""Unittests for DBStorage class of AirBnb_Clone_v2"""
import unittest
import pep8
import os
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import MySQLdb


@unittest.skipIf(
       os.getenv('HBNB_TYPE_STORAGE') != 'db',
       "This test only work in DBStorage")
class TestDBStorage(unittest.TestCase):
    """this will test the DBStorage"""

    @classmethod
    def setUpClass(cls):
        """Tests"""
        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.user

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_DBStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """tests if all works in DB Storage"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_new(self):
        """test when new is created"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_dbtorage(self):
        """
        tests reload
        """
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except Exception:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except Exception:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)
    
    def test_db_storage_get(self):
        """Test the get() method of DBStorage."""
        storage = DBStorage()

        # Create a State object and add it to the session
        state = State(name="State")
        storage.new(state)
        storage.save()
        
        # Test retrieving the State object by ID
        result = storage.get(State, state.id)
        self.assertEqual(result, state)
        
        # Test retrieving a non-existent object
        result = storage.get(State, "invalid_id")
        self.assertIsNone(result)

    def test_db_storage_count(self):
        """Test the count() method of DBStorage."""
        storage = DBStorage()
        
        # Ensure count returns 0 initially
        self.assertEqual(storage.count(), 0)
        
        # Create some objects and save them to the database
        state1 = State(name="California")
        state2 = State(name="New York")
        city1 = City(name="San Francisco", state_id=state1.id)
        city2 = City(name="New York City", state_id=state2.id)
        user1 = User(name="Alice")
        user2 = User(name="Bob")
        amenity1 = Amenity(name="Wifi")
        amenity2 = Amenity(name="Pool")
        place1 = Place(name="Cozy apartment", city_id=city1.id, user_id=user1.id)
        place2 = Place(name="Luxury penthouse", city_id=city2.id, user_id=user2.id)
        review1 = Review(text="Great place", place_id=place1.id, user_id=user1.id)
        review2 = Review(text="Terrible place", place_id=place2.id, user_id=user2.id)
        
        objects = [state1, state2, city1, city2, user1, user2, amenity1, amenity2, place1, place2, review1, review2]
        
        for obj in objects:
            storage.new(obj)
            storage.save()
            
            # Count the total number of objects in the database
            total_count = sum(storage.count(cls) for cls in all_classes)
            
            # Ensure count returns the correct number of objects
            self.assertEqual(storage.count(), total_count)
            
            # Ensure count returns the correct number of objects for each class
            for cls in all_classes:
                self.assertEqual(storage.count(cls), storage.__session.query(eval(cls)).count())
                
                storage.close()

if __name__ == "__main__":
    unittest.main()
