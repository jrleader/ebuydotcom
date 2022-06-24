from tblib.service import Service

from random import choice # choice()会返回一个列表、元组或字符串的随机项

class EbUser(Service):

    @property
    def get_url(self):
        return self.app.config(['SERVICE_EBUSER']['ADDRESSES']) # 如果定义了多个地址，那么就随机挑选一个