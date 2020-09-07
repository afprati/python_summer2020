# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 15:17:35 2020

@author: miame
"""
"""
Assignment:

For the purposes of this exercise, we define three types of Twitter users.
- Layman:  Users with less than 100 followers
- Expert:  Users with 100-1000 followers
- Celebrity:  Users with more than 1000 followers

Using the Twitter API, and starting with the @WUSTLPoliSci twitter user, answer
the following:
-One degree of separation:
    –Among the followers of @WUSTLPoliSci who is the most active?
    –Among the followers of @WUSTLPoliSci who is the most popular, i.e.  has
    the greatest number of followers?
    –Among the friends of @WUSTLPoliSci, i.e. the users she is following, who
    are the most active layman, expert and celebrity?
    –Among the friends of @WUSTLPoliSci who is the most popular?

-Two degrees of separation: For the following two questions, limit your search
of followers and friends to laymen and experts.
    –Among the followers of @WUSTLPoliSci and their followers, who is the
    most active?
    –Among the friends of @WUSTLPoliSci and their friends, who is the most active?

For reference, current tweepy documentation:
    http://docs.tweepy.org/en/v3.9.0/api.html
Latest tweepy documentation:
    http://docs.tweepy.org/en/latest/api.html
"""
import importlib # to import file
import sys # add directory to system PATH
import time

start_twitter_handle = 'WUSTLPoliSci'
batch_size = 100 #max allowed by tweepy
sleep_time = 20
laymen_follower_count = 100
expert_follower_count = 1000
celebrity_follower_count = 1001

sys.path.insert(0, 'C:/Users/miame/Documents/Secrets')
twitter = importlib.import_module('start_twitter')
api = twitter.client

start = time.time()

# =============================================================================
# variables we want from first degree of separation
# =============================================================================

most_active_follower_WUSTL = {}
most_popular_follower_WUSTL = {}

most_active_friend_WUSTL_laymen = {}
most_active_friend_WUSTL_expert = {}
most_active_friend_WUSTL_celebrity = {}
most_popular_friend_WUSTL = {}

# =============================================================================
# additional variables from the second degree of separation
# =============================================================================

most_active_follower = {}
most_active_friend = {}

# =============================================================================
# function to batch out users from provided list
# from: https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks
# =============================================================================

def batch(iterable, n=batch_size):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

# =============================================================================
# function to determine most active follower, most popular follower,
# and a dictionary of followers
# =============================================================================

def get_followers(handles_list):
    global number_requests
    #creating a dictionary for the followers
    follower_dict = {}

    #empty dictionaries to keep the most active and most popular
    most_active_laymen = {'screen_name' : 0} #default dict key/value
    most_active_expert = {'screen_name' : 0}
    most_active_celebrity = {'screen_name' : 0}
    most_popular = {'screen_name' : 0}

    for user in handles_list:
        current_time = time.time()
        print("User handle: " + user + ". Elapsed time: " + str(current_time - start))
        user_follower_ids = api.followers_ids(user)
        number_requests += 1

        loop_count = 0

        for batch_list in batch(user_follower_ids):
            print("Batch #" + str(loop_count) + ": " + str(loop_count*batch_size + len(batch_list)) +
                  " (request count: " + str(number_requests) + ").")
            loop_count+=1
            time.sleep(sleep_time) #to avoid rate limit

            followers = api.lookup_users(batch_list)
            number_requests += 1

            for follower in followers:
                screen_name = follower.screen_name
                tweet_count = follower.statuses_count
                followers_count = follower.followers_count

                # finding most active friend by category
                if followers_count <= laymen_follower_count:
                    if tweet_count > list(most_active_laymen.values())[0]:
                        most_active_laymen = {screen_name : tweet_count}
                elif followers_count >= celebrity_follower_count:
                    if tweet_count > list(most_active_celebrity.values())[0]:
                        most_active_celebrity = {screen_name : tweet_count}
                else: #aka an expert
                    if tweet_count > list(most_active_expert.values())[0]:
                        most_active_expert = {screen_name : tweet_count}

                if followers_count > list(most_popular.values())[0]:
                    most_popular = {screen_name : followers_count}

                #updating the dictionary;
                #ONLY SAVING LAYMEN AND EXPERTS (per assignment)
                #values are tuple with tweet count first, follower count second
                if followers_count < celebrity_follower_count:
                    follower_dict.update({screen_name : (tweet_count, followers_count)})

    return (follower_dict, most_active_laymen, most_active_expert,
            most_active_celebrity, most_popular) #returning tuple

# =============================================================================
# function to determine most active friends by category, most popular friend,
# and a dictionary of friends (friends are accounts you follow)
# =============================================================================

def get_friends(handles_list):
    global number_requests
    #creating a dictionary for the followers
    friends_dict = {}

    #empty dictionaries to keep the most active and most popular
    most_active_laymen = {'screen_name' : 0} #default dict key/value
    most_active_expert = {'screen_name' : 0}
    most_active_celebrity = {'screen_name' : 0}
    most_popular = {'screen_name' : 0}

    for user in handles_list:
        loop_count = 0
        current_time = time.time()
        print("User handle: " + user + ". Elapsed time: " + str(current_time - start))
        user_friends_ids = api.friends_ids(user)
        number_requests += 1

        for batch_list in batch(user_friends_ids):
            print("Batch #" + str(loop_count) + ": " + str(loop_count*batch_size + len(batch_list)) +
                  " (request count: " + str(number_requests) + ").")
            loop_count+=1
            time.sleep(sleep_time) #to avoid rate limit

            friends = api.lookup_users(batch_list)
            number_requests += 1

            for friend in friends:
                screen_name = friend.screen_name
                tweet_count = friend.statuses_count
                followers_count = friend.followers_count
    
                # finding most active friend by category
                if followers_count <= laymen_follower_count:
                    if tweet_count > list(most_active_laymen.values())[0]:
                        most_active_laymen = {screen_name : tweet_count}
                elif followers_count >= celebrity_follower_count:
                    if tweet_count > list(most_active_celebrity.values())[0]:
                        most_active_celebrity = {screen_name : tweet_count}
                else: #aka an expert
                    if tweet_count > list(most_active_expert.values())[0]:
                        most_active_expert = {screen_name : tweet_count}
                # finding most popular friend
                if followers_count > list(most_popular.values())[0]:
                    most_popular = {screen_name : followers_count}
    
                #updating the dictionary;
                #ONLY SAVING LAYMEN AND EXPERTS (per assignment)
                #values are tuple with tweet count first, follower count second
                if followers_count < celebrity_follower_count:
                    friends_dict.update({screen_name : (tweet_count, followers_count)})

    return (friends_dict, most_active_laymen, most_active_expert,
            most_active_celebrity,  most_popular) #returning tuple


# =============================================================================
# return dictionary with highest value
# =============================================================================

def get_highest(list_of_dicts):
    values = list(list_of_dicts.values())
    keys = list(list_of_dicts.keys())
    max_value = max(values)
    values_index = values.index(max_value)
    return {keys[values_index] : values[values_index]}

# =============================================================================
# first degree
# =============================================================================
number_requests = 0

print("Starting to find followers of " + start_twitter_handle)

(followers_WUSTLPoliSci,
 most_active_follower_WUSTL_laymen,
 most_active_follower_WUSTL_expert,
 most_active_follower_WUSTL_celebrity,
 most_popular_follower_WUSTL) = get_followers([start_twitter_handle])

most_active_follower_WUSTL = get_highest({**most_active_follower_WUSTL_laymen,
                                          **most_active_follower_WUSTL_expert,
                                          **most_active_follower_WUSTL_celebrity})

print('Most active follower of ' + start_twitter_handle + ': ' + str(most_active_follower_WUSTL))
# Most active follower of WUSTLPoliSci: {'tubuann_only': 109517}
print('Most popular follower of ' + start_twitter_handle + ': ' + str(most_popular_follower_WUSTL))
# Most popular follower of WUSTLPoliSci: {'BrendanNyhan': 81142}

print("Starting to find friends of " + start_twitter_handle)

(friends_WUSTLPoliSci,
 most_active_friend_WUSTL_laymen,
 most_active_friend_WUSTL_expert,
 most_active_friend_WUSTL_celebrity,
 most_popular_friend_WUSTL) = get_friends([start_twitter_handle])

print('Most active laymen friend of ' + start_twitter_handle + ': ' +
      str(most_active_friend_WUSTL_laymen))
# Most active laymen friend of WUSTLPoliSci: {'usmanfalalu1' : 1445}
print('Most active expert friend of ' + start_twitter_handle + ': ' +
      str(most_active_friend_WUSTL_expert))
# Most active expert friend of WUSTLPoliSci: {'prof_nokken' : 12562}
print('Most active celebrity friend of ' + start_twitter_handle + ': ' +
      str(most_active_friend_WUSTL_celebrity))
# Most active expert friend of WUSTLPoliSci: {'nytimes' : 406561}
print('Most popular friend of ' + start_twitter_handle + ': ' +
      str(most_popular_friend_WUSTL))
# Most popular friend of WUSTLPoliSci: {'BarackObama' : 122267221}

# =============================================================================
# second degree
# =============================================================================

# NB: only technically need most active

print("Starting to find followers of the followers of " + start_twitter_handle)

(second_degree_followers,
 second_degree_most_active_follower_laymen,
 second_degree_most_active_follower_expert,
 second_degree_most_active_follower_celebrity,
 second_degree_most_popular_follower) = get_followers(list(followers_WUSTLPoliSci.keys()))

most_active_follower = get_highest({**most_active_follower_WUSTL_laymen,
                                    **most_active_follower_WUSTL_expert,
                                    **second_degree_most_active_follower_laymen,
                                    **second_degree_most_active_follower_expert})

print('Most active user of followers of ' + start_twitter_handle + ' and its followers: ' +
      str(most_active_follower))

print("Starting to find friends of friends of " + start_twitter_handle)

(second_degree_friends,
 second_degree_most_active_friend_laymen,
 second_degree_most_active_friend_expert,
 second_degree_most_active_friend_celebrity,
 second_degree_most_popular_friend) = get_friends(list(friends_WUSTLPoliSci.keys()))

most_active_friend = get_highest({**most_active_friend_WUSTL_laymen,
                                  **most_active_friend_WUSTL_expert,
                                  **second_degree_most_active_friend_laymen,
                                  **second_degree_most_active_friend_expert})

print('Most active user of friends of ' + start_twitter_handle + ' and its friends: ' +
      str(most_active_friend))

end = time.time()

print("Total run time (in seconds): " + str(end - start))
