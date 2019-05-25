from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import *
from user.models import MyUser

def indexView(request):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:8]
    # 音乐分类
    label_list = Label.objects.all()
    # 热门歌曲
    play_hot_song = Dynamic.objects.select_related('song').order_by('-dynamic_plays').all()[:10]
    # 新歌推荐
    daily_recommendation = Song.objects.order_by('-song_release').all()[:3]
    # 热门搜索、热门下载
    search_ranking = search_song[:6]
    down_ranking = Dynamic.objects.select_related('song').order_by('-dynamic_download').all()[:6]
    all_ranking = [search_ranking, down_ranking]
    return render(request, 'index.html',locals())

def indexView1(request):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:8]
    # 音乐分类
    vip = 1
    print(vip)
    print(request.user.username)
    doing = MyUser.objects.filter(username=request.user.username).update(vip=vip)
    label_list = Label.objects.all()
    # 热门歌曲
    play_hot_song = Dynamic.objects.select_related('song').order_by('-dynamic_plays').all()[:10]
    # 新歌推荐
    daily_recommendation = Song.objects.order_by('-song_release').all()[:3]
    # 热门搜索、热门下载
    search_ranking = search_song[:6]
    down_ranking = Dynamic.objects.select_related('song').order_by('-dynamic_download').all()[:6]
    all_ranking = [search_ranking, down_ranking]
    return render(request, 'index.html',locals())


# 自定义404和500的错误页面
# def page_not_found(request):
#     return render_to_response('error404.html')