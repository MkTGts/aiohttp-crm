from app.web.utils import json_response, check_basic_auth
from app.web.app import View
from app.crm.models import User
import uuid
from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema
from app.crm.schemes import UserSchema, ListUsersResponseSchema, UserGetResponseSchema, UserAddSchema, UserGetRequestSchema
from app.web.schemes import OkResponseSchema


class AddUserView(View):
    @docs(
            tags=["crm"],
            summary="Add new user",
            description="Add new user to database"
    )
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = self.request["data"]
        user = User(email=data['email'], _id=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user)
        return json_response()


class ListUsersView(View):
    @docs(
            tags=["crm"],
            summary="List users",
            description="List users from database"
    )
    @response_schema(ListUsersResponseSchema, 200)
 
    async def get(self):
        '''        #print(self.request.headers.get("Authorization"))
                perem = self.request.headers["Authorization"]
                print(perem, type(perem))
                #print(type(self.request.headers("Authorization")))
'''
        if not self.request.headers.get("Authorization"):
            raise HTTPUnauthorized
        if not check_basic_auth(self.request.headers["Authorization"], 
                                username=self.request.app.config.username, password=self.request.app.config.password):
            raise HTTPForbidden
        
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [UserSchema().dump(user) for user in users]
        return json_response(data={"users": raw_users})
    

class GetUserView(View):
    @docs(
            tags=["crm"],
            summary="Get user",
            description="Get users from database"
    )
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get("Authorization"):
            raise HTTPUnauthorized
        if not check_basic_auth(self.request.headers["Authorization"], 
                                username=self.request.app.config.username, password=self.request.app.config.password):
            raise HTTPForbidden

        user_id = self.request.query["id"]
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(data={"user": {"email": user.email, "id": str(user._id)}})
        else:
            raise HTTPNotFound
