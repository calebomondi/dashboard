import requests
from . import config

def allPostsView():
    pgPostIDs = []
    info1 = []
    info2 = []
    #get post IDs
    url = f'https://graph.facebook.com/v19.0/{config.page_id}/posts?access_token={config.page_AT}&limit=10'
    res = requests.get(url).json()
    if res:
        postIDs = res['data']
        for postID in postIDs:
            myID = postID['id']
            pgPostIDs.append(myID)
    #get post info1
    for id in pgPostIDs:
        url1 = f'https://graph.facebook.com/v19.0/{id}?fields=created_time,permalink_url,full_picture,likes.summary(true),comments.summary(true),shares.summary(true)&access_token={config.page_AT}'
        res1 = requests.get(url1).json()
        info1.append(res1)
    #get post info2
    for id in pgPostIDs:
        url2 = f'https://graph.facebook.com/v19.0/{id}/insights?metric=post_impressions_unique,post_engaged_users&access_token={config.page_AT}'
        res2 = requests.get(url2).json()
        info2.append(res2)

    return {'info1': info1, 'info2': info2}

def viewCompiler():
    wData = allPostsView()
    cData = []
    dat1 = wData['info1']
    dat2 = wData['info2']
    size = len(dat1)
    
    i = 0
    while i < size:
        dicti = {}
        dicti['imgUrl'] = dat1[i]['full_picture']
        dicti['postUrl'] = dat1[i]['permalink_url']
        dicti['date'] = dat1[i]['created_time'][:10]
        dicti['likes'] = dat1[i]['likes']['summary']['total_count']
        dicti['comments'] = dat1[i]['comments']['summary']['total_count']
        dicti['reach'] = dat2[i]['data'][0]['values'][0]['value']
        dicti['engage'] = dat2[i]['data'][1]['values'][0]['value']

        if 'shares' in dat1[i]:
            dicti['shares'] = dat1[i]['shares']['count']
        else:
            dicti['shares'] = 0
        cData.append(dicti)
        i += 1
    return cData

def dashData():
    tot_likes = 0
    tot_com = 0
    tot_posts = 0
    tot_shares = 0
    #get page likes and followers
    url = f'https://graph.facebook.com/v19.0/{config.page_id}?fields=fan_count,followers_count&access_token={config.page_AT}'
    res = requests.get(url).json()
    #get posts data
    urlP = f'https://graph.facebook.com/v19.0/{config.page_id}/posts?access_token={config.page_AT}'
    tot_posts = get_total_posts(urlP)
    #get LCS
    data = viewCompiler()
    for dat in data:
        tot_likes += dat['likes']
        tot_com += dat['comments']
        tot_shares += dat['shares']
    
    return {'plikes':res['fan_count'], 'followers':res['followers_count'], 'likes':tot_likes, 'comments': tot_com, 'shares':tot_shares, 'posts':tot_posts}

def get_total_posts(url):
    total_posts = 0
    while url:
        response = requests.get(url)
        data = response.json()
        if 'data' in data:
            total_posts += len(data['data'])
            url = data.get('paging', {}).get('next', None)
        else:
            break
    return total_posts

def recentShared():
    pgPostIDs = []
    #get post IDs
    url = f'https://graph.facebook.com/v19.0/{config.page_id}/posts?access_token={config.page_AT}&limit=1'
    res = requests.get(url).json()
    if res:
        postIDs = res['data']
        for postID in postIDs:
            myID = postID['id']
            pgPostIDs.append(myID)
    recent = pgPostIDs[0]
    #get post info1
    url1 = f'https://graph.facebook.com/v19.0/{recent}?fields=created_time,permalink_url,full_picture,likes.summary(true),comments.summary(true),shares.summary(true)&access_token={config.page_AT}'
    res1 = requests.get(url1).json()
    toSend = res1
    if 'shares' not in res1:
        toSend['shares'] = 0
    else:
        toSend['shares'] = res1['shares']['count']

    return toSend

def most():
    comments = []
    likes = []
    shares = []
    #return
    final = {}
    #get LCS
    data = viewCompiler()
    for dat in data:
        comments.append(dat['comments'])
        likes.append(dat['likes'])
        shares.append(dat['shares'])
    shares.sort(reverse=True)
    likes.sort(reverse=True)
    comments.sort(reverse=True)
    #get post
    for dat in data:
        if dat['comments'] == comments[0]:
            final['comments'] = dat
        if dat['likes'] == likes[0]:
            final['likes'] = dat
        if dat['shares'] == shares[0]:
            final['shares'] = dat

    return final

def last24hrs():
    # last 24 hours performance
    metrics = 'page_impressions_unique,page_impressions_paid_unique,page_impressions_organic_unique_v2,page_posts_impressions_unique,page_consumptions_unique,page_total_actions,page_fans_online,page_daily_follows'
    url = f'https://graph.facebook.com/v19.0/{config.page_id}/insights?metric={metrics}&period=day&access_token={config.page_AT}'
    res = requests.get(url).json()
    pgImpress = res['data'][0]['values'][1]['value']
    pgImpressPaid = res['data'][1]['values'][1]['value']
    pgImpressOrg = res['data'][2]['values'][1]['value']
    poImpress = res['data'][3]['values'][1]['value']
    contClicks = res['data'][4]['values'][1]['value']
    ctaCont = res['data'][5]['values'][1]['value']
    dailyFol = res['data'][7]['values'][1]['value']

    return {'pgImpress':pgImpress,'pgImpressPaid':pgImpressPaid,'pgImpressOrg':pgImpressOrg,'poImpress':poImpress,'contClicks':contClicks,'ctaCont':ctaCont,'dailyFol':dailyFol}
