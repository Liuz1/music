from django.db import models

# Create your models here.

# 歌曲分类
class Label(models.Model):
    label_id =models.AutoField('序号', primary_key=True)
    label_name =models.CharField('标签', max_length=10)

    def __str__(self):
        return self.label_name


    class Meta:
        verbose_name = '歌曲分类'
        verbose_name_plural = verbose_name


# 歌曲
class Song(models.Model):
    song_id = models.AutoField('序号', primary_key=True)
    song_name = models.CharField('歌名', max_length=50)
    song_singer = models.CharField('歌手', max_length=50)
    song_time = models.CharField('时长', max_length=10)
    song_album = models.CharField('专辑', max_length=50)
    song_language = models.CharField('语种', max_length=20)
    song_type = models.CharField('歌曲类型', max_length=20)
    song_release = models.CharField('发行时间', max_length=20)
    song_img = models.CharField('图片', max_length=20)
    song_lyc = models.CharField('歌词', max_length=50, default='暂无歌词')
    song_file = models.CharField('文件', max_length=50)
    song_vip = models.CharField('会员', max_length=5)
    label =models.ForeignKey(Label, on_delete=models.CASCADE, verbose_name='分类')

    def __str__(self):
        return self.song_name


    class Meta:
        verbose_name = '歌曲信息'
        verbose_name_plural = verbose_name


# 动态信息表
class Dynamic(models.Model):
    dynamic_id = models.AutoField('序号', primary_key=True)
    dynamic_plays = models.IntegerField('播放次数')
    dynamic_search = models.IntegerField('搜索次数')
    dynamic_download = models.IntegerField('下载次数')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name='歌曲')


    class Meta:
        verbose_name = '动态信息'
        verbose_name_plural = verbose_name


# 评论
class Comment(models.Model):
    comment_id = models.AutoField('序号', primary_key=True)
    comment_text = models.CharField('内容', max_length=500)
    comment_user = models.CharField('用户', max_length=20)
    comment_date = models.CharField('日期', max_length=50)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name='歌曲')


    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

# 歌单
class Songlist(models.Model):
    list_id = models.AutoField('序号', primary_key=True)
    list_name = models.CharField('歌单名', max_length=20)
    list_user = models.CharField('用户', max_length=20)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name='歌曲')

    class Meta:
        verbose_name = '歌单'
        verbose_name_plural = verbose_name

