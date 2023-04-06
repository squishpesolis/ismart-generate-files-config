import typing
from fastapi import APIRouter,File, UploadFile
from fastapi_injector import Injected

from src.application.usecases.utils.tranform_file_to_dataframe_usecase import TransformFileToDataFrameUseCase
from src.application.usecases.utils.transform_dataframe_to_dict_usecase import TransformDataFrameToDictUseCase
from src.application.usecases.utils.transform_dict_to_json_usecase import TransformDictToJsonUseCase
from src.application.usecases.groups_ismart.create_groups_switch_usecase import CreateGroupsSwitchUseCase 
from src.adapter.api.shared.api_error_handling import ApiErrorHandling
from src.adapter.spi.repositories_factory import RepositoriesFactory


router = APIRouter()


@router.post("/")
async def grupos_config_file_facts(file: UploadFile, factory: RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        

        tranform_file_to_dataframe_usecase:TransformFileToDataFrameUseCase =  TransformFileToDataFrameUseCase(file, 'Entidades')
        dataframe = tranform_file_to_dataframe_usecase.execute()

        #transform_dataframe_to_dict_usecase: TransformDataFrameToDictUseCase = TransformDataFrameToDictUseCase(dataframe)
        #dict_data_config_ismart = transform_dataframe_to_dict_usecase.execute()

        create_groups_switch_usecase: CreateGroupsSwitchUseCase = CreateGroupsSwitchUseCase(dataframe)
        create_groups_switch_usecase.execute()

        """ dog_facts_repository: DogFactsRepositoryAbstract = factory.get_repository(
            "dog_fact_repository")
        dog_fact_presenter_mapper: DogFactPresenterMapper = DogFactPresenterMapper()

        get_all_dog_facts_usecase: GetAllDogFactsUseCase = GetAllDogFactsUseCase(
            dog_facts_repository)
        dog_facts = get_all_dog_facts_usecase.execute()

        facts: typing.List[DogFactPresenter] = []
        for data in dog_facts:
            facts.append(dog_fact_presenter_mapper.to_api(data))

        return facts """
        return {"filename": file.filename}
    except Exception as exception:
        raise ApiErrorHandling.http_error("Unexpected error al crear archivos de configuración", exception)


