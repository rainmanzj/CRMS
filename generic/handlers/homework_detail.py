from startX.serivce.v1 import StartXHandler, get_field_display, get_m2m_display, StartXModelForm
from .base_promission import PermissionHandler
from django.urls import re_path, reverse
from generic import models
from django.utils.safestring import mark_safe
from django.conf import settings
from django.shortcuts import HttpResponse


class HomeworkDetailModelForm(StartXModelForm):
    class Meta:
        model = models.HomeworkDetail
        fields = ['critic', 'status']


class HomeworkDetailHandler(PermissionHandler, StartXHandler):
    model_form_class = HomeworkDetailModelForm

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<homework_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^change/(?P<homework_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),
            re_path(r'^del/(?P<homework_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_del_name),
            re_path(r'^download/(?P<pk>\d+)/$', self.wrapper(self.download),
                    name=self.get_url_name('download')),
        ]
        patterns.extend(self.extra_url())
        return patterns

    def display_edit(self, model=None, is_header=None, *args, **kwargs):
        """

        :param model: model即数据库表对象
        :param is_header: 是否是表头字段
        :return: 显示除了表的字段verbose_name外，自添加字段
        """

        if is_header:
            return "编辑"
        homework_id = kwargs.get('homework_id')
        return mark_safe('<a href="%s">编辑</a>' % self.reverse_change_url(pk=model.pk, homework_id=homework_id))

    def display_edit_del(self, model=None, is_header=None, *args, **kwargs):

        if is_header:
            return '操作'
        homework_id = kwargs.get('homework_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_change_url(pk=model.pk, homework_id=homework_id),
            self.reverse_delete_url(pk=model.pk, homework_id=homework_id))
        return mark_safe(tpl)

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_model_queryset(self, request, *args, **kwargs):
        homework_id = kwargs.get('homework_id')
        return self.model_class.objects.filter(homework_id=homework_id)

    def action_multi_check(self, request, *args, **kwargs):
        """
        批量删除钩子，如果想要定制执行成功后的返回值，那么就为action函数设置返回值即可。
        :return:
        """

        pk_list = request.POST.getlist('pk')
        # self.model_class.objects.filter(id__id=pk_list).update(status=4)
        for pk in pk_list:
            home_detail_object = self.model_class.objects.filter(id=pk).first()
            home_detail_object.status = 4
            home_detail_object.save()

    action_multi_check.text = "批量批改"

    def display_download(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '作业文件'
        name = "%s:%s" % (self.site.namespace, self.get_url_name('download'),)
        reverse_url = reverse(name, kwargs={'pk': model.pk})
        return mark_safe('<a target="_blank" href="%s">下载作业</a>' % reverse_url)

    def download(self, request, pk, *args, **kwargs):
        """
        下载学员的作业
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        file = str(self.model_class.objects.filter(id=pk).first().file)
        file_link = settings.BASE_FILE + file
        return HttpResponse('<a href="%s" download="%s">点我下载</a>' % (file_link, file))

    action_list = [action_multi_check, ]
    list_display = [StartXHandler.display_checkbox, get_m2m_display('学生', 'student'),
                    get_field_display('作业状态', 'status'), display_download, 'critic']
