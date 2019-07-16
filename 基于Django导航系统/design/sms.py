import sys
import re
from random import randint

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
from design import const

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# print(sys.path)

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

class SMS:
    def __init__(self,sign_name,template_code):
        self.__business_id = uuid.uuid1()
        self.sign_name = sign_name  #签名
        self.template_code = template_code  #模板代码

    #发送短信
    def send_sms(self, phone_numbers,  template_param):
        template_param = "{\"code\":\"" + str(template_param) + "\"}"
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(self.template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(self.__business_id)

        # 短信签名
        smsRequest.set_SignName(self.sign_name)

        # 数据提交方式
        # smsRequest.set_method(MT.POST)

        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = acs_client.do_action_with_exception(smsRequest)

        # TODO 业务处理
        # print(smsResponse)
        return smsResponse

if __name__ == "__main__":
    sms = SMS('明天是个好日子','SMS_151547936')

    while 1:
        phone = input("请输入你的手机号：")
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d|178)\d{8}$')
        if not phone_pat.match(phone):
            print("手机号错误")
        else:
            break
    num = randint(1000, 9999)  #验证码
    sms.send_sms(phone, num)

    #验证码验证
    data = int(input("请输入你的验证码："))

    if num == data:
        print("验证成功")
    else:
        print("验证失败，30秒请重新验证！")