from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    '''fast dfs文件存储类'''

    def _open(self, name, mode='eb'):
        '''打开文件时使用'''
        pass

    def _save(self, name, content):
        '''保存文件时使用'''
        # content 包含文件内容的File对象
        client = Fdfs_client('./utils/fdfs/client.conf')

        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            raise Exception('上传到fast dfs失败')

        file_name = res.get('Remote file_id')
        return file_name

    def exists(self, name):
        '''Django判断文件是否可用'''
        return False  # 可用于新文件
