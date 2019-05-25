from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import Http404
from index.models import *
import time
def songlistView(request):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
    # 取出歌单
    list_user = request.user.username
    song_info = Song.objects.filter(song_id=song_id).first()
    list_all = Songlist.objects.filter(list_user=list_user).order_by('list_id')
    song_name = song_info.song_name
    page = int(request.GET.get('page', 1))
    paginator = Paginator(list_all, 5)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'songlist.html', locals())


# 添加到歌单
def songlistaddView(request, song_id):
    if request.user.username:
        songlist = Songlist()
        songlist.list_user = request.user.username
        songlist.list_name = songlist.list_user + '的歌单'
        songlist.song_id = song_id
        songlist.save()
    return redirect('/play/%s.html' % (str(song_id)))