import read_friends
import read_statuses

def main(folder, ego, options):
    if options == 'friends' :
        return read_friends.dict_of_mutual(folder, ego)
    elif options == 'statuses' :
        list_of_friends = read_friends.list_of_friends(folder, ego)
        return read_statuses.dict_of_mutual_commenters(folder, ego, list_of_friends)
    elif options == 'commenters':
        list_of_friends = read_friends.list_of_friends(folder, ego)
        return read_statuses.dict_of_commenters_per_status(folder, ego, list_of_friends)