import uvicorn
from fastapi import FastAPI

from .application_properties import ApplicationProperties, load_configuration
from .config.jackson_config import ApplicationJSONResponse
from .global_exception_handler import GlobalExceptionHandler

configuration = load_configuration()
properties = ApplicationProperties.load(configuration)
app = FastAPI(
    title=configuration["application"]["name"],
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    default_response_class=ApplicationJSONResponse,
    exception_handlers={Exception: GlobalExceptionHandler().handle_unexpected},
)
app.state.properties = properties


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=int(configuration["server"]["port"]))


if __name__ == "__main__":
    main()
