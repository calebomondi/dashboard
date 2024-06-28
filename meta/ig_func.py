from . import config
import requests
import facebook as fb
import urllib.parse

#DASHBOARD
def pageInfo():
    fields = 'username,name,biography,followers_count,follows_count,media_count'
    page_info_url = f'https://graph.facebook.com/v19.0/{config.ig_user_id}?fields={fields}&access_token={config.igAT}'
    info = requests.get(page_info_url).json()
    return info

def postInsights():
    metrics = 'impressions, reach,profile_views,total_interactions, likes, comments, shares, saves, replies,'
    post_insights_url = f'https://graph.facebook.com/{config.ig_user_id}/insights?metric={metrics}&period=day&metric_type=total_value&access_token={config.igAT}'
    insights = requests.get(post_insights_url).json()
    return insights

def totalCLS():
    metrics = 'engagement,impressions,reach,likes, comments, shares,total_interactions,saved'
    likes = 0
    comments = 0
    shares = 0
    
    #get media objects
    url = f'https://graph.facebook.com/v19.0/{config.ig_user_id}/media?access_token={config.igAT}&limit=10'
    output = requests.get(url).json()
    if 'data' in output:
        mediaObjArr = output['data']
        print(f'size: {len(mediaObjArr)}')
        #get single post metrics
        i = 0
        for mediaObj in mediaObjArr:
            post_likes = 0
            post_comments = 0
            post_shares = 0
            id = mediaObj['id']
            #media insites
            url_media = f'https://graph.facebook.com/{id}/insights?metric={metrics}&access_token={config.igAT}'
            media_info = requests.get(url_media).json()
            for dat in media_info['data']:
                if dat['name'] == 'likes':
                    post_likes = dat['values'][0]['value']
                if dat['name'] == 'comments':
                    post_comments = dat['values'][0]['value']
                if dat['name'] == 'shares':
                    post_shares = dat['values'][0]['value']
            likes += post_likes
            comments += post_comments
            shares += post_shares    

            i += 1
            if i > 9:
                break
    return {'likes': likes, 'comments':comments, 'shares':shares}
        
def dayInsights():
    insights = postInsights()

    for dat in insights['data']:
        if dat['name'] == 'impressions':
            impressions = dat['total_value']['value']
        if dat['name'] == 'reach':
            reach = dat['total_value']['value']
        if dat['name'] == 'profile_views':
            pviews = dat['total_value']['value']
        if dat['name'] == 'total_interactions':
            interact = dat['total_value']['value']
        if dat['name'] == 'likes':
            likes = dat['total_value']['value']
        if dat['name'] == 'comments':
            comments = dat['total_value']['value']
        if dat['name'] == 'shares':
            shares = dat['total_value']['value']
        if dat['name'] == 'saves':
            saves = dat['total_value']['value']
    return {'impressions':impressions,'reach':reach,'pviews':pviews,'interact':interact,'likes':likes,'comments':comments,'shares':shares,'saves':saves}

def most():
    #Arrays
    Likes = []
    Shares = []
    Comments = []
    #to return
    most_likes = {}
    most_comm = {}
    most_shares = {}
    final = {}
    postIDs = {}
    #--
    metrics = 'likes,comments, shares'
    fields = 'permalink,media_url,timestamp'
    #get media objects
    url = f'https://graph.facebook.com/v19.0/{config.ig_user_id}/media?access_token={config.igAT}&limit=10'
    output = requests.get(url).json()
    if 'data' in output:
        mediaObjArr = output['data']
        for mediaObj in mediaObjArr:
            media_info = getObject(mediaObj['id'])
            for dat in media_info['data']:
                if dat['name'] == 'likes':
                    Likes.append(dat['values'][0]['value'])
                if dat['name'] == 'shares':
                    Shares.append(dat['values'][0]['value'])
                if dat['name'] == 'comments':
                    Comments.append(dat['values'][0]['value'])
        Likes.sort(reverse=True)
        Comments.sort(reverse=True)
        Shares.sort(reverse=True)
        #get post Ids
        for mediaObj in mediaObjArr:
            media_info = getObject(mediaObj['id'])
            for dat in media_info['data']:
                if dat['name'] == 'likes':
                    if dat['values'][0]['value'] == Likes[0]:
                        most_likes['likes'] = Likes[0]
                        most_likes['comments'] = media_info['data'][1]['values'][0]['value']
                        most_likes['shares'] = media_info['data'][2]['values'][0]['value']
                        pid_likes = mediaObj['id'] 
                        postIDs['likes'] = pid_likes
                if dat['name'] == 'comments':
                    if dat['values'][0]['value'] == Comments[0]:
                        most_comm['likes'] = media_info['data'][0]['values'][0]['value']
                        most_comm['comments'] = Comments[0]
                        most_comm['shares'] = media_info['data'][2]['values'][0]['value']
                        pid_comments = mediaObj['id']
                        postIDs['comments'] = pid_comments
                if dat['name'] == 'shares':
                    if dat['values'][0]['value'] == Shares[0]:
                        most_shares['likes'] = media_info['data'][0]['values'][0]['value']
                        most_shares['comments'] = media_info['data'][1]['values'][0]['value']
                        most_shares['shares'] = Shares[0]
                        pid_shares = mediaObj['id']
                        postIDs['shares'] = pid_shares
        #add post url
        most_shares['url'] = getURL(postIDs['shares'])
        most_likes['url'] = getURL(postIDs['likes'])
        most_comm['url'] = getURL(postIDs['comments'])
    return {'shared': most_shares, 'liked': most_likes, 'commented': most_comm}

def getURL(pID):
    fields = 'permalink,media_url,timestamp'
    url_link = f'https://graph.facebook.com/v15.0/{pID}?fields={fields}&access_token={config.igAT}'
    return requests.get(url_link).json()

