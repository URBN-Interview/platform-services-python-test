import unittest
from helpers.validator import validator
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase, gen_test
from pymongo import MongoClient

class TestHelperClass(unittest.TestCase):
    
    def test_upper(self):        
        self.assertEqual('foo'.upper(), 'FOO')

    def test_validateEmail(self):
        print("test_validateEmail Passed Valid Email. Return True. Test Case Passed")
        self.assertEqual(validator.validateEmail(self, "customer@gmail.com"), True)

    def test_invalidEmail(self):
        print("test_invalidEmail Passed Invalid Email. Return False. Test Case Passed")
        self.assertEqual(validator.validateEmail(self, "customer"), False)   

    def test_NoEmail(self):
        print("test_NoEmail Passed No Email. Return False. Test Case Passed")
        self.assertEqual(validator.validateEmail(self, ""), False)      

    def test_dbcollection(self):            
        print("test_dbcollection")        
        #client = MongoClient("mongodb", 27017)
        HOST = 'localhost'
        PORT = 27017
        import socket
        sock = None
        try:
            sock = socket.create_connection((HOST, PORT),timeout=1) # one second        
            import pymongo
            conn = pymongo.MongoClient(HOST, PORT)
            print(conn.admin.command('ismaster'))
            db = conn["Rewards"]
            rewards = list(db.rewards.find({}, {"_id": 0}))
            print("test_Rewards one entry in db with 5% off purchase. Test Case Passed")
            self.assertIn("5% off purchase", rewards)      
        except socket.error as err:
            print("except")    
            raise EnvironmentError("Can't connect to MongoDB at {host}:{port} because: {err}".format(**locals()))
        finally:
            if sock is not None:
                sock.close()
                 
class TestRewardsHandler(AsyncTestCase):    
    def test_lower(self):        
        print("test_lower")
        self.assertEqual('FOO'.lower(), 'foo')

    @gen_test
    async def test_Customer_Rewards(self):        
        client = AsyncHTTPClient(self.io_loop)
        response = await client.fetch("http://localhost:7050/customer_rewards")
        print("test_Customer_Rewards one entry in db with customer01@gmail.com. Test Case Passed")        
        self.assertIn("customer01@gmail.com", response.body.decode())    

    @gen_test
    async def test_Rewards(self):
        print("test_http_fetch")
        client = AsyncHTTPClient(self.io_loop)
        response = await client.fetch("http://localhost:7050/rewards")
        print("test_Rewards one entry in db with 5% off purchase. Test Case Passed")  
        self.assertIn("5% off purchase", response.body.decode())        

if __name__ == '__main__':
    unittest.main()  


