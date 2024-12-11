# import os
# from dotenv import load_dotenv
# from fastapi import FastAPI, Depends, HTTPException, APIRouter
# from fastapi.security import OAuth2AuthorizationCodeBearer
# from httpx import AsyncClient
# from pydantic import BaseModel
# from starlette.middleware.sessions import SessionMiddleware
# from starlette.requests import Request
# from starlette.responses import RedirectResponse, JSONResponse
#
# from src.api.deps import get_current_user
#
# load_dotenv()
#
# router = APIRouter()
#
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# REDIRECT_URI = "http://localhost:8000/auth/callback"
# SECRET_KEY = os.getenv("SECRET_KEY")
#
# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
#     tokenUrl="https://oauth2.googleapis.com/token"
# )
#
#
# class User(BaseModel):
#     sub: str
#     name: str
#     given_name: str
#     family_name: str
#     picture: str
#     email: str
#     email_verified: bool
#     locale: str
#
#
# @router.get("/login")
# async def login():
#     google_auth_url = (
#         "https://accounts.google.com/o/oauth2/v2/auth"
#         "?response_type=code"
#         f"&client_id={GOOGLE_CLIENT_ID}"
#         f"&redirect_uri={REDIRECT_URI}"
#         "&scope=openid%20email%20profile"
#     )
#     return RedirectResponse(google_auth_url)
#
#
# @router.get("/auth/callback")
# async def auth_callback(request: Request):
#     code = request.query_params.get("code")
#     if not code:
#         raise HTTPException(status_code=400, detail="Authorization code not found")
#     token_url = "https://oauth2.googleapis.com/token"
#     token_data = {
#         "code": code,
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "redirect_uri": REDIRECT_URI,
#         "grant_type": "authorization_code",
#     }
#     async with AsyncClient() as client:
#         token_response = await client.post(token_url, data=token_data)
#         token_json = token_response.json()
#     if "error" in token_json:
#         raise HTTPException(status_code=400, detail=token_json["error"])
#     access_token = token_json["access_token"]
#     userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
#     headers = {"Authorization": f"Bearer {access_token}"}
#     async with AsyncClient() as client:
#         userinfo_response = await client.get(userinfo_url, headers=headers)
#         userinfo = userinfo_response.json()
#     if "error" in userinfo:
#         raise HTTPException(status_code=400, detail=userinfo["error"])
#     request.session["user"] = userinfo
#     return RedirectResponse("http://localhost:8000/docs")
#
#
# @router.get("/protected")
# async def protected_route(current_user: User = Depends(get_current_user)):
#     return current_user
#
#
# @router.get("/logout")
# async def logout(request: Request):
#     request.session.pop("user", None)
#     return JSONResponse({"message": "Successfully logged out"})
