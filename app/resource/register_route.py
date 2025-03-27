from app.resource.user.register import UserRegister
from app.resource.user.login import UserLogin
from app.resource.user.logout import UserLogout
from app.resource.user.account import UserAccount
from app.resource.link.link import LinkCreate, LinkDelete

def connect_roat_to_api(api):
    api.add_resource(UserRegister, '/link/register-user')
    api.add_resource(UserLogin, '/link/login')
    api.add_resource(UserLogout, '/link/logout')
    api.add_resource(UserAccount, '/link/account')
    api.add_resource(LinkCreate, '/link/create-link')
    api.add_resource(LinkDelete, '/link/delete-link')