def getObject(pID):
    metrics = 'likes,comments, shares'
    url_media = f'https://graph.facebook.com/{pID}/insights?metric={metrics}&access_token={config.igAT}'
    return requests.get(url_media).json()

def recentlyPosted():
    metrics = 'likes,comments, shares'
    fields = 'permalink,media_url,timestamp'
    recent = 1
    #get media objects
    url = f'https://graph.facebook.com/v19.0/{config.ig_user_id}/media?access_token={config.igAT}&limi=1'
    output = requests.get(url).json()
    if 'data' in output:
        mediaObjArr = output['data']
        recent = mediaObjArr[0]['id']
        print(recent)
    #get likes,shares,comments
    url_media = f'https://graph.facebook.com/{recent}/insights?metric={metrics}&access_token={config.igAT}'
    media_info = requests.get(url_media).json()
    for dat in media_info['data']:
        if dat['name'] == 'comments':
            post_comments = dat['values'][0]['value']
        if dat['name'] == 'likes':
            post_likes = dat['values'][0]['value']
        if dat['name'] == 'shares':
            post_shares = dat['values'][0]['value']
    #post link and short code
    url_link = f'https://graph.facebook.com/v15.0/{recent}?fields={fields}&access_token={config.igAT}'
    post_url = requests.get(url_link).json()

    return {'url':post_url,'likes':post_likes, 'shares':post_shares, 'comments':post_shares}

#VIEW
def getPostsData():
    metrics = 'likes,comments, shares,saved,reach'
    fields = 'permalink,media_url,timestamp'
    data = []
    links = []
    #get media objects
    url = f'https://graph.facebook.com/v19.0/{config.ig_user_id}/media?access_token={config.igAT}&limit=10'
    output = requests.get(url).json()
    if 'data' in output:
        mediaObjArr = output['data']
        print(f'size: {len(mediaObjArr)}')
        #get single post metrics
        for mediaObj in mediaObjArr:
            print(mediaObj['id'])
            #media insites
            id = mediaObj['id']
            url_media = f'https://graph.facebook.com/{id}/insights?metric={metrics}&access_token={config.igAT}'
            media_info = requests.get(url_media).json()
            data.append(media_info)
            #post link and short code
            url_link = f'https://graph.facebook.com/v15.0/{id}?fields={fields}&access_token={config.igAT}'
            post_url = requests.get(url_link).json()
            links.append(post_url)
    
    return {'data':data,'links':links}

def compilePosts():
    final = []
    rawDat = getPostsData()
    size = len(rawDat['data'])
    print(size)
    
    i = 0
    while i < size:
        addData = {}
        addData['date'] = rawDat['links'][i]['timestamp'][:10]
        addData['imgUrl'] = rawDat['links'][i]['media_url']
        addData['postUrl'] = rawDat['links'][i]['permalink']
        addData['likes'] = rawDat['data'][i]['data'][0]['values'][0]['value']
        addData['comments'] = rawDat['data'][i]['data'][1]['values'][0]['value']
        addData['shares'] = rawDat['data'][i]['data'][2]['values'][0]['value']
        addData['saved'] = rawDat['data'][i]['data'][3]['values'][0]['value']
        addData['reach'] = rawDat['data'][i]['data'][4]['values'][0]['value']
        #print(addData)
        final.append(addData)
        i += 1      
    
    return final

#POST
def makePost(imgUrl,caption):    
    encoded_url = urllib.parse.quote(imgUrl, safe='')
    encoded_cap = urllib.parse.quote(caption, safe='')
    #get container ID
    url = f'https://graph.facebook.com/v19.0/{config.ig_user_id}/media?image_url={encoded_url}&caption={encoded_cap}&access_token={config.igAT}'
    container_id = requests.post(url).json()
    #make post 
    if 'id' in container_id:
        print(f"container-id: {container_id['id']}")
        id = container_id['id']
        url2 = f'https://graph.facebook.com/v19.0/{config.ig_user_id}/media_publish?creation_id={id}&access_token={config.igAT}'
        media_id = requests.post(url2).json()

        if 'id' in media_id:
            print(f"media-id: {media_id['id']}")
            return media_id['id']
        else:
            print('Media ID Not Found!')
    else:
        print('Container ID Not Found!')

def postAll(file,caption,typ):
    #facebook object
    fbObj = fb.GraphAPI(config.page_AT)
    #upload in fb to get post id
    res = fbObj.put_photo(file,message=caption)
    post_id = res['post_id']
    print(f'post id: {post_id}')
    if typ == 0:
        print('FB Posted Successfully!')
        return 200
    #get post picture url
    url = f'https://graph.facebook.com/{post_id}?fields=full_picture&access_token={config.page_AT}'
    output = requests.get(url).json()
    if output and typ == 1:
        print('FB yes!')
        #post to IG
        res = makePost(output['full_picture'],caption)
        return res
    if output and typ == 2:
        res = makePost(output['full_picture'],caption)
        print(f'ig: {res}')
        url = f'https://graph.facebook.com/{post_id}?access_token={config.page_AT}'
        resp = requests.delete(url).json().get('success')
        print(f'resp: {resp}')
        return resp

#print(postAll('E:/UEFA_logo.png','It"s UEFA'))

#url = 'https://yt3.googleusercontent.com/r2E5eqodxe1vI1fUg229yOL5YyiBFq23wSbzXCcVKMEINj3i_DkM3hKZ4Rt9CBG3N9qaSInc=s900-c-k-c0x00ffffff-no-rj'
#caption = '#premierleague #mancity #4inarow #pep #champions2024'
#print(makePost(url,caption)) 