#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: 1.0.0
@author: huifeng tang
@contact: huifeng.tang@daocloud.io
@time: 2020/7/17 10:30 AM
docs: https://atlassian-python-api.readthedocs.io/confluence.html
"""

from atlassian import Confluence
import time

class ConfluenceService():
    def __init__(self, confluence, source_space, target_space=None, limit=1000):
        """
        init func
        :param confluence: confluence
        :type confluence: class confluence
        :param source_space: Gets the Space name for the body
        :type source_space: str
        :param target_space: input space name
        :type target_space: str
        :param limit: 限制检索一个空间内文章的数量 默认为1000
        :type limit: int
        :return: None
        """
        self.confluence = confluence
        self.limit = limit
        if target_space:
            self.target_space = target_space

        self.new_parent_msg = {

        }
        self.source_space = source_space
        self.get_body(self.source_space)
        self.wrong_title = []
        if target_space:
            self.create_child_body(self.msg_body, target_space)

    def get_body(self, source_space):
        """
        Gets the content of the article in the space
        :param source_space: Gets the Space name for the body
        :type source_space: str
        :return: msg_body as dict
        """
        all_page = self.confluence.get_all_pages_from_space(source_space, start=0, status=None, expand=None, limit=self.limit,
                                                            content_type='page')
        msg_body = {}
        n = 0
        for i in all_page:
            n = 1 + n
            child = self.confluence.get_page_child_by_type(i['id'], type='page', start=None, limit=None)
            body = self.confluence.get_page_by_id(i['id'], "body.storage", status=None, version=None)
            msg_body[body['title']] = {

            }
            msg_body[body['title']]['id'] = i['id']


            msg_body[body['title']]['title'] = body['title']
            msg_body[body['title']]['type'] = body['type']
            msg_body[body['title']]['parent_title'] = self.confluence.get_parent_content_title(i['id'])
            msg_body[body['title']]['parent_id'] = self.confluence.get_parent_content_id(i['id'])
            msg_body[body['title']]['child_title'] = [j['title'] for j in child]
            msg_body[body['title']]['child_id'] = [j['id'] for j in child]

        print('num: ', n)

        self.msg_body = msg_body
        self.big_title = [i for i in self.msg_body.keys()][0]
        return msg_body

    def create_child_body(self, msg_body,target_space):
        """
         Create pages on another service
        :param msg_body: input msg_body {'title':'','body':''}
        :type msg_body: dict
        :param target_space: input space name
        :type target_space: str
        :return: None
        """
        Error_msg = []
        for title, msg in msg_body.items():
            try:
                _id = self.new_parent_msg.get(msg_body[title]['parent_title'])
            except:
                _id = None
            if title != self.big_title and _id == None:
                Error_msg.append(msg_body[title])
            else:
                try:
                    print(title,'\t\n|')
                    self.confluence.create_page(
                        space=target_space,
                        title=title,
                        body=self.confluence.get_page_by_title(self.source_space, title, expand="body.storage")['body']['storage']['value'],
                        parent_id=_id,
                        type=msg['type'],
                        representation='storage',
                    )
                    new_id = self.confluence.get_page_id(target_space, title)
                    self.new_parent_msg[title] = new_id
                except:
                    pass
                for title_child in msg['child_title']:
                    print('\t\t|   ', title_child)
                    if title_child:
                        try:
                            self.confluence.create_page(
                                space=target_space,
                                title=title_child,
                                body=self.confluence.get_page_by_title(self.source_space, msg_body[title_child]['title'], expand="body.storage")['body']['storage']['value'],
                                parent_id=self.confluence.get_page_id(target_space, title),
                                type=msg_body[title_child]['type'],
                                representation='storage',
                            )
                            new_id = self.confluence.get_page_id(target_space, title_child)
                            self.new_parent_msg[title_child] = new_id
                        except:
                            pass
        print("\n\n\n")
        for e_msg in Error_msg:

            print(self.confluence.get_page_by_id(e_msg['id'], "body.storage"))
            try:
                print("=================")
                print(e_msg['title'], '\t\n|')
                print(self.confluence.get_page_by_title(self.source_space,e_msg['title'], expand="body.storage")['body']['storage']['value'])
                self.confluence.create_page(
                    space=target_space,
                    title=e_msg['title'],
                    body=self.confluence.get_page_by_title(self.source_space, e_msg['title'], expand="body.storage")['body']['storage']['value'],
                    parent_id=self.new_parent_msg.get(e_msg['parent_title']),
                    type=e_msg['type'],
                    representation='storage',
                )
                # del msg_body[title]
                new_id = self.confluence.get_page_id(target_space, e_msg['title'])
                self.new_parent_msg[e_msg['title']] = new_id
            except:
                print('Wrong!!!!!')

def create_body_other_website(confluence, msg_body, source_space, big_title, target_space):
    """
     Create pages on another service
    :param confluence: confluence
    :type confluence: class confluence
    :param msg_body: input msg_body {'title':'','body':''}
    :type msg_body: dict
    :param source_space: Gets the Space name for the body
    :type source_space: str
    :param big_title: 首页空间的名字
    :type big_title: str
    :param target_space: input space name
    :type target_space: str
    :return: None
    """

    new_parent_msg = {

    }

    Error_msg = []
    for title, msg in msg_body.items():
        try:
            _id = new_parent_msg.get(msg_body[title]['parent_title'])
        except:
            _id = None
        if title != big_title and _id == None:
            Error_msg.append(msg_body[title])
        else:
            try:
                print(title, '\t\n|')
                confluence.create_page(
                    space=target_space,
                    title=title,
                    body=confluence.get_page_by_title(source_space, msg['title'],expand="body.storage")['body']['storage']['value'],
                    parent_id=_id,
                    type=msg['type'],
                    representation='storage',
                )
                new_id = confluence.get_page_id(target_space, title)
                new_parent_msg[title] = new_id
            except:
                pass
            for title_child in msg['child_title']:
                print('\t\t|   ', title_child)
                if title_child:
                    try:
                        confluence.create_page(
                            space=target_space,
                            title=title_child,
                            body=confluence.get_page_by_title(source_space, msg_body[title_child]['title'], expand="body.storage")['body']['storage']['value'],
                            parent_id=confluence.get_page_id(target_space, title),
                            type=msg_body[title_child]['type'],
                            representation='storage',
                        )
                        new_id = confluence.get_page_id(target_space, title_child)
                        new_parent_msg[title_child] = new_id
                    except:
                        pass
    print("\n\n\n")
    for e_msg in Error_msg:
        try:
            print("=================")
            print(e_msg['title'], '\t\n|')
            confluence.create_page(
                space=target_space,
                title=e_msg['title'],
                body=confluence.get_page_by_title(source_space, e_msg['title'], expand="body.storage")['body']['storage']['value'],
                parent_id=new_parent_msg.get(e_msg['parent_title']),
                type=e_msg['type'],
                representation='storage',
            )
            new_id = confluence.get_page_id(target_space, e_msg['title'])
            new_parent_msg[e_msg['title']] = new_id
        except:
            print('Wrong!!!!!')



def loop_update_confluence(target, source, target_space, source_space, limit=1000):
    for source_page in source.get_all_pages_from_space(source_space, start=0, status=None, expand=None, limit=limit,
                                                                content_type='page'):

        if target.is_page_content_is_already_updated(page_id=target.get_page_id(target_space, source_page['title']), body=source.get_page_by_title(source_space, source_page['title'], expand="body.storage")['body']['storage']['value']):
            print('=============is already updated===============')

        else:
            print('=============开始 更新============')
            # 判断 target内容是否需要更新
            target_page = target.get_page_by_title(target_space, source_page['title'], expand='body.storage')['body']['storage']['value']
            # 获取target的page内容
            target_id = target.get_page_id(target_space, source_page['title'])
            target_parent_id = target.get_page_id(target_space, target.get_parent_content_title(target_id))

            try:
                target.update_page(
                    page_id=target_id,
                    title=source_page['title'],
                    body=source.get_page_by_title(source_space, source_page['title'], expand="body.storage")['body']['storage']['value'],
                    parent_id=target_parent_id,
                    representation='storage'
                )
            except:
                pass


def dev_update(source, target, source_space, target_space):
    sourceservice = ConfluenceService(confluence=source, source_space=source_space)

    create_body_other_website(confluence=target, msg_body=sourceservice.msg_body, source_space=sourceservice.source_space, big_title=sourceservice.big_title, target_space=target_space)
    # 首先迁移文章，构造基本的文档关系网络
    while True:
        try:
            loop_update_confluence(target, source, target_space=target_space, source_space=source_space, limit=1000)
            # 进行同步工作
            time.sleep(1000)
        except:
            pass

if __name__ == "__main__":
    source_space = '~luping'
    target_space = '~huifeng.tang'
    URL_target = ''
    USERNAME_target = ''
    PASSWD_target = ''
    URL_source = ''
    USERNAME_source = ''
    PASSWD_source = ''
    target = Confluence(URL_target, USERNAME_target, PASSWD_target)
    source = Confluence(URL_source, USERNAME_source, PASSWD_source)
    dev_update(source, target, source_space, target_space)

    # target = Confluence(URL, USERNAME, PASSWD)
    # source = Confluence(URL, USERNAME, PASSWD)
    # a = ConfluenceService(source, source_space, target_space)
    # 若跨域迁移 则无需在 ConfluenceService 中指定 target_space 的内容
    # create_body_other_website(target, a.msg, a.source_space, target_space)
    # loop_update_confluence(target, source, target_space=target_space, source_space=source_space, limit=1000)
