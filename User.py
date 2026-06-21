class User:
    def __init__(self,name,username,password):
        self._id = ""
        self.name = name
        self.username = username
        self.password = password
        
    def checkName(self):
        if(self.name != "" and len(self.name) >= 5):
            return True
        return False
    
    def checkUsername(self,users):
        if(self.username != "" and len(self.username) >= 5):
            for user in users:
                if(user["username"] == self.username):
                    return False
        else:
            return False
        return True
    
    def checkPassword(self):
        if(self.password != "" and len(self.password) >= 8):
            return True
        return False
    
    def createId(self,role,users):
        count = 0
        if(role == "Customer"):
            for user in users:
                if (user["_id"])[0] == "c":
                    count += 1
                
            self._id = "c" + str(count+1)
        elif(role == "Manager"):
            for user in users:
                if (user["_id"])[0] == "m":
                    count += 1
                
            self._id = "m" + str(count+1)