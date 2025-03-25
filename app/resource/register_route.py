from app.resource.user.register import UserRegister
from app.resource.user.login import UserLogin
from app.resource.user.logout import UserLogout
from app.resource.user.account import UserAccount

def connect_roat_to_api(api):
    api.add_resource(UserRegister, '/register-user')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(UserAccount, '/account')