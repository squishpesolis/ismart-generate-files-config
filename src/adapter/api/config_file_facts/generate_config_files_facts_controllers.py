import typing
from fastapi import APIRouter,File, UploadFile
from fastapi_injector import Injected



from src.application.usecases.views_ismart.create_views_dashboard_usecase   import CreateViewsDashboardUseCase



from src.adapter.api.shared.api_error_handling import ApiErrorHandling
from src.adapter.spi.repositories_factory import RepositoriesFactory



router = APIRouter()


@router.post("/")
async def generate_config_files_facts(file: UploadFile, factory: RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        

       


       
        create_views_usecase: CreateViewsDashboardUseCase = CreateViewsDashboardUseCase(file)
        await create_views_usecase.execute()
        #create_groups_switch_usecase: CreateGroupsSwitchUseCase = CreateGroupsSwitchUseCase(dataframe)
        #

        return {"filename": file.filename}
    except Exception as exception:
        print(str(exception))
        raise ApiErrorHandling.http_error("Error al crear archivos de configuración", exception)


