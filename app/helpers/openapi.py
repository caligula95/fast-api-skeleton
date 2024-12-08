

from app.models.enums.tags import Tags


open_api = {
    'tags': [
        {
            "name": Tags.public,
            "description": "public available endpoint",
        },
        {
            "name": Tags.users,
            "description": "Manage users.",
            # "externalDocs": {
            #     "description": "Items external docs",
            #     "url": "https://fastapi.tiangolo.com/",
            # },
        },
    
    ],
    'app_title': "Backend API",
    'app_summary': "Backend API for application",
    'app_version': "V1",
    'app_description': """
            API helps you do awesome stuff. 🚀
            """,

}
