import os ,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import security_manager


def test_decoder(token: str):
    response = security_manager.decode_token(token)
    print(response)
    
def test_refresh_token(token: str):
    print("refresh token payload")
    response = security_manager.refresh_access_token(token)
    print(response)

def access_token_test(token: str):
    response = security_manager.create_access_token(token)
    print(response)






def main():
    print("Starting test security")
    choice = input("Enter your choice: ")
    print("1:Decode Token")
    print("2:refresh Token")
    print("3:access Token")

