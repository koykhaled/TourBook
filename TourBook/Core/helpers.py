from datetime import datetime


def upload_to(instance, file_name):
    file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + \
        "." + file_name.split('.')[-1]
    return instance.path+file_name
