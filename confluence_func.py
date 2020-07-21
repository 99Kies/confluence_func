#!/usr/bin/env python
# -*- coding: gb2312 -*-

from atlassian import Confluence
from pprint import pprint
import time

class ConfluenceService():
    def __init__(self, URL, USERNAME, PASSWD, source_space, target_space=None):
        """
         Login in
        :param URL: input service website
        :type URL: str
        :param USERNAME: input username
        :type USERNAME: str
        :param PASSWD: input password
        :type PASSWD: str
        :param source_space: the space that Page is in
        :type source_space: str
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
        self.source_space = source_space
        self.msg = self.get_body(self.source_space)
        self.wrong_title = []
        if target_space:
            self.target_space = target_space
            self.create_body(self.msg, self.target_space)

    def get_body(self, source_space):
        """
        Gets the content of the article in the space

        :return: msg_body as dict
        """
        all_page = self.confluence.get_all_pages_from_space(source_space, start=0, status=None, expand=None,limit=30,
                                                            content_type='page')

        msg_body = {}
        child_parent = {}
        n = 0
        for i in all_page:
            n = 1+n
            child = self.confluence.get_page_child_by_type(i['id'],type='page', start=None, limit=None)

            body = self.confluence.get_page_by_id(i['id'], "body.view", status=None ,version=None)
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
        print('num: ',  n)
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
                try:
                    self.confluence.create_page(
                        space=target_space,
                        title=msg['title'],
                        body=msg['body'],
                        type=msg['type']
                    )
                    new_id = self.confluence.get_page_id(target_space, msg['title'])
                    new_parent_msg[msg['title']] = new_id
                    # break
                except Exception as e:
                    try:
                        time.sleep(3)
                        self.confluence.create_page(
                            space=target_space,
                            title=msg['title'],
                            body='wrong',
                            type=msg['type']
                        )
                        new_id = self.confluence.get_page_id(target_space, msg['title'])
                        new_parent_msg[msg['title']] = new_id
                        self.wrong_title.append(msg['title'])
                        print(e.args)
                        # print(msg)
                    except:
                        pass
            else:

                print(msg['title'], msg.get('parent_title'), new_parent_msg.get(msg.get('parent_title')))
                try:
                    self.confluence.create_page(
                        space=target_space,
                        title=msg['title'],
                        body=msg['body'],
                        parent_id=new_parent_msg.get(msg.get('parent_title')),
                        type=msg['type']
                    )
                    new_id = self.confluence.get_page_id(target_space, msg['title'])
                    new_parent_msg[msg['title']] = new_id
                    # break
                except Exception as e:
                    try:
                        time.sleep(3)
                        self.confluence.create_page(
                            space=target_space,
                            title=msg['title'],
                            body='wrong',
                            parent_id=new_parent_msg.get(msg.get('parent_title')),
                            type=msg['type']
                        )
                        new_id = self.confluence.get_page_id(target_space, msg['title'])
                        new_parent_msg[msg['title']] = new_id
                        print(e.args)
                        # print(msg)
                    except:
                        pass


        print()
        print()
        print()
        print(self.wrong_title)


def create_body_other_website(URL, USERNAME, PASSWD, msg_body, source_space, target_space):
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
        if msg.get('title') == source_space or msg.get('parent_title')==None:

            try:
                confluence.create_page(
                    space=target_space,
                    title=msg['title'],
                    body=msg['body'],
                    type=msg['type']
                )
                time.sleep(1)
                new_id = confluence.get_page_id(target_space, msg['title'])
                new_parent_msg[msg['title']] = new_id
                # break
            except Exception as e:
                time.sleep(3)
                confluence.create_page(
                    space=target_space,
                    title=msg['title'],
                    body='wrong',
                    type=msg['type']
                )
                print(e.args)
            
        else:

            print(msg['title'], msg.get('parent_title'), new_parent_msg.get(msg.get('parent_title')))

            try:
                confluence.create_page(
                    space=target_space,
                    title=msg['title'],
                    body=msg['body'],
                    parent_id=new_parent_msg.get(msg.get('parent_title')),
                    type=msg['type']
                )
                time.sleep(1)
                new_id = confluence.get_page_id(target_space, msg['title'])
                new_parent_msg[msg['title']] = new_id
                # break
            except Exception as e:
                time.sleep(3)
                confluence.create_page(
                    space=target_space,
                    title=msg['title'],
                    body='wrong',
                    type=msg['type']
                )
                print(e.args)




if __name__ == "__main__":

    source_space = 'XXX'
    target_space ='XXX'
    URL ='XXX'
    USERNAME = 'XXX'
    PASSWD = 'XXX'

    a = ConfluenceService(URL, USERNAME, PASSWD, source_space, target_space)
    # print(a.msg)
    # create_body_other_website(URL, USERNAME, PASSWD, a.msg, a.source_space, target_space)