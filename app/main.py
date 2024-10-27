import logging

from telegram.ext import Application as PTBAppLication, ApplicationBuilder
from settings.config import AppSettings
from app.infra.postgres.db import DataBase
from app.hendlers import HANDLERS
from app.core.users.repositories import UserRepository
from app.core.users.services import UserService

class Application(PTBAppLication):
    def __init__(self, app_settings: AppSettings, **kwargs):
        super().__init__(**kwargs)
        self._settings = app_settings
        self._register_handlers()
        self.database = DataBase(app_settings.POSTGRES_DSN)
        user_repository = UserRepository(database=self.database)
        self.user_service = UserService(repository=user_repository)
    @staticmethod
    async def initialize_dependencies(application: 'Application')->None:
        await application.database.initialize()

    @staticmethod
    async def shutdown_dependencies(application: 'Application') -> None:
        await application.database.shutdown()
    def run(self)->None:
        self.run_polling()

    def _register_handlers(self):
        for handler in HANDLERS:
            self.add_handler(handler)


def configure_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level= logging.INFO
    )
    logging.getLogger('httpx').setLevel(logging.WARNING)

def create_app(app_settings:...)->Application:
    appLication = (ApplicationBuilder().application_class(Application, kwargs={'app_settings':app_settings})
                   .application_class(Application,kwargs={'app_settings':app_settings})
                   .post_init(Application.initialize_dependencies)
                   .post_shutdown(Application.shutdown)
                   .token(app_settings.TELEGRAM_API_KEY.get_secret_value()).build())
    return appLication # type: ignore[arg-type]



if __name__=='__main__':
    configure_logging()
    settings = AppSettings()
    app = create_app(settings)
    app.run()