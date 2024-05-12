from planning_service import app_planning, api_planning, consul_client
from planning_service.controllers.routes import PlanningService


api_planning.add_resource(PlanningService, '/api/v1/planning_service')


if __name__ == "__main__":
    service_id = f"planning_service"
    consul_client.agent.service.register(service_id, port=8081, service_id=service_id)
    app_planning.run(port=8081)
