class LogoutUser:
    def __init__(self,blacklist_token):
        self.blacklist_token = blacklist_token
        
    def execute(self,refresh_token):
        self.blacklist_token.blacklist_token(refresh_token)
        