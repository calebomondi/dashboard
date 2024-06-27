from .models import UsrCredentials

#get user & details
user = UsrCredentials.objects.get(usrname='zen')

#instagram
igAT = user.llat
ig_user_id = user.iguserid
#facebook
page_id = user.fbpageid
fbAT = igAT
page_AT = user.pgat
