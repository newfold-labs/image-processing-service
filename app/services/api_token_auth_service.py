from fastapi import HTTPException, Header, Depends
import os

class ApiTokenAuthService:
    @staticmethod
    def get_api_auth_token():
        # Get token from environment variable
        token_env = os.getenv("API_AUTH_TOKEN", "invalid")
        return token_env.strip()
    
    @staticmethod
    def verify_token(authorization: str = Header(None)) -> bool:
        """
        Verify the Authorization header contains a valid token
        
        Expected header format: "Bearer api-token"
        """
        if not authorization:
            raise HTTPException(
                status_code=401, 
                detail="Authorization header missing"
            )
        
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401, 
                detail="Invalid authorization format. Use: Bearer <token>"
            )
        
        token = authorization.replace("Bearer ", "")
        valid_token = ApiTokenAuthService.get_api_auth_token()
        
        if token != valid_token:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        return True