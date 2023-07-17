import wifi_qrcode_generator.generator
from dotenv import dotenv_values


def router_info() -> dict:

    """
    configures router information that is placed inside your .env file.
    
    :return: dict - needed information for router
    """
    env_file_info = dotenv_values()
    return dict(env_file_info) 

def generate_code() -> None :

    """
    generates a qr code for everyone to connect to the local network and saves the file to project root directory as a png image.
    """
    connection_info = router_info()
    qr_code = wifi_qrcode_generator.generator.wifi_qrcode(
        ssid=connection_info['SSID'],
        hidden=False,
        authentication_type=connection_info['AUTH_TYPE'],
        password=connection_info['PASSWORD']
    )

    qr_code.make_image().save('wifi_qr.png')

if __name__ == '__main__':
    generate_code()