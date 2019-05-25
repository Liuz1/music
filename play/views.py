from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse
from index.models import *
from django.utils.encoding import escape_uri_path
from user.models import MyUser
# 歌曲播放页面

def playView(request, song_id):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
    # 歌曲信息
    # if request.method == 'POST':
    #     if request.user.username:
    #         list_user = request.user.username
    #         songlist = Songlist()
    #         songlist.list_user = list_user
    #         songlist.list_name = songlist.list_user + '的歌单'
    #         songlist.song_id = song_id
    #         songlist.save()
    #     return redirect('/play/%s.html' % (str(song_id)))
    song_info = Song.objects.get(song_id=int(song_id))
    # print(song_info.song_vip)
    if request.user.username:
        uservip = request.user.vip
        print(uservip)
        if (song_info.song_vip != '0') & (uservip != '1'):
            # if song_info.song_vip == 1:
            print('render')
            vip = 1
            print(vip)
            print(request.user.username)
            doing = MyUser.objects.filter(username=request.user.username).update(vip=vip)
            return render(request, 'buyying.html')

    # 播放列表
    play_list = request.session.get('play_list', [])
    song_exist = False
    if play_list:
        for i in play_list:
            if int(song_id) == i['song_id']:
                song_exist = True
    if song_exist == False:
        play_list.append({'song_id': int(song_id), 'song_singer': song_info.song_singer, 'song_name': song_info.song_name, 'song_time': song_info.song_time})
    request.session['play_list'] = play_list
    # 歌词
    if song_info.song_lyc != '暂无歌词':
        f = open('static/songLyric/' +song_info.song_lyc, 'r', encoding='utf-8')
        song_lyc = f.read()
        f.close()
    # 相关歌曲
    song_type = Song.objects.values('song_type').get(song_id=song_id)['song_type']
    song_relevant = Dynamic.objects.select_related('song').filter(song__song_type=song_type).order_by('-dynamic_plays').all()[:6]
    # 添加播放次数
    # 扩展功能：可使用session实现每天只添加一次播放次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_plays += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=1, dynamic_search=0, dynamic_download=0, song_id=song_id)
        dynamic_info.save()
    return render(request, 'play.html', locals())

# 歌曲下载
def downloadView(request, song_id):
    # 根据song_id查找歌曲信息
    song_info = Song.objects.get(song_id=int(song_id))
    # 添加下载次数
    dynamic_info = Dynamic.objects.filter(song_id=int(song_id)).first()
    # 判断歌曲动态信息是否存在，存在就在原来基础上加1
    if dynamic_info:
        dynamic_info.dynamic_download += 1
        dynamic_info.save()
    # 动态信息不存在则创建新的动态信息
    else:
        dynamic_info = Dynamic(dynamic_plays=0,dynamic_search=0,dynamic_download=1,song_id=song_id)
        dynamic_info.save()
    # 读取文件内容
    file = 'static/songFile/' + song_info.song_file
    print(file)
    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    # 将文件内容写入StreamingHttpResponse对象，并以字节流方式返回给用户，实现文件下载
    filename = str(song_info.song_name) + '.mp3'
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename={}'.format(escape_uri_path(filename))
    return response