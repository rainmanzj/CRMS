from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm, get_m2m_display
from .base_promission import PermissionHandler
from generic import models
from django.urls import re_path, reverse
from django.shortcuts import HttpResponse, render
from django.utils.safestring import mark_safe
from django.http import FileResponse
from django.db.models import Q


class HomeworkAddModelForm(StartXModelForm):
    class Meta:
        model = models.Homework
        fields = ['classes', 'courses', 'teacher', 'content']


"""glyphicon glyphicon-upload
    glyphicon glyphicon-download-alt
"""


class HomeworkHandler(PermissionHandler, StartXHandler):
    model_form_class = HomeworkAddModelForm

    def display_upload(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '提交作业'
        name = "%s:%s" % (self.site.namespace, self.get_url_name('upload'),)
        reverse_url = reverse(name, kwargs={'pk': model.pk})
        return mark_safe('<a target="_blank" href="%s">提交作业</a>' % reverse_url)

    def display_detail(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '学员作业情况'
        detail_url = reverse('startX:generic_homeworkdetail_list', kwargs={'homework_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">学员作业情况</a>' % detail_url)

    list_display = ['classes', 'courses', 'teacher',
                    display_detail, display_upload]
    #
    # def get_model_queryset(self, request, *args, **kwargs):
    #     teacher_id = request.session['staffinfo']['staff_id']
    #     return self.model_class.objects.filter(Q(teacher_id=teacher_id) | Q(classes__))

    def save(self, request, form, is_update, *args, **kwargs):
        teacher_id = request.session['staffinfo']['staff_id']
        if not is_update:
            form.instance.teacher_id = teacher_id
        form.save()

    def upload(self, request, pk, *args, **kwargs):
        """
        学生查看作业，提交作业
        :param request:
        :param homework_id:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = request.session['staffinfo']['staff_id']
        homework = models.Homework.objects.filter(id=pk).first()
        student = models.Student.objects.filter(users_id=user_id).first()
        if request.method == 'GET':
            return render(request, 'homework.html', {'work': homework.content})

        if not homework:
            return HttpResponse('请勿XSS攻击，我们已经记录了您的行为')
        file = request.FILES.get('file')
        file.name = '%s-%s-' % (pk, user_id) + file.name

        # 这里可以做筛选，学生已经上传过，是否支持更新
        hoemworkdetail = models.HomeworkDetail.objects.filter(homework_id=pk, student=student.id).exists()
        if hoemworkdetail:
            return HttpResponse('您已经上传过啦')

        # 学生提交一次作业就往作业详情表里添加一条数据
        users_homework = models.HomeworkDetail.objects.create(homework_id=pk, file=file, status=3)
        users_homework.student.add(student.id)
        return render(request, 'homework.html', {'work': homework.content, 'msg': '提交成功'})

    def extra_url(self):
        patterns = [
            re_path(r'^upload/(?P<pk>\d+)$', self.wrapper(self.upload), name=self.get_url_name('upload'))
        ]
        return patterns
