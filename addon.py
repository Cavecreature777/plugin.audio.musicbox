#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 2014 Techdealer

##############LIBRARIES TO IMPORT AND SETTINGS####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time,datetime,os,xbmcvfs
import json
import random
h = HTMLParser.HTMLParser()

import SimpleDownloader as downloader
downloader = downloader.SimpleDownloader()
from t0mm0.common.addon import Addon
from random import randint

addon_id = 'plugin.audio.musicbox'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
translation = selfAddon.getLocalizedString
datapath = Addon(addon_id).get_profile()

def translate(text):
	return translation(text).encode('utf-8')
	  
###################################################################################
#MAIN MENU

def Main_menu():
	if selfAddon.getSetting('vk_token') == "":
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400), translate(30401))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q=eminem&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		if 'error' in decoded_data:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400), translate(30402))
			xbmcaddon.Addon(addon_id).openSettings()
		else:
			addDir(translate(30403),'1',1,addonfolder+artfolder+'recomended.png')
			addDir(translate(30404),'1',2,addonfolder+artfolder+'digster.png')
			addDir(translate(30405),'1',7,addonfolder+artfolder+'charts.png')
			addDir(translate(30406),'1',17,addonfolder+artfolder+'search.png')
			addDir(translate(30407),'1',28,addonfolder+artfolder+'mymusic.png')
			addDir(translate(30408),'',31,addonfolder+artfolder+'favorites.png')
			addDir(translate(30409),'',35,addonfolder+artfolder+'configs.png',False)

###################################################################################
#RECOMENDATIONS

def Recomendations(url):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=chart.getTopTracks&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['tracks']['track'])):
		artist = decoded_data['tracks']['track'][x]['artist']['name'].encode("utf8")
		track_name = decoded_data['tracks']['track'][x]['name'].encode("utf8")
		try: iconimage = decoded_data['tracks']['track'][x]['image'][3]['#text'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
	total_pages = decoded_data['tracks']['@attr']['totalPages']
	if int(url)<int(total_pages): addDir(translate(30410),str(int(url)+1),1,addonfolder+artfolder+'next.png')

###################################################################################
#DIGSTER	

def Digster_menu():
	addDir('[COLOR blue][B]'+translate(30109)+':[/B][/COLOR] '+['Adria','Australia','Austria','Belgium','Denmark','Estonia','Finland','France','Germany','Latvia','Lithuania','Mexico','Netherlands','New Zeland','Norway','Poland','Portugal','Romania','Spain','Sweden','Switzerland','United Kingdom','USA'][int(selfAddon.getSetting('digster_country'))],'',2,'',False)
	addDir(translate(30450),'',3,'')
	addDir(translate(30451),'genre',4,'')
	addDir(translate(30452),'mood',4,'')
	addDir(translate(30453),'suitable',4,'')

def Digster_sections():
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/sections')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['sections'])):
		slug = decoded_data['sections'][x]['slug'].encode("utf8")
		title = decoded_data['sections'][x]['name'].encode("utf8")
		addDir(title,'1',5,'',search_query = '&section='+slug)

def Digster_categories(url):
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/taxonomies/'+url)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['taxonomy'])):
		slug = decoded_data['taxonomy'][x]['slug'].encode("utf8")
		title = decoded_data['taxonomy'][x]['title'].encode("utf8").replace("&amp;", "&")
		addDir(title,'1',5,'',search_query = '&'+url+'='+slug)

def List_digster_playlists(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists?posts_per_page='+str(items_per_page)+'&paged='+str(url)+search_query)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['playlists'])):
		slug = decoded_data['playlists'][x]['slug'].encode("utf8")
		title = decoded_data['playlists'][x]['title'].encode("utf8")
		try: iconimage = decoded_data['playlists'][x]['image']['large'][0].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir(title,slug,6,iconimage)
	#check if next page exist
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists?posts_per_page='+str(items_per_page)+'&paged='+str(int(url)+1)+search_query)
	decoded_data = json.loads(codigo_fonte)
	if len(decoded_data['playlists'])>0: addDir(translate(30410),str(int(url)+1),5,addonfolder+artfolder+'next.png',search_query = search_query)

def List_digster_tracks(url):
	digster_domain = ['http://digster-adria.com/','http://www.digster.com.au/','http://www.digster.at/','http://nl.digster.be/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://www.digster.fr/','http://www.digsterplaylist.de/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://dev9.digster.umdev.se/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/','http://www.digster.se/','http://www.digster.ch/','http://www.digster.co.uk/','http://www.digster.fm/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists/'+url)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['playlist']['tracks'])):
		if len(decoded_data['playlist']['tracks'][x]['artists'])==1: artist = decoded_data['playlist']['tracks'][x]['artists'][0].encode("utf8")
		elif len(decoded_data['playlist']['tracks'][x]['artists'])==2: artist = decoded_data['playlist']['tracks'][x]['artists'][0].encode("utf8")+' feat. '+decoded_data['playlist']['tracks'][x]['artists'][1].encode("utf8")
		elif len(decoded_data['playlist']['tracks'][x]['artists'])>2:
			artist = ''
			for y in range(0, len(decoded_data['playlist']['tracks'][x]['artists'])): artist = artist+decoded_data['playlist']['tracks'][x]['artists'][y].encode("utf8")+' & '
			artist = artist[:-3] # remove last ' & '
		track_name = decoded_data['playlist']['tracks'][x]['title'].encode("utf8")
		iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)

###################################################################################
#CHARTS

