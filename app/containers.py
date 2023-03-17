from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from logging import Logger
from .db import DbClient
from . import services
from .settings import CONN_STRING
from .services import ValidationService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[".views"])
    db_client = providers.Factory(DbClient, conn_string=CONN_STRING)
    validation_service = providers.Factory(services.ValidationService)




@inject
def main(validation_service: ValidationService = Provide[Container.validation_service],
         db_client: DbClient = Provide[Container.db_client]) -> None:
    pass


if __name__ == '__main__':
    container = Container()
    container.config.conn_string.from_env('CONN_STRING', required=True)
    container.wire(modules=[__name__])

    main()

