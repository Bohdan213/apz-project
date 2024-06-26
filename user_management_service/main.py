from user_management_service import app_user_management, api_user_management, consul_client, db
from user_management_service.controllers.routes import UserManagementService


api_user_management.add_resource(UserManagementService, '/api/v1/user_management_service/<string:operation>')

with app_user_management.app_context():
    db.create_all()

if __name__ == "__main__":
    service_id = f"user_management_service"
    consul_client.agent.service.register("user_management_service", port=8000, service_id=service_id)
    app_user_management.run(port=8000)
