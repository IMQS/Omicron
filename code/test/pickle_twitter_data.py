'''
Created on 01 Jul 2013

@author: M. Rozenkrantz
@summary: Used to 'hard code' Twitter data which is then used as input for test cases.

'''
import social_platform as sp
import pickle
hashtag = '#coffee'


if __name__ == '__main__':
    twitterObject = sp.twitter_platform()
    twitterObject.authenticate()
    #: Search for 50 posts which have 'coffee' tagged.
    data = twitterObject.request_center_radius(search_tags = [hashtag])
    pickle.dump( data, open( "tweets.p", "wb" ) )
    print 'Data has been pickled to \'tweets.p\''