from cornice_swagger import CorniceSwagger, cornice_enable_openapi_view
from cornice.service import get_services
from cornice import Service

swagger = Service(name='OpenAPI',
                  path='/__api__',
                  description="OpenAPI documentation")


@swagger.get()
def openAPI_spec(request):
    doc = CorniceSwagger(get_services(['flights']))
    my_spec = doc.generate('MyAPI', '1.0.0')
    return my_spec
