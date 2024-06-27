from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import ig_func
from . import fb_func
from .forms import myForm,formSet
from django.http import JsonResponse
from .models import UsrCredentials
from . import gen_func

# Create your views here.
def welcome(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

#FACEBOOK
def facebook_dashboard(request):
    template = loader.get_template('fb_dashboard.html')
    data = fb_func.dashData()
    recent = fb_func.recentShared()
    most = fb_func.most()
    last = fb_func.last24hrs()
    context = {
        'recent': recent,
        'liked' : most['likes'],
        'shared' : most['shares'],
        'commented' : most['comments'],
        'data':data,
        'last': last
    }
    return HttpResponse(template.render(context,request))

def facebook_view(request):
    template = loader.get_template('fb_views.html')
    viewData = fb_func.viewCompiler()
    context = {
        'posts': viewData,
    }
    return HttpResponse(template.render(context,request))

def facebook_post(request):
    form = myForm()
    template = loader.get_template('fb_post.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def face_make_post(request):
    if request.method == 'POST':
        form = myForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            caption = form.cleaned_data['caption']
        
        status = ig_func.postAll(file, caption,0)
        if status:
            return JsonResponse({'message': 'Posting To Facebook Completed'})
        else:
            return JsonResponse({'message': 'Post Not Successful'}, status=400)
        
    return JsonResponse({'message': 'Method Not Post'}, status=405)

#INSTAGRAM
def instagram_dashboard(request):
    template = loader.get_template('ig_dashboard.html')
    info = ig_func.pageInfo()
    CLS = ig_func.totalCLS()
    daily_ins = ig_func.dayInsights()
    most = ig_func.most()
    recent = ig_func.recentlyPosted()
    context = {
        'followers':info['followers_count'],
        'following':info['follows_count'],
        'posts':info['media_count'],
        'tot_likes': CLS['likes'],
        'tot_comment': CLS['comments'],
        'tot_shares': CLS['shares'],
        'impressions': daily_ins['impressions'], 
        'reach': daily_ins['reach'], 
        'pviews': daily_ins['pviews'], 
        'interact': daily_ins['interact'], 
        'likes': daily_ins['likes'], 
        'comments': daily_ins['comments'], 
        'shares': daily_ins['shares'], 
        'saves': daily_ins['saves'],
        'most_liked':most['liked'],
        'most_shared':most['shared'],
        'most_comments':most['commented'],
        'recent':recent,
    }
    return HttpResponse(template.render(context,request))

def insta_views(request):
    template = loader.get_template('ig_views.html')
    data = ig_func.compilePosts()
    context = {
        'posts': data
    }
    return HttpResponse(template.render(context,request))

def insta_post(request):
    form = myForm()
    template = loader.get_template('ig_post.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def insta_make_post(request):
    if request.method == 'POST':
        form = myForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            caption = form.cleaned_data['caption']
        
        post_id = ig_func.postAll(file, caption, 2)
        print(f'VIEW: {post_id}')
        if post_id:
            return JsonResponse({'message': 'Posting To Instagram Completed'})
        else:
            return JsonResponse({'message': 'Post Not Successful'}, status=400)
        
        #return HttpResponse(f'{file} - {caption}')
    return JsonResponse({'message': 'Method Not Post'}, status=405)

#SETUP
def setup(request):
    form = formSet()
    template = loader.get_template('setup.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def setup_process(request):
    if request.method == 'POST':
        form = formSet(request.POST)
        if form.is_valid():
            #get form inputs
            usrname = form.cleaned_data['usrname'] 
            slToken = form.cleaned_data['slToken']
            fbPgId = form.cleaned_data['fbPgId']
            appId = form.cleaned_data['appId']
            appSecret = form.cleaned_data['appSecret']
            #get LLTKN and PGTKN
            res = gen_func.genLLAT_PAT(appId,appSecret,slToken,fbPgId)

            if res['access_token']:
                print('Am In!')
                usr, created = UsrCredentials.objects.update_or_create(
                    usrname=usrname,
                    defaults = {
                        'usrname':usrname,
                        'llAT':res['access_token'],
                        'pgAT':res['page_token'],
                        'igUserId':res['ig_user'],
                        'fbPageId':fbPgId,
                        'appID':appId,
                        'appSecret':appSecret
                    }
                )
                #usr = UsrCredentials(usrname=usrname,llAT=res['access_token'],pgAT=res['page_token'],igUserId=igUsrId,fbPageId=fbPgId,appID=appId,appSecret=appSecret)
                #usr.save()
                if usr:
                    print(f'usr: {usr}')
                    return JsonResponse({'message': 'Data Processing Completed!'})
                else:
                    return JsonResponse({'message': 'Data Processing Not Successful'}, status=400)
            
    return JsonResponse({'message': 'Method Not Post'}, status=405)

#ALL
def postAll(request):
    form = myForm()
    template = loader.get_template('all_post.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def all_make_post(request):
    if request.method == 'POST':
        form = myForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            caption = form.cleaned_data['caption']
        
        post_id = ig_func.postAll(file, caption, 1)
        if post_id:
            return JsonResponse({'message': 'Posting To All Socials Completed'})
        else:
            return JsonResponse({'message': 'Post Not Successful'}, status=400)
        
        #return HttpResponse(f'{file} - {caption}')
    return JsonResponse({'message': 'Method Not Post'}, status=405)