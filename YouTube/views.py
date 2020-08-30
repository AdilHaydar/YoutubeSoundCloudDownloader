from django.shortcuts import render,HttpResponse,redirect,reverse,HttpResponseRedirect,Http404
from django.contrib import messages
import os
from pytube import YouTube
import shutil
from moviepy.editor import *
# Create your views here.


def index(request):

	if request.GET.get("url") and "youtube.com" in request.GET.get("url").lower():
		str_url = str(request.GET.get("url"))
		yt = YouTube(str_url)

		if request.GET.get("comboBox") == "1080p":
			q_1080p = yt.streams.filter(res="1080p",mime_type="video/mp4").first().download()
		elif request.GET.get("comboBox") == "720p":
			q_720p = yt.streams.filter(res="720p",mime_type="video/mp4").first().download()
		elif request.GET.get("comboBox") == "480p":
			q_480p = yt.streams.filter(res="480p",mime_type="video/mp4").first().download()
		elif request.GET.get("comboBox") == "audio":		
			#audio_128kbps = yt.streams.filter(abr="128kbps",mime_type="audio/mp4").first().download()
			q_720p = yt.streams.filter(res="720p",mime_type="video/mp4").first().download()
			

		###########
		"""videos = yt.streams.all()

		video = list(enumerate(videos))
		for i in video:
			print(i)

		dn_video = videos[0]
		dn_video.download()"""
		############
		
		for i in os.listdir(os.getcwd()):
			if '.mp4' in i:
				downloaded_video = i
		shutil.move(downloaded_video,os.getcwd()+'/media/')

		if request.GET.get("comboBox") == "audio":
			video = VideoFileClip(os.path.join(os.getcwd(),"media",downloaded_video))
			video.audio.write_audiofile(os.path.join(os.getcwd(),"media",yt.title+".mp3"))
			os.remove(os.path.join(os.getcwd(),"media",downloaded_video))

		data = {
			"success":"Videoyu Başarılı Bir Şekilde İndirilebilirsiniz.",
			"url":downloaded_video,
			"title":yt.title,
			"views":yt.views,
			"thumbnail":yt.thumbnail_url,
			"description":yt.description,
			"author":yt.author,
		}

		return render(request,'index.html',data)
	elif request.GET.get("url") and "soundcloud.com" in request.GET.get("url").lower():
		os.system("scdl -l "+request.GET.get("url"))
		for i in os.listdir(os.getcwd()):
			if '.mp3' in i:
				downloaded_music = i
		shutil.move(downloaded_music,os.getcwd()+'/media/')
		data = {
			"success":"Şarkıyı Başarılı Bir Şekilde İndirilebilirsiniz.",
			"url":downloaded_music,
			"title":downloaded_music[:-4],
		}
		return render(request,'index.html',data)
	return render(request,'index.html')

            #https://stackoverflow.com/questions/62098925/why-my-youtube-video-downloader-only-downloads-some-videos-and-for-other-videos
            #bu link ile signatureCipher yaptım cipher kısmını ve hata düzeldi.

            #soundcloud downlaoder https://github.com/flyingrub/scdl
            #scdl -l url ile çalışıyor terminalden