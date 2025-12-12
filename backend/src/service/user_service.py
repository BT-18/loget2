from repository.user_repo import *
from model.user import *
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
import pyotp
import mariadb

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
    
    def add_user(self, email: str, password: str, role: str, totp: str, role_claim: str) -> str:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_
            totp (str): _description_
        """
        if role_claim != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            user = User(email=email, password=password, role=role, totp=totp)
            self.user_repo.add_user(user)
            return "USER_ADDED"
        except mariadb.IntegrityError as e:
            return e.msg
        
    def delete_user(self, email: str, role_claim: str) -> str:
        """
        Service method to delete a user by email
        Args:
            email (str): the email of the user to delete
        Returns: A status message
        """
        if role_claim != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            self.user_repo.delete_user(email)
            return "USER_DELETED"
        except mariadb.Error as e:
            return e.msg
                    
    def update_totp(self, email: str, identity: str, role_claim: str) -> str:
        """
        Service method to update the TOTP key for a user
        Args:
            email (str): the email of the user to update
            totp (str): the new TOTP key
        Returns: Nothing
        """
        if identity != email and role_claim != "admin":
            return "AUTHORIZATION_FAILED"
        else:
            totp = pyotp.random_base32()
            self.user_repo.update_totp(email, totp)
            return f"TOTP_UPDATED {totp}"
        
    def update_email(self, old_email: str, new_email: str, identity: str, role_claim: str) -> str:
        """
        Service method to update the email of a user
        Args:
            old_email (str): the current email of the user
            new_email (str): the new email to set
            identity (str): the identity of the user making the request
        Returns: Nothing
        """
        if identity != old_email and role_claim != "admin":
            return "AUTHORIZATION_FAILED"
        else:
            self.user_repo.update_email(old_email, new_email)
            return "EMAIL_UPDATED"
        
    def update_password(self, email: str, new_password: str, identity: str, role_claim: str) -> str:
        """
        Service method to update the password of a user
        Args:
            email (str): the email of the user to update
            new_password (str): the new password to set
        Returns: Nothing
        """
        if identity != email and role_claim != "admin":
            return "AUTHORIZATION_FAILED"
        else:
            self.user_repo.update_password(email, new_password) 
            return "PASSWORD_UPDATED"
        
    def authenticate(self, email: str, password: str) -> str:
        user = self.get_user_by_email(email)
        print("User: " , user)
        if user is None:
            return "AUTH_FAILED"
        valid_password = user.get_password()
        totp = user.get_totp()

        print("password:", password, "valid_password:", valid_password)
        
        role = user.get_role()
        if password == valid_password:
            print("totp:", totp)
            if totp is not None:
                
                return "TOTP_REQUIRED"
            else:
                if role is not None:
                    if role == "admin":
                        additional_claims = {"role": "admin"}
                    else:
                        additional_claims = {"role": "user"}
                    return create_access_token(identity=email, additional_claims=additional_claims)
                else:
                    return "ERROR"
        else:
            return "AUTH_FAILED"
        
        
    def check_totp(self, email: str, password: str, totp: str) -> str:
        user = self.get_user_by_email(email)
        if user is None:
            return "AUTH_FAILED"
        valid_password = user.get_password()
        role = user.get_role()
        
        if password == valid_password:
            userTotp = user.get_totp()
            if userTotp is not None:
                totp_obj = pyotp.TOTP(userTotp)
                current_code = totp_obj.now()
                if current_code == totp:
                    if role is not None:
                        if role == "admin":
                            additional_claims = {"role": "admin"}
                        else:
                            additional_claims = {"role": "user"}
                        return create_access_token(identity=email, additional_claims=additional_claims)
                    else:
                        return "ERROR"
                else:
                    return "TOTP_FAILED"
            else:
                return "ERROR"
        else:
            return "AUTH_FAILED"