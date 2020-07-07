import os


async def get_extension_models():
    l = []
    list_of_files = [x for x in os.listdir("/code/external_modules/") if x not in ['__init__.py', '__pycache__']]
    for m in list_of_files:
        # Check if model not empty
        extension_model_files = [
            x for x in os.listdir(f"/code/external_modules/{m}/models") if x not in ['__init__.py', '__pycache__']
        ]
        if len(extension_model_files) > 0:
            l.append(f"external_modules.{m}.models")
    return l