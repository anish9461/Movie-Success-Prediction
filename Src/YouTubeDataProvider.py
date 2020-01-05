import gdata.youtube
import gdata.youtube.service
from apiclient.discovery import build
#from optparse import OptionParser
import os
import ssl
import keyprovider
import httplib2

DEVELOPER_KEY = keyprovider.getYouTubeDeveloperKey()
YOUTUBE_API_SERVICE_NAME = keyprovider.getYouTubeServiceName()
YOUTUBE_API_VERSION = keyprovider.getYouTubeVersion()
yt_service = gdata.youtube.service.YouTubeService()
# Comment feed URL
comment_feed_url = "http://gdata.youtube.com/feeds/api/videos/%s/comments?start-index=1&max-results=3"


ssl._create_default_https_context = ssl._create_unverified_context

''' Get a List of all comments from you tube based on search keyword'''
def getYouTubeComments(keyword, maxVideos=10):

    youTubeComments = []
    videoIds = getYouTubeVideoIds(keyword, maxVideos);
    for videoid in videoIds:
        url = comment_feed_url % videoid
        comment_feed = yt_service.GetYouTubeVideoCommentFeed(uri=url)

        count = 0

        try:
            while comment_feed:
                for comment_entry in comment_feed.entry:
                    #print comment_entry.id.text
                    #print comment_entry.author[0].name.text
                    #print comment_entry.title.text
                    #print comment_entry.published.text
                    #print comment_entry.updated.text
                    #print comment_entry.content.text

                    youTubeComments.append(comment_entry.content.text)    

                if comment_feed is not None:
                    nextLinkRef = comment_feed.GetNextLink()
                    if nextLinkRef is not None:
                        comment_feed = yt_service.Query(nextLinkRef.href)

                count = count + 1
                # Fetch only top 100 comments
                if count == 100:
                    return youTubeComments
                

        except Exception as e:
            print 'Error in youtube comment retrieval:\n'
            print e
    #end for
    return youTubeComments
#end getYouTubeComments


def getYouTubeVideoIds(keyword, maxresults):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY,http=httplib2.Http( disable_ssl_certificate_validation=True))
    search_response = youtube.search().list(q=keyword,part="id,snippet",maxResults=maxresults).execute()

    videos_id = []
    try:
        
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos_id.append(search_result["id"]["videoId"])
                #print "Title : " + search_result["snippet"]["title"]
                #print "Id : " + search_result["id"]["videoId"]
      
      
    except Exception as e:
        print "Error in retrieving comments from youtube.. \n"
        print e

    return videos_id



#comments = getYouTubeComments('Conjuring English Movie', 10)
#print "Total comments retrieved : ", len(comments)
