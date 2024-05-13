from facade_service import app_facade, api_facade, consul_client
from facade_service.controllers.routes import FacadeService


api_facade.add_resource(FacadeService, '/api/v1/facade_service/<string:operation>')


if __name__ == "__main__":
    service_id = f"facade_service"
    consul_client.agent.service.register("facade_service", port=8080, service_id=service_id)
    app_facade.run(port=8080, processes=4, threaded=False)
