# -*- coding: utf-8 -*-

import gzip
import json
import os

def open_json(folder, ego):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    return f

def print_list_of_commenters(folder, ego, list_of_friends):
    f = open_json(folder, ego)
    to_write = open('GALLERY/'+folder+'/'+ego+'/Graphs/list_of_commenters.json', 'w')
    cmters_already_seen = set()
    
    for line in f:
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                if 'name' in comment['from']:
                    if comment['from']['name'] == None:
                        commenter = u'None'
                    else:
                        commenter = comment['from']['name']
                else:
                    commenter = comment["from"]["id"]
                if commenter == ego:
                    commenter = 0
                else:
                    if commenter not in cmters_already_seen and commenter in list_of_friends:
                        cmters_already_seen.add(commenter)
    to_write.write(json.dumps([list_of_friends.index(e) for e in list(cmters_already_seen) if e != None]))
    to_write.close()   
    
def read_list_of_commenters(folder, ego):
    path = folder + '/' + ego
    f = open("GALLERY/"+path+"/Graphs/list_of_commenters.json", 'rb')
    for line in f:
        list_of_commenters = json.loads(line)
        return list_of_commenters

def dict_of_commenters_per_status(folder, ego):
    f = open_json(folder, ego)    
    result = {}

    for line in f:
        status = json.loads(line)
        commenters = {}
        if 'comments' in status:
            for comment in status["comments"]:
                if 'name' in comment['from']:
                    commenter = comment['from']['name']
                else:
                    commenter = comment["from"]["id"]
                if commenter == ego.decode('utf-8'):
                    commenter = 0
                if commenter not in commenters:
                    commenters[commenter] = 1
                else:
                    commenters[commenter] += 1
        result[status['id']] = commenters
    return result

def dict_of_likers_per_status(folder, ego):
    f = open_json(folder, ego)     
    result = {}

    for line in f:
        status = json.loads(line)
        likers = []
        if 'likes' in status:
            for like in status['likes']:
                if 'name' in like:
                    liker = like['name']
                else:
                    liker = like['id']
                if liker == ego.decode('utf-8'):
                    liker = 0
                likers.append(liker)
        result[status['id']] = likers
    return result

def dict_of_likers_of_comments_per_status(folder, ego):
    path = folder +'/' + ego
    f = open_json(folder, ego) 
    result = {}

    for line in f:
        status = json.loads(line)
        likers = {}
        if 'comments' in status:
            for comment in status['comments']:
                if 'likes' in comment:
                    for like in comment['likes']:
                        if 'name' in like:
                            liker = like['name']
                        else:
                            liker = like['id']
                        if 'name' in like:
                            gz_bis = 'DATA/'+path+'/ego.json.gz'
                            f_bis = gzip.open(gz_bis, 'rb')
                            infos = json.loads(f_bis)
                            if liker == infos['name']:
                                liker = 0
                        elif liker == ego:
                            liker = 0
                        if liker not in likers:
                            likers[liker] = 1
                        else:
                            likers[liker] += 1
        result[status['id']] = likers
    return result

def dict_of_mutual_commenters(folder, ego, list_of_friends):
    f = open_json(folder, ego)    
    result = {}
    
    for friend in list_of_friends:
        result[friend] = []
    
    for line in f:
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                if 'name' in comment['from']:
                    commenter = comment['from']['name']
                else:
                    commenter = comment['from']['id']
                if commenter in list_of_friends:
                    for comment_2 in status['comments']:
                        if 'name' in comment_2['from']:
                            commenter_2 = comment_2['from']['name']
                        else:
                            commenter_2 = comment_2['from']['id']
                        if commenter_2 in list_of_friends and commenter_2 != commenter:
                            result[commenter].append(commenter_2)
                            
    return result

def calculate_info_commenters(folder, ego):
    f = open_json(folder, ego) 
    result = {}
    
    for line in f:
        list_commenters_of_line = []
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                if 'name' in comment['from']:
                    commenter = comment['from']['name']
                else:
                    commenter = comment['from']['id']
                #if commenter == ego:
                    #commenter = 0
                    #if commenter in result:
                        #result[commenter]['nb_of_comments'] += 1
                        #if commenter not in list_commenters_of_line:
                            #result[commenter]['nb_of_statuses'] += 1
                            #list_commenters_of_line.append(commenter)
                if commenter in result:
                    result[commenter]['nb_of_comments'] += 1
                    if commenter not in list_commenters_of_line:
                        result[commenter]['nb_of_statuses'] += 1
                        list_commenters_of_line.append(commenter)
                else:
                    result[commenter] = {'nb_of_comments' : 1, 'nb_of_statuses' : 1}
                    list_commenters_of_line.append(commenter)
                        
    return result

def calculate_info_likers(folder, ego):
    f = open_json(folder, ego) 
    result = {}
    
    for line in f:
        status = json.loads(line)
        if 'likes' in status:
            for like in status['likes']:
                if 'name' in like:
                    liker = like['name']
                else:
                    liker = like['id']
                if liker in result:
                    result[liker] += 1
                else:
                    result[liker] = 1
                        
    return result

def calculate_info_likers_of_comment(folder, ego):
    f = open_json(folder, ego) 
    for line in f:
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                if 'likes' in comment: 
                    for like in comment['likes']:
                        if 'name' in like:
                            liker = like['name']
                        else:
                            liker = like['id']
                        if liker in result:
                            result[liker] += 1
                        else:
                            result[liker] = 1
    return result

def find_status(folder, ego, id):
    f = open_json(folder, ego) 
    for line in f:
        status = json.loads(line)
        if status['id'] == id:
            return status