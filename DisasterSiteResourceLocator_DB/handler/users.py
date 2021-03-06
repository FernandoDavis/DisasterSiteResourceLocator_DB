from flask import jsonify
from dao.users import UsersDAO


class UsersHandler:

    def build_users_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['uname'] = row[1]
        result['upass'] = row[2]
        result['first_name'] = row[3]
        result['last_name'] = row[4]
        return result

    def login(self, form):
        if form and len(form) == 3:
            uname = form['uname']
            upass = form['upass']
            utype = form['utype']
            if uname and upass and utype:
                dao = UsersDAO()
                result = dao.confirmUser(uname, upass, utype)
                if isinstance(result, int):  # If result is the id then log-in was successful for the user.
                    return "Log-in successful.", 201
        return "Log-in unsuccessful. User or password did not match.", 404

    def signup(self, form):
        if form and (len(form) == 5):
            uname = form['uname']
            upass = form['upass']
            first_name = form['first_name']
            last_name = form['last_name']
            utype = form['utype']
            result = None
            if uname and upass and utype and first_name and last_name:  # Check if: admin or (consumer/supplier)
                # Create consumer/supplier/administrator
                if utype == "Consumer" or utype == "Supplier":
                    dao = UsersDAO()
                    result = dao.addRegularUser(utype, uname, upass, first_name, last_name)
                elif utype == "Administrator":
                    dao = UsersDAO()
                    result = dao.addAdminUser(utype, uname, upass, first_name, last_name)
            if result:  # If result has a value then the user was correctly added to the application.
                return "Sign-up successful.", 201
        return jsonify(Error="Malformed post request")

    def getAllUsers(self):
        dao = UsersDAO()
        user_list = dao.getAllUsers()
        result_list = []
        for row in user_list:
            result = self.build_users_dict(row)
            result_list.append(result)
        return jsonify(Users=result_list)

    def getUserById(self, uid):
        dao = UsersDAO()
        row = dao.getUserById(uid)
        if not row:
            return jsonify(Error="User Not Found"), 404
        else:
            result = self.build_users_dict(row[0])
        return jsonify(User=result)

    def searchUsers(self, args):
        uname = args.get("uname")
        first_name = args.get("first_name")
        last_name = args.get("last_name")
        dao = UsersDAO()
        user_list = []
        if len(args) == 3 and uname and first_name and last_name:
            dao = UsersDAO()
            user_list = dao.getUserByUserAndFirstAndLastname(uname, first_name, last_name)
        elif len(args) == 2 and uname and first_name:
            dao = UsersDAO()
            user_list = dao.getUserByUserAndFirstname(uname, first_name)
        elif len(args) == 2 and uname and last_name:
            dao = UsersDAO()
            user_list = dao.getUserByUserAndLastname(uname, last_name)
        elif len(args) == 2 and first_name and last_name:
            dao = UsersDAO()
            user_list = dao.getUserByFirstAndLastname(first_name, last_name)
        elif len(args) == 1 and uname:
            dao = UsersDAO()
            user_list = dao.getUserByUsername(uname)
        elif len(args) == 1 and first_name:
            dao = UsersDAO()
            user_list = dao.getUserByFirstname(first_name)
        elif len(args) == 1 and last_name:
            dao = UsersDAO()
            user_list = dao.getUserByLastname(last_name)
        else:
            return jsonify(Error="Malformed search string."), 400

        result_list = []
        for row in user_list:
            result = self.build_users_dict(row)
            result_list.append(result)
        return jsonify(Users=result_list)

    # def insertUser(self, uid): Im a bit too sleepey, I need to check for type of user with utype, no touchy pls
