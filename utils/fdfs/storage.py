from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    '''fast dfs文件存储类'''

    def __init__(self, client_conf=None, base_url=None):
        if client_conf == None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url == None:
            base_url = settings.FDFS_URL
        self.base_url = base_url


    def _open(self, name, mode='eb'):
        '''打开文件时使用'''
        pass

    def _save(self, name, content):
        '''保存文件时使用'''
        # content 包含文件内容的File对象
        client = Fdfs_client(self.client_conf)

        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            raise Exception('上传到fast dfs失败')

        file_name = res.get('Remote file_id')
        return file_name

    def exists(self, name):
        '''Django判断文件是否可用'''
        return False  # 可用于新文件

    def url(self, name):
        '''返回访问文件的url路径'''
        return self.base_url + name
