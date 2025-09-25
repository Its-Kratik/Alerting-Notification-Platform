from services.user_service import UserService
from services.team_service import TeamService

def seed(db):
    usr_srv, team_srv = UserService(db), TeamService(db)
    org = "org_001"
    eng = team_srv.create_team({"name":"Engineering","organization_id":org})
    admin = usr_srv.create_user({"name":"Admin","email":"admin@org.com",
                                 "team_id":eng.id,"organization_id":org,"is_admin":True})
    return {"org": org, "admin": admin}
