from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI()
        params = { 'sender' : '',
                   'receptor': phone_number,
                   'message' :f'BLOGSPACE: your verification code {code}, edpired in 3 minutes' }
        response = api.sms_send(params)
        print(response)
    except APIException as err:
        print(err)
    except HTTPException as err:
        print(err)