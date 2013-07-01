'''
Created on 01 Jul 2013

@author: M. Rozenkrantz
'''
import social_platform as sp
import pickle

if __name__ == '__main__':
    twitterObject = sp.twitter_platform()
    twitterObject.authenticate()
    data = twitterObject.request_center_radius(search_tags = ['#food'])
    data2 = twitterObject.strip_data(data, ['tags', 'locations'])
    print data2
    
    pickle.dump(data2, open( "tweets.p", "wb" ) ) 
    pickled_data = pickle.load( open( "tweets.p", "rb" ) )

    print pickled_data