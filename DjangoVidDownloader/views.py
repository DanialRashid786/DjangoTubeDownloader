from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *  
from django.utils import timezone
from datetime import date
from pytube import YouTube
from django.contrib import messages
from math import pow, floor, log
from datetime import timedelta
from requests import get

def handling_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)


# Convert from bytes
def convertsize(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(floor(log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def humanformat(number):
    if number <= 0:
        return '0.00'

    units = ['', 'K', 'M', 'B', 'T', 'Q']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

#When click search button
def download_video(request, string=""):
    global video_url
    form = DownloadForm(request.POST or None)
    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        try:
            yt_obj = YouTube(video_url)
            videos = yt_obj.streams.filter(is_dash=False).desc()
            audios = yt_obj.streams.filter(only_audio=True).order_by('abr').desc()
        except Exception as e:
            messages.error(request, e)
            return render(request, 'home.html', {'form': form})

        video_audio_streams = []
        audio_streams = []

        for s in videos:
            video_audio_streams.append({
                'resolution': s.resolution,
                'extension': s.mime_type.replace('video/', ''),
                'file_size': convertsize(s.filesize),
                'video_url': s.url, 'file_name': yt_obj.title + '.' + s.mime_type.replace('video/', '')
            })

        for s in audios:
            audio_streams.append({
                'resolution': s.abr,
                'extension': s.mime_type.replace('audio/', ''),
                'file_size': convertsize(s.filesize),
                'video_url': s.url, 'file_name': yt_obj.title + '.' + s.mime_type.replace('video/', '')
            })

        context = {
            'form': form,
            'title': yt_obj.title,
            'thumb': yt_obj.thumbnail_url,
            'author': yt_obj.author,
            'author_url': yt_obj.channel_url,
            'duration': str(timedelta(seconds=yt_obj.length)),
            'views': humanformat(yt_obj.views) if yt_obj.views >= 1000 else yt_obj.views,
            'stream_audio': audio_streams,
            'streams': video_audio_streams,
            'video_url': video_url,  # Pass the video URL to the template
        }

        return render(request, 'home.html', context)

    return render(request, 'home.html', {'form': form})