def Top_charts_menu():
	addDir(translate(30500),'1',8,'')
	addDir(translate(30501),'1',9,'')
	addDir(translate(30502),'1',15,'')
	addDir(translate(30503),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/hot-100')
	addDir(translate(30504),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/billboard-200')
	addDir(translate(30505),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/heatseekers-songs')
	addDir(translate(30506),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/heatseekers-albums')
	addDir(translate(30507),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/pop-songs')
	addDir(translate(30508),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/country-songs')
	addDir(translate(30509),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/country-albums')
	addDir(translate(30510),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/rock-songs')
	addDir(translate(30511),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/rock-albums')
	addDir(translate(30512),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/r-b-hip-hop-songs')
	addDir(translate(30513),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/r-b-hip-hop-albums')
	addDir(translate(30514),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/hot-r-and-b-hip-hop-airplay')
	addDir(translate(30515),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/dance-electronic-albums')
	addDir(translate(30516),'1',13,'',playlist_id = 'http://www.billboard.com/rss/charts/latin-songs')
	addDir(translate(30517),'1',14,'',playlist_id = 'http://www.billboard.com/rss/charts/latin-albums')

def Itunes_countries_menu(mode):
	country_name = ["Albania","Algeria","Angola","Anguilla","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Botswana","Brazil","British Virgin Islands","Brunei Darussalam","Bulgaria","Burkina Faso","Cambodia","Canada","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo, Republic of the","Costa Rica","Croatia","Cyprus","Czech Republic","Denmark","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia","Fiji","Finland","France","Gambia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea-Bissau","Guyana","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Korea, Republic Of","Kuwait","Kyrgyzstan","Lao, People's Democratic Republic","Latvia","Lebanon","Liberia","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Mali","Malta","Mauritania","Mauritius","Mexico","Micronesia, Federated States of","Moldova","Mongolia","Montserrat","Mozambique","Namibia","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Saudi Arabia","Senegal","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","South Africa","Spain","Sri Lanka","St. Kitts and Nevis","St. Lucia","St. Vincent and The Grenadines","Suriname","Swaziland","Sweden","Switzerland","São Tomé and Príncipe","Taiwan","Tajikistan","Tanzania","Thailand","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Venezuela","Vietnam","Yemen","Zimbabwe"]
	country_code = ["al","dz","ao","ai","ag","ar","am","au","at","az","bs","bh","bb","by","be","bz","bj","bm","bt","bo","bw","br","vg","bn","bg","bf","kh","ca","cv","ky","td","cl","cn","co","cg","cr","hr","cy","cz","dk","dm","do","ec","eg","sv","ee","fj","fi","fr","gm","de","gh","gr","gd","gt","gw","gy","hn","hk","hu","is","in","id","ie","ir","it","jm","jp","jo","kz","ke","kr","kw","kg","la","lv","lb","lr","lt","lu","mo","mk","mg","mw","my","ml","mt","mr","mu","mx","fm","md","mn","ms","mz","na","np","nl","nz","ni","ne","ng","no","om","pk","pw","pa","pg","py","pe","ph","pl","pt","qa","ro","ru","sa","sn","sc","sl","sg","sk","si","sb","za","es","lk","kn","lc","vc","sr","sz","se","ch","st","tw","tj","tz","th","tt","tn","tr","tm","tc","ug","ua","ae","gb","us","uy","uz","ve","vn","ye","zw"]
	for x in range(0, len(country_name)):
		if country_code[x] not in ["al","dz","ao","bj","bt","td","cn","cg","gy","is","jm","kr","kw","lr","mk","mg","mw","ml","mr","ms","pk","pw","sn","sc","sl","sb","lc","vc","sr","st","tz","tn","tc","uy","ye"]: #Countries without music store
			if mode==8: addDir(country_name[x],'1',10,'http://www.geonames.org/flags/x/'+country_code[x]+'.gif',country = country_code[x])
			elif mode==9: addDir(country_name[x],'1',11,'http://www.geonames.org/flags/x/'+country_code[x]+'.gif',country = country_code[x])

def Itunes_track_charts(url,country):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://itunes.apple.com/'+country+'/rss/topsongs/limit=100/explicit=true/json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		artist = decoded_data['feed']['entry'][x]['im:artist']['label'].encode("utf8")
		track_name = decoded_data['feed']['entry'][x]['im:name']['label'].encode("utf8")
		try: iconimage = decoded_data['feed']['entry'][x]['im:image'][2]['label'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
	if int(int(url)*items_per_page)<300: addDir(translate(30410),str(int(url)+1),10,addonfolder+artfolder+'next.png',country = country)

def Itunes_album_charts(url,country):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://itunes.apple.com/'+country+'/rss/topalbums/limit=100/explicit=true/json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		artist = decoded_data['feed']['entry'][x]['im:artist']['label'].encode("utf8")
		album_name = decoded_data['feed']['entry'][x]['im:name']['label'].encode("utf8")
		id = decoded_data['feed']['entry'][x]['id']['attributes']['im:id'].encode("utf8")
		try: iconimage = decoded_data['feed']['entry'][x]['im:image'][2]['label'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+artist+'[/B] - '+album_name,id,12,iconimage,album = album_name,artist = artist,country = country,type = 'album')
	if int(int(url)*items_per_page)<300: addDir(translate(30410),str(int(url)+1),14,addonfolder+artfolder+'next.png',country = country)

def Itunes_list_album_tracks(url,album,country):
	#api documentation: https://www.apple.com/itunes/affiliates/resources/documentation/itunes-store-web-service-search-api.html
	codigo_fonte = abrir_url('https://itunes.apple.com/lookup?id='+url+'&country='+country+'&entity=song&limit=200')
	decoded_data = json.loads(codigo_fonte)
	try:
		if int(decoded_data['resultCount'])>0:
			for x in range(1, len(decoded_data['results'])):
				artist = decoded_data['results'][x]['artistName'].encode("utf8")
				track_name = decoded_data['results'][x]['trackName'].encode("utf8")
				try: iconimage = decoded_data['results'][x]['artworkUrl100'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
	except: pass
		
def Billboard_charts(url,mode,playlist_id):
	#if mode==13: list billboard track charts
	#if mode==14: list billboard album charts
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str(int(url)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
	decoded_data = json.loads(codigo_fonte)
	try:
		if len(decoded_data['query']['results']['item']) > 0:
			if mode==13:
				#checks if output has only an object or various and proceeds according
				if 'artist' in decoded_data['query']['results']['item'] and 'chart_item_title' in decoded_data['query']['results']['item']:
					artist = decoded_data['query']['results']['item']['artist'].encode("utf8")
					track_name = decoded_data['query']['results']['item']['chart_item_title'].encode("utf8")
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',29,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',18,addonfolder+artfolder+'no_cover.png',search_query = artist+' '+track_name)
				else:
					for x in range(0, len(decoded_data['query']['results']['item'])):
						artist = decoded_data['query']['results']['item'][x]['artist'].encode("utf8")
						track_name = decoded_data['query']['results']['item'][x]['chart_item_title'].encode("utf8")
						if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',29,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,type = 'song')
						elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',18,addonfolder+artfolder+'no_cover.png',search_query = artist+' '+track_name)
			elif mode==14:
				#checks if output has only an object or various and proceeds according
				if 'artist' in decoded_data['query']['results']['item'] and 'chart_item_title' in decoded_data['query']['results']['item']:
					artist = decoded_data['query']['results']['item']['artist'].encode("utf8")
					track_name = decoded_data['query']['results']['item']['chart_item_title'].encode("utf8")
					addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',20,addonfolder+artfolder+'no_cover.png',artist = artist,album = album_name,type = 'album')
				else:
					for x in range(0, len(decoded_data['query']['results']['item'])):
						artist = decoded_data['query']['results']['item'][x]['artist'].encode("utf8")
						album_name = decoded_data['query']['results']['item'][x]['chart_item_title'].encode("utf8")
						addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',20,addonfolder+artfolder+'no_cover.png',artist = artist,album = album_name,type = 'album')
	except: pass
	try:
		codigo_fonte_2 = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str((int(url)+1)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
		decoded_data_2 = json.loads(codigo_fonte_2)
		if len(decoded_data_2['query']['results']['item']) > 0: addDir(translate(30410),str(int(url)+1),mode,addonfolder+artfolder+'next.png',playlist_id = playlist_id)
	except: pass

def Officialcharts_uk(url,mode,playlist_id):
	if playlist_id==None or playlist_id=='':
		options_name = ['Singles','Albums','Singles Update','Albums Update','Dance Singles','Dance Albums','Indie Singles','Indie Albums','RnB Singles','RnB Albums','Rock Singles','Rock Albums','Compilations Albums']
		options_mode = [15,16,15,16,15,16,15,16,15,16,15,16,16]
		options_playlist_id = ['http://www.bbc.co.uk/radio1/chart/singles','http://www.bbc.co.uk/radio1/chart/albums','http://www.bbc.co.uk/radio1/chart/updatesingles','http://www.bbc.co.uk/radio1/chart/updatealbums','http://www.bbc.co.uk/radio1/chart/dancesingles','http://www.bbc.co.uk/radio1/chart/dancealbums','http://www.bbc.co.uk/radio1/chart/indiesingles','http://www.bbc.co.uk/radio1/chart/indiealbums','http://www.bbc.co.uk/radio1/chart/rnbsingles','http://www.bbc.co.uk/radio1/chart/rnbalbums','http://www.bbc.co.uk/radio1/chart/rocksingles','http://www.bbc.co.uk/radio1/chart/rockalbums','http://www.bbc.co.uk/radio1/chart/compilations']
		id = xbmcgui.Dialog().select(translate(30518), options_name)
		if id != -1:
			mode = options_mode[id]
			playlist_id = options_playlist_id[id]
		else:
			sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM html(' + str(int(url)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '" and xpath="//div[@class=\'cht-content-wrapper\']/div[@class=\'cht-content\']/div[@class=\'cht-entries\']/div[@class=\'cht-entry-wrapper\']"') + '&format=json&diagnostics=true&callback=', timeout=30)
	decoded_data = json.loads(codigo_fonte)
	try:
		if len(decoded_data['query']['results']['div']) > 0:
			if url=='1': addDir(translate(30519),'1',15,'')
			if mode==15:
				#checks if output has only an object or various and proceeds according
				if 'div' in decoded_data['query']['results']['div'] and 'img' in decoded_data['query']['results']['div']:
					try: artist = decoded_data['query']['results']['div']['div'][1]['div'][0]['p'].encode("utf8")
					except: artist = decoded_data['query']['results']['div']['div']['div'][1]['div'][0]['p'].encode("utf8")
					try: track_name = decoded_data['query']['results']['div']['div']['div'][1]['div'][1]['p'].encode("utf8")
					except: track_name = decoded_data['query']['results']['div']['div'][1]['div'][1]['p'].encode("utf8")
					try: iconimage = decoded_data['query']['results']['div']['img']['src'].encode("utf8")
					except: 
						try: iconimage = decoded_data['query']['results']['div']['div']['img']['src'].encode("utf8")
						except: iconimage = addonfolder+artfolder+'no_cover.png'
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
				else:
					for x in range(0, len(decoded_data['query']['results']['div'])):
						try: artist = decoded_data['query']['results']['div'][x]['div'][1]['div'][0]['p'].encode("utf8")
						except: artist = decoded_data['query']['results']['div'][x]['div']['div'][1]['div'][0]['p'].encode("utf8")
						try: track_name = decoded_data['query']['results']['div'][x]['div']['div'][1]['div'][1]['p'].encode("utf8")
						except: track_name = decoded_data['query']['results']['div'][x]['div'][1]['div'][1]['p'].encode("utf8")
						try: iconimage = decoded_data['query']['results']['div'][x]['img']['src'].encode("utf8")
						except: 
							try: iconimage = decoded_data['query']['results']['div'][x]['div']['img']['src'].encode("utf8")
							except: iconimage = addonfolder+artfolder+'no_cover.png'
						if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
						elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
			elif mode==16:
				#checks if output has only an object or various and proceeds according
				if 'div' in decoded_data['query']['results']['div'] and 'img' in decoded_data['query']['results']['div']:
					try: artist = decoded_data['query']['results']['div']['div'][1]['div'][0]['p'].encode("utf8")
					except: artist = decoded_data['query']['results']['div']['div']['div'][1]['div'][0]['p'].encode("utf8")
					try: album_name = decoded_data['query']['results']['div']['div']['div'][1]['div'][1]['p'].encode("utf8")
					except: album_name = decoded_data['query']['results']['div']['div'][1]['div'][1]['p'].encode("utf8")
					try: iconimage = decoded_data['query']['results']['div']['img']['src'].encode("utf8")
					except: 
						try: iconimage = decoded_data['query']['results']['div']['div']['img']['src'].encode("utf8")
						except: iconimage = addonfolder+artfolder+'no_cover.png'
					addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',20,iconimage,artist = artist,album = album_name,type = 'album')
				else:
					for x in range(0, len(decoded_data['query']['results']['div'])):
						try: artist = decoded_data['query']['results']['div'][x]['div'][1]['div'][0]['p'].encode("utf8")
						except: artist = decoded_data['query']['results']['div'][x]['div']['div'][1]['div'][0]['p'].encode("utf8")
						try: album_name = decoded_data['query']['results']['div'][x]['div']['div'][1]['div'][1]['p'].encode("utf8")
						except: album_name = decoded_data['query']['results']['div'][x]['div'][1]['div'][1]['p'].encode("utf8")
						try: iconimage = decoded_data['query']['results']['div'][x]['img']['src'].encode("utf8")
						except:
							try: iconimage = decoded_data['query']['results']['div'][x]['div']['img']['src'].encode("utf8")
							except: iconimage = addonfolder+artfolder+'no_cover.png'
						addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',20,iconimage,artist = artist,album = album_name,type = 'album')
	except: pass
	try:
		codigo_fonte_2 = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM html(' + str((int(url)+1)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '" and xpath="//div[@class=\'cht-content-wrapper\']/div[@class=\'cht-content\']/div[@class=\'cht-entries\']/div[@class=\'cht-entry-wrapper\']"') + '&format=json&diagnostics=true&callback=', timeout=30)
		decoded_data_2 = json.loads(codigo_fonte_2)
		if len(decoded_data_2['query']['results']['div']) > 0: addDir(translate(30410),str(int(url)+1),mode,addonfolder+artfolder+'next.png',playlist_id = playlist_id)
	except: pass

###################################################################################
#SEARCH AND LIST CONTENT

def Search_main():
	keyb = xbmc.Keyboard('', translate(30600))
	keyb.doModal()
	if (keyb.isConfirmed()):
		search_query = keyb.getText()
		if search_query=='': sys.exit(0)
	else: sys.exit(0)
	if search_query.startswith('tags:'):
		if search_query!='tags:':
			#playlists by tags
			codigo_fonte = abrir_url('http://8tracks.com/mix_sets/tags:'+urllib.quote(search_query[5:].replace(', ', '+').replace(',', '+'))+'.json?include=mixes+pagination'+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
			decoded_data = json.loads(codigo_fonte)
			total_items = decoded_data['total_entries']
			if total_items>0: addDir(translate(30609)+str(total_items)+translate(30610),'1',24,'',search_query = search_query)
	else:
		#tracks
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(search_query)+'&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		total_items = decoded_data['response'][0]
		if int(total_items)>0: addDir(translate(30601)+str(total_items)+translate(30602),'1',18,'',search_query = search_query)
		#albums
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: decoded_data['error']
		except:
			try: total_items = decoded_data['topalbums']['@attr']['total']
			except: total_items = decoded_data['topalbums']['total']
			if int(total_items)>0: addDir(translate(30603)+str(total_items)+translate(30604),'1',19,'',search_query = search_query)
		#toptracks
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.getTopTracks&artist='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: total_items = decoded_data['toptracks']['@attr']['total']
		except:
			try: total_items = decoded_data['toptracks']['total']
			except: total_items = 0
		if int(total_items)>0: addDir(translate(30605)+str(total_items)+translate(30606),'1',21,'',search_query = search_query)
		#setlists
		try: codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/search/setlists.json?artistName='+urllib.quote(search_query))
		except urllib2.URLError, e: codigo_fonte = "not found"
		if codigo_fonte != "not found":
			decoded_data = json.loads(codigo_fonte)
			total_items = decoded_data['setlists']['@total']
			addDir(translate(30607)+str(total_items)+translate(30608),'1',22,'',search_query = search_query)
		#playlists
		codigo_fonte = abrir_url('http://8tracks.com/mix_sets/keyword:'+urllib.quote(search_query)+'.json?include=mixes+pagination'+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
		decoded_data = json.loads(codigo_fonte)
		total_items = decoded_data['total_entries']
		if total_items>0: addDir(translate(30609)+str(total_items)+translate(30610),'1',24,'',search_query = search_query)

def Search_by_tracks(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	index = ((int(url)-1)*items_per_page)
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(search_query)+'&count='+str(items_per_page)+'&offset='+str(index)+'&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	for x in range(1, len(decoded_data['response'])):
		artist = decoded_data['response'][x]['artist'].encode("utf8").replace("&amp;", "&")
		track_name = decoded_data['response'][x]['title'].encode("utf8")
		link = decoded_data['response'][x]['url'].encode("utf8")
		item_id = str(decoded_data['response'][x]['owner_id'])+'_'+str(decoded_data['response'][x]['aid'])
		addLink('[B]'+artist+'[/B] - '+track_name,link,29,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,item_id = item_id,manualsearch = False,type = 'song')
	total_items = decoded_data['response'][0]
	if index+items_per_page<int(total_items): addDir(translate(30410),str(int(url)+1),18,addonfolder+artfolder+'next.png',search_query = search_query)
	
def Search_by_albums(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist='+urllib.quote(search_query)+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		for x in range(0, len(decoded_data['topalbums']['album'])):
			artist = decoded_data['topalbums']['album'][x]['artist']['name'].encode("utf8")
			album_name = decoded_data['topalbums']['album'][x]['name'].encode("utf8")
			mbid = decoded_data['topalbums']['album'][x]['mbid'].encode("utf8")
			try: iconimage = decoded_data['topalbums']['album'][x]['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir('[B]'+artist+'[/B] - '+album_name,mbid,20,iconimage,artist = artist,album = album_name,type = 'album')
		total_pages = decoded_data['topalbums']['@attr']['totalPages']
		if int(url)<int(total_pages): addDir(translate(30410),str(int(url)+1),19,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass

def List_album_tracks(url,artist,album):
	if url: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.getInfo&mbid='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	else: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.getInfo&artist='+urllib.quote(artist)+'&album='+urllib.quote(album)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	count = 0
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['album']['tracks']['track']:
			artist = decoded_data['album']['tracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['album']['tracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['album']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
			count += 1
		else:
			for x in range(0, len(decoded_data['album']['tracks']['track'])):
				artist = decoded_data['album']['tracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['album']['tracks']['track'][x]['name'].encode("utf8")
				try: iconimage = decoded_data['album']['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
				count += 1
	except: pass
	#if none result was found with last.fm api, we use 7digital api
	if artist and album and count==0:
		try:
			codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM xml WHERE url="http://api.7digital.com/1.2/release/search?q='+urllib.quote(artist+' '+album)+'&type=album&oauth_consumer_key=musichackday"') + '&format=json&diagnostics=true&callback=', timeout=30)
			decoded_data = json.loads(codigo_fonte)
			releaseid_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['id']
			title_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['title']
			artist_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['artist']['name']
			codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM xml WHERE url="http://api.7digital.com/1.2/release/tracks?releaseid='+releaseid_xml+'&oauth_consumer_key=musichackday&country=GB"') + '&format=json&diagnostics=true&callback=', timeout=30)
			decoded_data = json.loads(codigo_fonte)
			if artist.lower() == artist_xml.lower():
				for x in range(0, len(decoded_data['query']['results']['response']['tracks']['track'])):
					artist = decoded_data['query']['results']['response']['tracks']['track'][x]['artist']['name'].encode("utf8")
					track_name = decoded_data['query']['results']['response']['tracks']['track'][x]['title'].encode("utf8")
					try: iconimage = decoded_data['query']['results']['response']['tracks']['track'][x]['release']['image'].encode("utf8")
					except: iconimage = addonfolder+artfolder+'no_cover.png'
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
					count += 1
		except: pass

def Search_by_toptracks(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.getTopTracks&artist='+urllib.quote(search_query)+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['toptracks']['track']:
			artist = decoded_data['toptracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['toptracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['toptracks']['track']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['toptracks']['track'])):
				artist = decoded_data['toptracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['toptracks']['track'][x]['name'].encode("utf8")
				#mbid = decoded_data['toptracks']['track'][x]['mbid'].encode("utf8")
				try: iconimage = decoded_data['toptracks']['track'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
			total_pages = decoded_data['toptracks']['@attr']['totalPages']
			if int(url)<int(total_pages): addDir(translate(30410),str(int(url)+1),21,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass

def Search_by_setlists(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = 20 #impossible to use a custom value currently
	codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/search/setlists.json?artistName='+urllib.quote(search_query)+'&p='+url)
	if codigo_fonte != "not found":
		decoded_data = json.loads(codigo_fonte)
		try:
			#checks if output has only an object or various and proceeds according
			if 'artist' in decoded_data['setlists']['setlist']:
				date = decoded_data['setlists']['setlist']['@eventDate'].encode("utf8")
				artist = decoded_data['setlists']['setlist']['artist']['@name'].encode("utf8")
				location = decoded_data['setlists']['setlist']['venue']['@name'].encode("utf8")
				id = decoded_data['setlists']['setlist']['@id'].encode("utf8")
				iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+location+' ('+date+')',id,23,iconimage,type='setlist')
			else:
				for x in range(0, len(decoded_data['setlists']['setlist'])):
					date = decoded_data['setlists']['setlist'][x]['@eventDate'].encode("utf8")
					artist = decoded_data['setlists']['setlist'][x]['artist']['@name'].encode("utf8")
					location = decoded_data['setlists']['setlist'][x]['venue']['@name'].encode("utf8")
					id = decoded_data['setlists']['setlist'][x]['@id'].encode("utf8")
					iconimage = addonfolder+artfolder+'no_cover.png'
					addDir('[B]'+artist+'[/B] - '+location+' ('+date+')',id,23,iconimage,artist = artist,type='setlist')
				total_items = decoded_data['setlists']['@total']
				if int(url)*items_per_page<int(total_items): addDir(translate(30410),str(int(url)+1),22,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass

def List_setlist_tracks(url):
	codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/setlist/'+url+'.json')
	decoded_data = json.loads(codigo_fonte)
	try:
		artist = decoded_data['setlist']['artist']['@name'].encode("utf8")
		for x in range(0, len(decoded_data['setlist']['sets']['set']['song'])):
			track_name = decoded_data['setlist']['sets']['set']['song'][x]['@name'].encode("utf8")
			iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
	except: pass

def Search_8tracks_playlists(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30611))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	if search_query.startswith('tags:'): codigo_fonte = abrir_url('http://8tracks.com/mix_sets/tags:'+urllib.quote(search_query[5:].replace(', ', '+').replace(',', '+'))+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	else: codigo_fonte = abrir_url('http://8tracks.com/mix_sets/keyword:'+urllib.quote(search_query)+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['mixes'])):
		username = decoded_data['mixes'][x]['user']['login'].encode("utf8")
		playlist_name = decoded_data['mixes'][x]['name'].encode("utf8")
		tracks_count = str(decoded_data['mixes'][x]['tracks_count'])
		playlist_id = str(decoded_data['mixes'][x]['id'])
		try: iconimage = decoded_data['mixes'][x]['cover_urls']['max200'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+username+'[/B] - '+playlist_name+' [I]('+tracks_count+' tracks)[/I]','1',25,iconimage,playlist_id = playlist_id,type='playlist')
	total_pages = decoded_data['total_pages']
	if int(url)<int(total_pages): addDir(translate(30410),str(int(url)+1),24,addonfolder+artfolder+'next.png',search_query = search_query)

def List_8tracks_tracks(url,iconimage,playlist_id):
	#official resolver method - more stable but no cache
	if selfAddon.getSetting('playlist_resolver_method')=="0":
		last_track = 0
		total_tracks = int(json.loads(abrir_url('http://8tracks.com/mixes/'+playlist_id+'.json?api_key=e165128668b69291bf8081dd743fa6b832b4f477&api_version=3'))['mix']['tracks_count'])
		play_token = json.loads(abrir_url('http://8tracks.com/sets/new.json&api_key=e165128668b69291bf8081dd743fa6b832b4f477&api_version=3'))['play_token']
		progress = xbmcgui.DialogProgress()
		progress.create(translate(30400),translate(30612))
		progress.update(0)
		playlist = xbmc.PlayList(1)
		playlist.clear()
		if progress.iscanceled(): sys.exit(0)
		#load first track
		codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/play.json?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
		decoded_data = json.loads(codigo_fonte)
		progress.update(int(((0)*100)/(total_tracks)),translate(30612),translate(30613)+str(last_track+1)+translate(30614)+str(total_tracks))
		artist = decoded_data['set']['track']['performer'].encode("utf8")
		track_name = decoded_data['set']['track']['name'].encode("utf8")
		link = decoded_data['set']['track']['url'].encode("utf8")
		addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
		duration = int(decoded_data['set']['track']['play_duration'])
		listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
		listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
		playlist.add(link,listitem)
		if progress.iscanceled(): sys.exit(0)
		xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(playlist) #lets try to force a player to avoid no codec error
		#load remaining tracks
		if (last_track+1)<total_tracks:
			for x in range(last_track+1, total_tracks):
				try: codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477&format=jsonh&api_version=2')
				except urllib2.HTTPError, e: codigo_fonte = e.fp.read() #bypass 403 error
				decoded_data = json.loads(codigo_fonte)
				if progress.iscanceled(): sys.exit(0)
				try:
					progress.update(int(((x)*100)/(total_tracks)),translate(30612),translate(30613)+str(x+1)+translate(30614)+str(total_tracks))
					artist = decoded_data['set']['track']['performer'].encode("utf8")
					track_name = decoded_data['set']['track']['name'].encode("utf8")
					link = decoded_data['set']['track']['url'].encode("utf8")
					addLink('[B]'+artist+'[/B] - '+track_name,link,29,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
					duration = int(decoded_data['set']['track']['play_duration'])
					listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
					listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
					playlist.add(link,listitem)
					print 'Debug: carregado track '+str(x)+' from official2'
				except:
					if decoded_data['status']=='403 Forbidden':
						for y in range((duration/2)+7, 0, -1):
							time.sleep(1)
							progress.update(int(((x)*100)/(total_tracks)),translate(30612),translate(30613)+str(x+1)+translate(30614)+str(total_tracks),translate(30615)+str(y)+translate(30616))
							if progress.iscanceled(): sys.exit(0)
						try:
							try: codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477&format=jsonh&api_version=2')
							except urllib2.HTTPError, e: codigo_fonte = e.fp.read() #bypass 403 error
							decoded_data = json.loads(codigo_fonte)
							progress.update(int(((x)*100)/(total_tracks)),translate(30612),'Carregando track '+str(x+1)+' de '+str(total_tracks))
							artist = decoded_data['set']['track']['performer'].encode("utf8")
							track_name = decoded_data['set']['track']['name'].encode("utf8")
							link = decoded_data['set']['track']['url'].encode("utf8")
							addLink('[B]'+artist+'[/B] - '+track_name,link,29,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
							duration = int(decoded_data['set']['track']['play_duration'])
							listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
							listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
							playlist.add(link,listitem)
							print 'Debug: carregado track '+str(x)+' from official3'
						except:
							dialog = xbmcgui.Dialog()
							ok = dialog.ok(translate(30400), translate(30617))
							break
		if progress.iscanceled(): sys.exit(0)
		progress.update(100)
		progress.close()
	#omgcatz resolver method - with cache, faster in general
	if selfAddon.getSetting('playlist_resolver_method')=="1":
		# Get "correct" url from id
		req = urllib2.Request('https://8tracks.com/mixes/'+playlist_id+'/')
		res = urllib2.urlopen(req)
		playlist_url = res.geturl()
		# Let's use omgcatz to resolve and cache the playlist
		codigo_fonte = abrir_url_custom('http://omgcatz.com/run/fetch/eight.php', post = { 'url': playlist_url, 'playToken': '', 'mixId': '', 'trackNumber': '0' })
		decoded_data = json.loads(codigo_fonte)
		last_track = 0
		total_tracks = int(decoded_data['mix']['tracks_count'])
		progress = xbmcgui.DialogProgress()
		progress.create(translate(30400),translate(30618))
		progress.update(0)
		playlist = xbmc.PlayList(1)
		playlist.clear()
		if progress.iscanceled(): sys.exit(0)
		for x in range(0, total_tracks):
			try:
				last_track = x
				progress.update(int(((x)*100)/(total_tracks)),translate(30618),translate(30613)+str(last_track+1)+translate(30614)+str(total_tracks))
				artist = decoded_data[str(x)]['artist'].encode("utf8")
				track_name = decoded_data[str(x)]['title'].encode("utf8")
				link = decoded_data[str(x)]['songUrl'].encode("utf8")
				duration = int(decoded_data[str(x)]['duration'])
				addLink('[B]'+artist+'[/B] - '+track_name,link,29,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
				listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
				listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
				playlist.add(link,listitem)
				print 'Debug: carregado track '+str(x)+' from catz1'
			except:
				last_track = x-1
				break
		if progress.iscanceled(): sys.exit(0)
		xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(playlist) #lets try to force a player to avoid no codec error
		if (last_track+1)<total_tracks:
			play_token = decoded_data['play_token']
			mixId = str(decoded_data['mix']['id'])
			for x in range(last_track+1, total_tracks):
				codigo_fonte = abrir_url_custom('http://omgcatz.com/run/fetch/eight.php', post = { 'url': playlist_url, 'playToken': play_token, 'mixId': mixId, 'trackNumber': str(x) })
				decoded_data = json.loads(codigo_fonte)
				if progress.iscanceled(): sys.exit(0)
				try:
					progress.update(int(((x)*100)/(total_tracks)),translate(30618),translate(30613)+str(x+1)+translate(30614)+str(total_tracks))
					artist = decoded_data['0']['artist'].encode("utf8")
					track_name = decoded_data['0']['title'].encode("utf8")
					link = decoded_data['0']['songUrl'].encode("utf8")
					duration = int(decoded_data['0']['duration'])
					addLink('[B]'+artist+'[/B] - '+track_name,link,29,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
					listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
					listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
					playlist.add(link,listitem)
					print 'Debug: carregado track '+str(x)+' from catz2'
				except:
					if decoded_data['error']==403:
						for y in range((duration/2)+7, 0, -1):
							time.sleep(1)
							progress.update(int(((x)*100)/(total_tracks)),translate(30618),translate(30613)+str(x+1)+translate(30614)+str(total_tracks),translate(30615)+str(y)+translate(30616))
							if progress.iscanceled(): sys.exit(0)
						try:
							codigo_fonte = abrir_url_custom('http://omgcatz.com/run/fetch/eight.php', post = { 'url': playlist_url, 'playToken': play_token, 'mixId': mixId, 'trackNumber': str(x) })
							decoded_data = json.loads(codigo_fonte)
							artist = decoded_data['0']['artist'].encode("utf8")
							track_name = decoded_data['0']['title'].encode("utf8")
							link = decoded_data['0']['songUrl'].encode("utf8")
							duration = int(decoded_data['0']['duration'])
							addLink('[B]'+artist+'[/B] - '+track_name,link,29,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,type = 'song')
							listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
							listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
							playlist.add(link,listitem)
							print 'Debug: carregado track '+str(x)+' from catz3'
						except:
							if decoded_data['error']==403:
								dialog = xbmcgui.Dialog()
								ok = dialog.ok(translate(30400), translate(30619))
								break
		if progress.iscanceled(): sys.exit(0)
		progress.update(100)
		progress.close()

def Search_by_similartracks(artist,track_name):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=track.getSimilar&artist='+urllib.quote(artist)+'&track='+urllib.quote(track_name)+'&limit='+str(items_per_page)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['similartracks']['track']:
			artist = decoded_data['similartracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['similartracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['similartracks']['track']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['similartracks']['track'])):
				artist = decoded_data['similartracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['similartracks']['track'][x]['name'].encode("utf8")
				try: iconimage = decoded_data['similartracks']['track'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',29,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name)
	except: pass

def Search_videoclip(artist,track_name):
	try:	
		search_string = urllib.quote(artist + ' ' + track_name + ' music video')
		codigo_fonte = abrir_url("http://gdata.youtube.com/feeds/api/videos?q="+ search_string +"&key=AIzaSyBbDY0UzvF5Es77M7S1UChMzNp0KsbaDPI&alt=json&max-results=1")
	except: codigo_fonte = ''
	if codigo_fonte:
		try:
			codigo_fonte = eval(codigo_fonte)
			video_url = codigo_fonte["feed"]["entry"][0]["media$group"]['media$content'][0]['url']
			match = re.compile('v/(.+?)\?').findall(video_url)
		except: match = []
		if match: print 'playing video youtube id',match[0];xbmc.Player().play("plugin://plugin.video.youtube?action=play_video&videoid="+match[0])
		else: 
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400), translate(30620))

###################################################################################
#DOWNLOADS AND RESOLVERS

def List_my_songs():
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30800))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		dirs = os.listdir(selfAddon.getSetting('downloads_folder'))
		for file in dirs:
			extension = os.path.splitext(file)[1]
			if extension == '.mp3' or extension == '.m4a': addLink(file,os.path.join(selfAddon.getSetting('downloads_folder'), file),29,addonfolder+artfolder+'no_cover.png',type = 'mymusic')

def Get_songfile_from_name(artist,track_name):
	codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(artist+' '+track_name)+'&access_token='+selfAddon.getSetting("vk_token"))
	decoded_data = json.loads(codigo_fonte)
	try: return decoded_data['response'][1]['url'].encode("utf8")
	except: return 'track_not_found'

def Resolve_songfile(url,artist,track_name,album,iconimage):
	#if a url is provided, the function reproduce it
	#else it gets the file from vk.com API using the artist and track_name info
	success = True
	if url=='' or url==None:
		progress = xbmcgui.DialogProgress()
		progress.create(translate(30400),translate(30801))
		progress.update(0)
		codigo_fonte = abrir_url('https://api.vk.com/method/audio.search.json?q='+urllib.quote(artist+' '+track_name)+'&access_token='+selfAddon.getSetting("vk_token"))
		decoded_data = json.loads(codigo_fonte)
		try: url=decoded_data['response'][1]['url'].encode("utf8")
		except:
			url=''
			success = False
		if progress.iscanceled(): sys.exit(0)
		progress.update(100)
		progress.close()
		item = xbmcgui.ListItem(path=url)
		item.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)
	else:
		item = xbmcgui.ListItem(path=url)
		item.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)

def Download_songfile(name,url,artist,track_name):
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30800))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		if url=="track_not_found":
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400),translate(30802))
			return
		elif url=='':
			url = Get_songfile_from_name(artist,track_name)
			if url=="track_not_found":
				dialog = xbmcgui.Dialog()
				ok = dialog.ok(translate(30400),translate(30802))
				return
		#get file extension
		if url.endswith('.m4a'): file_extension = '.m4a'
		else: file_extension = '.mp3'
		#correct the name - remove top track position and tags/labels
		regexfix = re.search('^\[COLOR yellow\][\d]+?\[/COLOR\] \-(.+?)$', name)
		if regexfix: name = regexfix.group(1)
		name = re.sub("\[/?(?:COLOR|B|I)[^]]*\]", "", name)
		name = re.sub('[<>:"/\|?*]', '', name) #remove not allowed characters in the filename
		params = { "url": url, "download_path": selfAddon.getSetting('downloads_folder'), "Title": name }
		downloader.download(name.decode("utf-8")+file_extension, params, async=False)

###################################################################################
#FAVORITES

def Favorites_menu():
	addDir(translate(30701),'songs',32,'')
	addDir(translate(30702),'albums',32,'')
	addDir(translate(30703),'setlists',32,'')
	addDir(translate(30704),'playlists',32,'')

def List_favorites(url):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile): save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"songs\": []\n}")
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if url=='songs':
		for x in range(0, len(decoded_data['songs'])):
			if decoded_data['songs'][x]['type'].encode("utf8")=='vk.com': #get the direct link for a specific vk.com audio file id
				artist = decoded_data['songs'][x]['artist'].encode("utf8")
				track_name = decoded_data['songs'][x]['track_name'].encode("utf8")
				item_id = decoded_data['songs'][x]['item_id'].encode("utf8")
				try: url = json.loads(abrir_url('https://api.vk.com/method/audio.getById.json?audios='+item_id+'&access_token='+selfAddon.getSetting("vk_token")))['response'][0]['url'].encode("utf8")
				except: url = ''
				if decoded_data['songs'][x]['iconimage']: iconimage = decoded_data['songs'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addLink('[B]'+artist+'[/B] - '+track_name,url,29,iconimage,artist = artist,track_name = track_name,manualsearch = False,item_id = str(x),type='fav_song')
			elif decoded_data['songs'][x]['type'].encode("utf8")=='default': #call default song resolver method
				artist = decoded_data['songs'][x]['artist'].encode("utf8")
				track_name = decoded_data['songs'][x]['track_name'].encode("utf8")
				url = decoded_data['songs'][x]['url'].encode("utf8")
				if decoded_data['songs'][x]['iconimage']: iconimage = decoded_data['songs'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				if url or selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,url,29,iconimage,artist = artist,track_name = track_name,item_id = str(x),type='fav_song')
				else: addDir('[B]'+artist+'[/B] - '+track_name,'1',18,iconimage,search_query = artist+' '+track_name,item_id = str(x),type='fav_song')
	elif url=='albums':
		for x in range(0, len(decoded_data['albums'])):
			if decoded_data['albums'][x]['provider'].encode("utf8")=='itunes': #albums from itunes charts
				artist = decoded_data['albums'][x]['artist'].encode("utf8")
				album = decoded_data['albums'][x]['album'].encode("utf8")
				country = decoded_data['albums'][x]['country'].encode("utf8")
				url = decoded_data['albums'][x]['url'].encode("utf8")
				if decoded_data['albums'][x]['iconimage']: iconimage = decoded_data['albums'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album,url,12,iconimage,album = album,artist = artist,country = country,item_id = str(x),type='fav_album')
			elif decoded_data['albums'][x]['provider'].encode("utf8")=='default': #other albums from last.fm/7digital
				artist = decoded_data['albums'][x]['artist'].encode("utf8")
				album = decoded_data['albums'][x]['album'].encode("utf8")
				url = decoded_data['albums'][x]['url'].encode("utf8")
				if decoded_data['albums'][x]['iconimage']: iconimage = decoded_data['albums'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album,url,20,iconimage,artist = artist,album = album,item_id = str(x),type='fav_album')
	elif url=='setlists':
		for x in range(0, len(decoded_data['setlists'])):
			name = decoded_data['setlists'][x]['name'].encode("utf8")
			artist = decoded_data['setlists'][x]['artist'].encode("utf8")
			url = decoded_data['setlists'][x]['url'].encode("utf8")
			if decoded_data['setlists'][x]['iconimage']: iconimage = decoded_data['setlists'][x]['iconimage'].encode("utf8")
			else: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir(name,url,23,iconimage,artist = artist,item_id = str(x),type='fav_setlist')
	elif url=='playlists':
		for x in range(0, len(decoded_data['playlists'])):
			name = decoded_data['playlists'][x]['name'].encode("utf8")
			playlist_id = decoded_data['playlists'][x]['playlist_id'].encode("utf8")
			if decoded_data['playlists'][x]['iconimage']: iconimage = decoded_data['playlists'][x]['iconimage'].encode("utf8")
			else: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir(name,'1',25,iconimage,playlist_id = playlist_id,item_id = str(x),type='fav_playlist')

def Add_to_favorites(type,artist,album,country,name,playlist_id,track_name,url,iconimage,item_id):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile): save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"songs\": []\n}")
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if iconimage == addonfolder+artfolder+'no_cover.png': iconimage = None
	if type=='song':
		# vk.com mp3 url expires (is ip restricted), so is necessary use ids to save and restore music in favorites
		if item_id: decoded_data["songs"].append({"type": 'vk.com',"artist": artist,"track_name": track_name,"item_id": item_id,"iconimage": iconimage})
		# if is not a vk.com direct link, we use the default method to store in favorites
		else: decoded_data["songs"].append({"type": 'default',"artist": artist,"track_name": track_name,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification('[B]'+artist+'[/B] - '+track_name,translate(30700),'4000',iconimage)
	elif type=='album':
		#albums from itunes charts
		if country: decoded_data["albums"].append({"provider": 'itunes',"artist": artist,"album": album,"country": country,"url": url,"iconimage": iconimage})
		#other albums from last.fm/7digital
		else: decoded_data["albums"].append({"provider": 'default',"artist": artist,"album": album,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification('[B]'+artist+'[/B] - '+album,translate(30700),'4000',iconimage)
	elif type=='setlist':
		decoded_data["setlists"].append({"name": name,"artist": artist,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification(name,translate(30700),'4000',iconimage)
	elif type=='playlist':
		decoded_data["playlists"].append({"name": name,"playlist_id": playlist_id,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification(name,translate(30700),'4000',iconimage)

def Edit_favorites(url,type,item_id):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile):
		save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"songs\": []\n}")
		return
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if url=='moveup':#move up the item
		if type=='fav_song':
			if int(item_id)==0: decoded_data["songs"].insert(len(decoded_data["songs"])+1, decoded_data["songs"].pop(int(item_id)))
			else: decoded_data["songs"].insert(int(item_id)-1, decoded_data["songs"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			if int(item_id)==0: decoded_data["albums"].insert(len(decoded_data["albums"])+1, decoded_data["albums"].pop(int(item_id)))
			else: decoded_data["albums"].insert(int(item_id)-1, decoded_data["albums"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			if int(item_id)==0: decoded_data["setlists"].insert(len(decoded_data["setlists"])+1, decoded_data["setlists"].pop(int(item_id)))
			else: decoded_data["setlists"].insert(int(item_id)-1, decoded_data["setlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			if int(item_id)==0: decoded_data["playlists"].insert(len(decoded_data["playlists"])+1, decoded_data["playlists"].pop(int(item_id)))
			else: decoded_data["playlists"].insert(int(item_id)-1, decoded_data["playlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	elif url=='movedown':#move down the item
		if type=='fav_song':
			if int(item_id)==(len(decoded_data["songs"])-1): decoded_data["songs"].insert(0, decoded_data["songs"].pop(int(item_id)))
			else: decoded_data["songs"].insert(int(item_id)+1, decoded_data["songs"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			if int(item_id)==(len(decoded_data["albums"])-1): decoded_data["albums"].insert(0, decoded_data["albums"].pop(int(item_id)))
			else: decoded_data["albums"].insert(int(item_id)+1, decoded_data["albums"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			if int(item_id)==(len(decoded_data["setlists"])-1): decoded_data["setlists"].insert(0, decoded_data["setlists"].pop(int(item_id)))
			else: decoded_data["setlists"].insert(int(item_id)+1, decoded_data["setlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			if int(item_id)==(len(decoded_data["playlists"])-1): decoded_data["playlists"].insert(0, decoded_data["playlists"].pop(int(item_id)))
			else: decoded_data["playlists"].insert(int(item_id)+1, decoded_data["playlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	elif url=='delete':#delete the item
		if type=='fav_song':
			del decoded_data["songs"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			del decoded_data["albums"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			del decoded_data["setlists"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			del decoded_data["playlists"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	xbmc.executebuiltin('Container.Refresh')

###################################################################################
#SETTINGS

def Open_settings():
	xbmcaddon.Addon(addon_id).openSettings()

###################################################################################
#XBMC RANDOM FUNCTIONS: OPEN_URl; ADDLINK; ADDDIR, FANART, NOTIFICATION, ETC...

def get_artist_fanart(artist):
	if not xbmcvfs.exists(os.path.join(datapath,"artistfanart")): xbmcvfs.mkdir(os.path.join(datapath,"artistfanart"))
	artistfile = os.path.join(datapath,"artistfanart",urllib.quote(artist) + '.txt')
	if xbmcvfs.exists(artistfile):
		fanart_list = eval(readfile(artistfile))
		return str(fanart_list[randint(0,len(fanart_list))-1])
	else:
		try:
			codigo_fonte = abrir_url('http://www.theaudiodb.com/api/v1/json/1/search.php?s=' + urllib.quote(artist))
		except:
			codigo_fonte = ''
		if codigo_fonte:
			decoded_data = json.loads(codigo_fonte)
			if len(decoded_data) >= 1:
    				fanart_list = []
    				if decoded_data['artists'][0]['strArtistFanart']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart'])
    				if decoded_data['artists'][0]['strArtistFanart2']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart2'])
    				if decoded_data['artists'][0]['strArtistFanart3']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart3'])
        			if fanart_list:
        				save(artistfile,str(fanart_list))
    					return str(fanart_list[randint(0,len(fanart_list)-1)])
    				else:
    					return ''
     		else:
     			return ''

#Function to write to txt files
def save(filename,contents):
    fh = open(filename, 'w')
    fh.write(contents)
    fh.close()

#Function to read txt files
def readfile(filename):
	f = open(filename, "r")
	string = f.read()
	return string

def notification(title,message,time,iconimage):
    xbmc.executebuiltin("XBMC.notification("+title+","+message+","+time+","+iconimage+")")

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def abrir_url_custom(url,**kwargs):
	for key, value in kwargs.items(): exec('%s = %s' % (key, repr(value)))
	if 'post' in locals():
		data = urllib.urlencode(post)
		req = urllib2.Request(url,data)
	else: req = urllib2.Request(url)
	if 'user_agent' in locals(): req.add_header('User-Agent', user_agent)
	else: req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0')
	if 'referer' in locals(): req.add_header('Referer', referer)
	if 'timeout' in locals(): response = urllib2.urlopen(req, timeout=timeout)
	else: response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,mode,iconimage,**kwargs):
	extra_args = ''
	for key, value in kwargs.items():
		exec('%s = %s' % (key, repr(value)))
		extra_args = extra_args + '&' + str(key) + '=' + urllib.quote_plus(str(value))
	if selfAddon.getSetting('get_artist_fanart')=="true":
		try:
			fanart = get_artist_fanart(artist)
		except:
			fanart = ''
	else: fanart = ''
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+extra_args
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
	liz.setProperty('IsPlayable', 'true')
	liz.setProperty('fanart_image', fanart)
	cm = []
	if type and type!='mymusic':
		if 'manualsearch' in locals() and manualsearch==True or not 'manualsearch' in locals():
			cm.append((translate(30803), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=18&url=1&search_query='+urllib.quote_plus(str(artist)+' '+str(track_name))+')'))
		cm.append((translate(30804), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=26&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+')'))
		if type=='song':
			if item_id: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=33&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+'&item_id='+urllib.quote_plus(item_id)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			else: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=33&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='fav_song':
			cm.append((translate(30808), 'RunPlugin(plugin://'+addon_id+'/?mode=34&url=moveup&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30809), 'RunPlugin(plugin://'+addon_id+'/?mode=34&url=movedown&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30810), 'RunPlugin(plugin://'+addon_id+'/?mode=34&url=delete&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
		cm.append((translate(30805), 'RunPlugin(plugin://'+addon_id+'/?mode=30&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
		cm.append((translate(30806), 'RunPlugin(plugin://'+addon_id+'/?mode=27&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
	liz.addContextMenuItems(cm, replaceItems=True)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,folder=True,**kwargs):
	extra_args = ''
	for key, value in kwargs.items():
		exec('%s = %s' % (key, repr(value)))
		extra_args = extra_args + '&' + str(key) + '=' + urllib.quote_plus(str(value))
	if selfAddon.getSetting('get_artist_fanart')=="true":
		try:
			fanart = get_artist_fanart(artist)
		except:
			fanart = ''
	else: fanart = ''
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+extra_args
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	cm = []
	if type:
		if type=='album':
			if country: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=33&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&country='+urllib.quote_plus(country)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			else: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=33&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='setlist': cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=33&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus(url)+'&artist='+urllib.quote_plus(artist)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='playlist': cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=33&name='+urllib.quote_plus(name)+'&playlist_id='+urllib.quote_plus(playlist_id)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='fav_song' or type=='fav_album' or type=='fav_setlist' or type=='fav_playlist':
			cm.append((translate(30808), 'RunPlugin(plugin://'+addon_id+'/?mode=34&url=moveup&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30809), 'RunPlugin(plugin://'+addon_id+'/?mode=34&url=movedown&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30810), 'RunPlugin(plugin://'+addon_id+'/?mode=34&url=delete&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
	liz.addContextMenuItems(cm, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None
artist=None
album=None
track_name=None
type=None
search_query=None
country=None
item_id=None
playlist_id=None
fanart=None


try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: artist=urllib.unquote_plus(params["artist"])
except: pass
try: album=urllib.unquote_plus(params["album"])
except: pass
try: track_name=urllib.unquote_plus(params["track_name"])
except: pass
try: type=urllib.unquote_plus(params["type"])
except: pass
try: search_query=urllib.unquote_plus(params["search_query"])
except: pass
try: country=urllib.unquote_plus(params["country"])
except: pass
try: item_id=urllib.unquote_plus(params["item_id"])
except: pass
try: playlist_id=urllib.unquote_plus(params["playlist_id"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Fanart: "+str(fanart)
if artist: print "Artist: "+str(artist)
if album: print "Album: "+str(album)
if track_name: print "Track Name: "+str(track_name)
if type: print "Type: "+str(type)
if search_query: print "Search Query: "+str(search_query)
if country: print "Country: "+str(country)
if item_id: print "Item Id: "+str(item_id)
if playlist_id: print "Playlist Id: "+str(playlist_id)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

# Main Menu
if mode==None: Main_menu()
# Recomendations
elif mode==1: Recomendations(url)
# Digster
elif mode==2: Digster_menu()
elif mode==3: Digster_sections()
elif mode==4: Digster_categories(url)
elif mode==5: List_digster_playlists(url,search_query)
elif mode==6: List_digster_tracks(url)
# Charts
elif mode==7: Top_charts_menu()
elif mode==8 or mode==9: Itunes_countries_menu(mode)
elif mode==10: Itunes_track_charts(url,country)
elif mode==11: Itunes_album_charts(url,country)
elif mode==12: Itunes_list_album_tracks(url,album,country)
elif mode==13 or mode==14: Billboard_charts(url,mode,playlist_id)
elif mode==15 or mode==16: Officialcharts_uk(url,mode,playlist_id)
# Search and list content
elif mode==17: Search_main()
elif mode==18: Search_by_tracks(url,search_query)
elif mode==19: Search_by_albums(url,search_query)
elif mode==20: List_album_tracks(url,artist,album)
elif mode==21: Search_by_toptracks(url,search_query)
elif mode==22: Search_by_setlists(url,search_query)
elif mode==23: List_setlist_tracks(url)
elif mode==24: Search_8tracks_playlists(url,search_query)
elif mode==25: List_8tracks_tracks(url,iconimage,playlist_id)
elif mode==26: Search_by_similartracks(artist,track_name)
elif mode==27: Search_videoclip(artist,track_name)
# Downloads and Resolvers
elif mode==28: List_my_songs()
elif mode==29: Resolve_songfile(url,artist,track_name,album,iconimage)
elif mode==30: Download_songfile(name,url,artist,track_name)
# Favorites
elif mode==31: Favorites_menu()
elif mode==32: List_favorites(url)
elif mode==33: Add_to_favorites(type,artist,album,country,name,playlist_id,track_name,url,iconimage,item_id)
elif mode==34: Edit_favorites(url,type,item_id)
# Settings
elif mode==35: Open_settings()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))