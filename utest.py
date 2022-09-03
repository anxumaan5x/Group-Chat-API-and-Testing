import names
try:
    from app import app
    import unittest

except Exception as e:
    print("Some modules are missing {}".format(e))


class FlaskTest(unittest.TestCase):

    username=names.get_first_name()
    groupname=names.get_first_name()

    #index page

    #check for 200 response
    def test_index(self):
        tester=app.test_client(self)
        response = tester.get('/')
        statuscode=response.status_code
        self.assertEqual(statuscode,200)

    #check if response if JSON
    def test_index_content(self):
        tester=app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.content_type, "application/json")

    #Check if message field is there or not
    def test_index_data(self):
        tester=app.test_client(self)
        response = tester.get('/')
        self.assertTrue(b'message' in response.data)

    #--------------------------------------------------------
    # Testing Signup API and checking status code, response type and success fields
    
    def test_signup(self):
        tester=app.test_client(self)
        print("trying to sign up with username, password: ", self.username, "password")
        response = tester.post('/api/v1/signup', json={"username": self.username, "password": "password"})
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)


    #--------------------------------------------------------
# Testing Login API and checking status code, response type and success fields
    def test_login(self):
        tester=app.test_client(self)
        print("trying to login with username, password: ", self.username, "password")
        response = tester.post('/api/v1/login', json={"username": self.username, "password": "password"})
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)


   #--------------------------------------------------------
# Testing Create Admin User API and checking status code, response type and success fields
    def test_create_user(self):
        tester=app.test_client(self)
        testuser=names.get_first_name()
        print("trying to add user with username, password: ", testuser, "password")
        response = tester.post('/api/v1/add_user', json={"username": testuser})
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)

     #--------------------------------------------------------
# Testing Change Password API and checking status code, response type and success fields
    def test_change_password(self):
        tester=app.test_client(self)
        print("trying to change password for user with username, password: ", self.username, "password")
        response = tester.post('/api/v1/change_password', json={"password": "password", 'new_password': 'new_password'})
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)

    #--------------------------------------------------------
# Testing Create Group API and checking status code, response type and success fields
    def test_create_group(self):
        tester=app.test_client(self)
        print("trying to create group with name: ", self.groupname)
        response = tester.post('/api/v1/create_group', json={"name": self.groupname})
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)

    #--------------------------------------------------------
# Testing Adding members API and checking status code, response type and success fields
    def test_add_members_group(self):
        tester=app.test_client(self)
        print("trying to add_members with id 1 to group 1")
        response = tester.post('/api/v1/add_members/1/1', json={"name": self.groupname})
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)

    #--------------------------------------------------------
# Testing Search/View Groups API and checking status code, response type and success fields
    def test_search_groups(self):
        tester=app.test_client(self)
        print("trying to search/view groups")
        response = tester.post('/api/v1/search_groups')
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)



    #--------------------------------------------------------
# Testing Sending message API and checking status code, response type and success fields
    def test_send_message_group(self):
        tester=app.test_client(self)
        print("trying to send random message to group 1")
        message=names.get_full_name()
        response = tester.post('/api/v1/send_message/1', json={"message": message})
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)

    #--------------------------------------------------------
# Testing like API and checking status code, response type and success fields
    def test_like_message(self):
        tester=app.test_client(self)
        print("trying to like message with id 1")
        response = tester.post('/api/v1/like_message/1')
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)

    #--------------------------------------------------------
# Testing View Messages in group API and checking status code, response type and success fields
    def test_view_message(self):
        tester=app.test_client(self)
        print("trying to view messages in group_id 1")
        response = tester.post('/api/v1/view_message/1')
        statuscode=response.status_code
        self.assertEqual(statuscode,200) and self.assertEqual(response.content_type, "application/json") and self.assertTrue(b'success' in response.data)

if __name__=="__main__":
    unittest.main()