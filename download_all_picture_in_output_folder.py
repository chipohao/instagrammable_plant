# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import json
import sys
import configparser
import os
from io import open
import requests
from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings


def usage():
    return """
        python crawler.py posts -u cal_foodie -n 100 -o ./output
        python crawler.py posts_full -u cal_foodie -n 100 -o ./output
        python crawler.py profile -u cal_foodie -o ./output
        python crawler.py profile_script -u cal_foodie -o ./output
        python crawler.py hashtag -t taiwan -o ./output

        The default number for fetching posts via hashtag is 100.
    """


def get_posts_by_user(username, number, detail, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_user_posts(username, number, detail)


def get_profile(username):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_profile(username)


def get_profile_from_script(username):
    ins_cralwer = InsCrawler()
    return ins_cralwer.get_user_profile_from_script_shared_data(username)


def get_posts_by_hashtags(tag, number, debug):
    ins_crawler = InsCrawler(has_screen=debug)

    ret=ins_crawler.get_latest_posts_by_tag(tag, number)

    return ins_crawler.get_latest_posts_by_tag(tag, number)


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


def output(data, filepath):
    out = json.dumps(data, ensure_ascii=False)
    if filepath:
        with open(filepath, "w", encoding="utf8") as f:
            f.write(out)
    else:
        print(out)


if __name__ == "__main__":

    output_folder='./output_folder/'
    
    filenames=os.listdir(output_folder)


    if os.path.isdir('./img_folder/'):
        pass
    else:
        os.mkdir('./img_folder/')

    for filename in filenames:
        print(filename)
        count=0
        with open('{}/{}'.format(output_folder,filename), 'r', encoding="utf8") as read_file:
            dict_data = json.load(read_file)
            hashtag=filename.split('.')[0]

            if os.path.isdir('./img_folder/{}'.format(hashtag)):
                pass
            else:
                os.mkdir('./img_folder/{}'.format(hashtag))
            
            #print(dict_data)
            for k in dict_data:
                print(k['img_url'])
                
                filename=k['img_url'].split('/')[-1].split('.')[0]
                if os.path.isfile("./img_folder/{}/{}.png".format(hashtag,filename)):
                    print("./img_folder/{}/{}.png".format(hashtag,filename),'exist')
                    continue                
                response = requests.get(k['img_url'])
                file = open("./img_folder/{}/{}.png".format(hashtag,filename), "wb")
                file.write(response.content)
                file.close()
                count+=1
                #break