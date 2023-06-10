import typing
from fastapi import APIRouter,File, UploadFile
from fastapi_injector import Injected



from src.application.usecases.views_ismart.create_view_admin_dashboard_usecase   import CreateViewAdminDashboardUseCase



from src.adapter.api.shared.api_error_handling import ApiErrorHandling
from src.adapter.spi.repositories_factory import RepositoriesFactory



router = APIRouter()


@router.post("/")
async def generate_config_files_facts(file: UploadFile,configurar_con_entidades_demos: bool,factory: RepositoriesFactory = Injected(RepositoriesFactory)):
    try:
        

       


       
        create_views_usecase: CreateViewAdminDashboardUseCase = CreateViewAdminDashboardUseCase(file, configurar_con_entidades_demos)
        await create_views_usecase.execute()
        #create_groups_switch_usecase: CreateGroupsSwitchUseCase = CreateGroupsSwitchUseCase(dataframe)
        #

        return {"filename": file.filename}
    except Exception as exception:
        print(str(exception))
        raise ApiErrorHandling.http_error("Error al crear archivos de configuración", exception)


