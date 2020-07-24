#!/usr/bin/env python
# -*- coding: utf-8 -*-

from atlassian import Confluence
from pprint import pprint
import time

class ConfluenceService():
    def __init__(self, URL, USERNAME, PASSWD):
        """
         Login in
        :param URL: input service website
        :type URL: str
        :param USERNAME: input username
        :type USERNAME: str
        :param PASSWD: input password
        :type PASSWD: str
        :return: None
        """
        try:
            self.confluence = Confluence(
                url=URL,
                username=USERNAME,
                password=PASSWD
            )
        except:
            print('login failed!')
            return False

    def get_body(self, SPACE):
        """
        Gets the content of the article in the space
        :param SPACE: the space that Page is in
        :type SPACE: str
        :return: msg_body as dict
        """
        self.source_space = SPACE
        all_page = self.confluence.get_all_pages_from_space(SPACE, start=0, status=None, expand=None,
                                                            content_type='page')

        msg_body = {}
        child_parent = {}
        for i in all_page:
            child = self.confluence.get_page_child_by_type(i['id'],type='page', start=None, limit=None)

            body = self.confluence.get_page_by_id(i['id'], "body.view", status=None, version=None)
            msg_body[body['id']] = {

            }

            msg_body[body['id']]['title'] = body['title']
            msg_body[body['id']]['body'] = body['body']['view']['value']
            msg_body[body['id']]['type'] = body['type']
            child_parent[body['id']] = [j['id'] for j in child]

        for j, k in child_parent.items():
            for c in k:
                if c in child_parent[j]:
                    try:
                        msg_body[c]['parent_title'] = msg_body[j]['title']
                        print(msg_body[c]['title'] ,'\t\t\t\t\t\t\t\t', msg_body[c]['parent_title'])
                    except:
                        pass
        return msg_body

    def create_body(self, msg_body, target_space):
        """
        Gets the content of the article in the space
        :param msg_body: input msg_body {'title':'','body':''}
        :type msg_body: dict
        :param target_space: input space name
        :type target_space: str
        :return: None
        """
        new_parent_msg = {

        }

        for _id, msg in msg_body.items():
            if msg.get('title') == self.source_space or msg.get('parent_title')==None:

                for i in range(10):
                    try:
                        status = self.confluence.create_page(
                            space=target_space,
                            title=msg['title'],
                            body=msg['body'],
                        )
                        time.sleep(1)
                        new_id = self.confluence.get_page_id(target_space, msg['title'])
                        new_parent_msg[msg['title']] = new_id
                        break
                    except Exception as e:
                        time.sleep(3)
                        print(e.args)

            else:

                print(msg['title'], msg.get('parent_title'), new_parent_msg.get(msg.get('parent_title')))
                for i in range(10):
                    try:
                        status = self.confluence.create_page(
                            space=target_space,
                            title=msg['title'],
                            body=msg['body'],
                            parent_id=new_parent_msg.get(msg.get('parent_title'))
                        )
                        time.sleep(1)
                        new_id = self.confluence.get_page_id(target_space, msg['title'])
                        new_parent_msg[msg['title']] = new_id
                        break
                    except Exception as e:
                        time.sleep(3)
                        print(e.args)


def create_body_other_website(URL, USERNAME, PASSWD, msg_body, target_space, source_space):
    """
     Create pages on another service
    :param URL: input service website
    :type URL: str
    :param USERNAME: input username
    :type USERNAME: str
    :param PASSWD: input password
    :type PASSWD: str
    :param msg_body: input msg_body {'title':'','body':''}
    :type msg_body: dict
    :param target_space: input space name
    :type target_space: str
    :param source_space: Gets the Space name for the body
    :type source_space: str
    :return: None
    """
    try:
        confluence = Confluence(
            url=URL,
            username=USERNAME,
            password=PASSWD
        )
    except:
        print('login failed!')
        return False
    new_parent_msg = {

    }

    for _id, msg in msg_body.items():
        # print(msg['title'],'\t',msg.get('parent_title'))
        if msg.get('title') == source_space or msg.get('parent_title')==None:

            for i in range(10):
                try:
                    status = confluence.create_page(
                        space=target_space,
                        title=msg['title'],
                        body=msg['body'],
                        # type=msg['type']
                    )
                    time.sleep(1)
                    new_id = confluence.get_page_id(target_space, msg['title'])
                    new_parent_msg[msg['title']] = new_id
                    break
                except Exception as e:
                    time.sleep(3)
                    print(e.args)

        else:

            print(msg['title'], msg.get('parent_title'), new_parent_msg.get(msg.get('parent_title')))
            for i in range(10):
                try:
                    status = confluence.create_page(
                        space=target_space,
                        title=msg['title'],
                        body=msg['body'],
                        parent_id=new_parent_msg.get(msg.get('parent_title'))
                        # type=msg['type']
                    )
                    time.sleep(1)
                    new_id = confluence.get_page_id(target_space, msg['title'])
                    new_parent_msg[msg['title']] = new_id
                    break
                except Exception as e:
                    time.sleep(3)
                    print(e.args)


if __name__ == "__main__":

    source_space = 'xxxxxxx'
    URL = 'https://dwiki.daocloud.io/'
    USERNAME = 'xxxxxxxxxxx'
    PASSWD = 'xxxxxxxxxxxx'

    a = ConfluenceService(URL, USERNAME, PASSWD)
    msg= a.get_body(GET_BODY_SPACE)
    # a.create_body(msg, '~huifeng.tang')
    # create_body_other_website(URL, USERNAME, PASSWD, msg, target_space, source_space) 