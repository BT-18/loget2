from repository.user_repo import *
from model.user import *
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
import pyotp

class UserService:
    def __init__(self, databasePool: Pool):
        self.user_repo = UserRepo(databasePool)
        
    def get_user_by_email(self, email: str):
        """
        Service method to get a user by email
        Args:
            email (str): the email of the user to retrieve
        Returns: A User object if found, None otherwise
        """
        return self.user_repo.get_user_by_email(email)
    
    def add_user(self, email: str, password: str, totp: str) -> None:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_
            totp (str): _description_
        """
        user = User(email=email, password=password, totp=totp)
        self.user_repo.add_user(user)
        
    def update_totp(self, email: str, totp: str) -> None:
        """
        Service method to update the TOTP key for a user
        Args:
            email (str): the email of the user to update
            totp (str): the new TOTP key
        Returns: Nothing
        """
        self.user_repo.update_totp(email, totp) 
        
    def update_email(self, old_email: str, new_email: str) -> None:
        """
        Service method to update the email of a user
        Args:
            old_email (str): the current email of the user
            new_email (str): the new email to set
        Returns: Nothing
        """
        self.user_repo.update_email(old_email, new_email)
        
    def update_password(self, email: str, new_password: str) -> None:
        """
        Service method to update the password of a user
        Args:
            email (str): the email of the user to update
            new_password (str): the new password to set
        Returns: Nothing
        """
        self.user_repo.update_password(email, new_password) 
        
        
    def authenticate(self, email: str, password: str) -> str:
        user = self.get_user_by_email(email)
        print("User: " , user)
        if user is None:
            return "ERROR"
        valid_password = user.get_password()
        totp = user.get_totp()

        print("password:", password, "valid_password:", valid_password)
        if password == valid_password:
            print("totp:", totp)
            if totp is not None:
                
                return "TOTP_REQUIRED"
            else:
                return create_access_token(identity=email)
        else:
            return "AUTH_FAILED"
        
        
    def check_totp(self, email: str, password: str, totp: str) -> str:
        user = self.get_user_by_email(email)
        if user is None:
            return "ERROR"
        valid_password = user.get_password()
        
        if password == valid_password:
            userTotp = user.get_totp()
            if userTotp is not None:
                totp_obj = pyotp.TOTP(userTotp)
                current_code = totp_obj.now()
                if current_code == totp:
                    return create_access_token(identity=email)
                else:
                    return "TOTP_FAILED"
            else:
                return "ERROR"
        else:
            return "AUTH_FAILED" 