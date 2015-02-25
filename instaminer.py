import urllib
import json

#limits= 	5,000 / hour per token

accesstoken='your-access-token'	#do not share access token
icount='20'	#records per request
database={}

uids=['1714352117','367597243']	#user's id

for userid in uids:
	database[userid]={}
	total=0
	nexturl='https://api.instagram.com/v1/users/'+userid+'/media/recent/?access_token='+accesstoken+'&count='+icount
	while nexturl!=None:
		
		txt=urllib.urlopen(nexturl).read()
		js=json.loads(txt)
		
		datalen=len(js['data'])
		if datalen==0: 
			nexturl=None
			continue
		for i in range(datalen):
			if js['data'][i]['caption'] != None:
				text=js['data'][i]['caption']['text']
			else:
				text=None
			imgurl=js['data'][i]['images']['standard_resolution']['url']
			comments_text=[i['text'] for i in js['data'][i]['comments']['data']]
			for comment in comments_text:
				if comment != None:
					chunks=comment.split()
					comment_hashtags=[j for j in chunks if j.startswith("#")]
				else: comment_hashtags=[]
			if text != None:
				
				tchunks=text.split()	
				hashtags=[j for j in tchunks if j.startswith("#")]
			else: hashtags=[]
			
			database[userid][imgurl]={}
			database[userid][imgurl]['hashtags']=hashtags
			database[userid][imgurl]['comment_hashtags']=comment_hashtags
			database[userid][imgurl]['comment_list']=comments_text
			database[userid][imgurl]['caption']=text
		
		if js['pagination'].has_key('next_url'):
			nexturl=js['pagination']['next_url']
		else:
			nexturl=None
		total += datalen
	
	print "Total images for user: "+userid+": ",total

print database

