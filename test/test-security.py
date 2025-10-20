from app.core.security import security_manager


response = security_manager.decode_token("token")
print(response)