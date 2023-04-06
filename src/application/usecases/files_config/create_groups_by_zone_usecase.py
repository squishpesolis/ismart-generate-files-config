import typing
from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils
from src.domain.dog_fact import DogFactEntity


class CreateGroupsByZoneUseCase(GenericUseCase):
    def __init__(self) -> None:
        pass

    def execute(self) -> typing.Iterable[DogFactEntity]:
        try:
            return "Archivo Creado en la ruta"
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Cannot get all dog facts", exception)

    