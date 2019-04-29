from startX.serivce.v1 import StartXHandler, get_datetime_format, StartXModelForm
from django.urls import re_path, reverse
from generic import models
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render
from django.forms.models import modelformset_factory
from .base_promission import PermissionHandler


class CourseRecordModelForm(StartXModelForm):
    class Meta:
        model = models.CourseRecord
        fields = ['day_num', 'teacher']


class StudyRecordModelForm(StartXModelForm):
    class Meta:
        model = models.StudyRecord
        fields = ['record', ]


class CourseRecordHandler(PermissionHandler, StartXHandler):
    model_form_class = CourseRecordModelForm

    def display_attendance(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '考勤'
        name = "%s:%s" % (self.site.namespace, self.get_url_name('attendance'),)
        attendance_url = reverse(name, kwargs={'course_record_id': model.pk})
        tpl = '<a target="_blank" href="%s">考勤</a>' % attendance_url
        return mark_safe(tpl)

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<class_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/(?P<class_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_name),
            re_path(r'^change/(?P<class_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),
            re_path(r'^del/(?P<class_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_del_name),
            re_path(r'^attendance/(?P<course_record_id>\d+)/$', self.wrapper(self.attendance_view),
                    name=self.get_url_name('attendance')),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def display_edit_del(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        class_id = kwargs.get('class_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_change_url(pk=model.pk, class_id=class_id),
            self.reverse_delete_url(pk=model.pk, class_id=class_id))
        return mark_safe(tpl)

    def get_model_queryset(self, request, *args, **kwargs):
        class_id = kwargs.get('class_id')
        return self.model_class.objects.filter(class_object_id=class_id)

    def save(self, request, form, is_update, *args, **kwargs):
        class_id = kwargs.get('class_id')

        if not is_update:
            form.instance.class_object_id = class_id
        form.save()

    def action_multi_init(self, request, *args, **kwargs):
        """
        批量初始化考勤记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        course_record_id_list = request.POST.getlist('pk')
        class_id = kwargs.get('class_id')
        class_object = models.Classes.objects.filter(id=class_id).first()
        if not class_object:
            return HttpResponse('班级不存在')
        student_object_list = class_object.student_set.all()
        for course_record_id in course_record_id_list:
            # 判断选择的上课记录是否合法
            course_record_object = models.CourseRecord.objects.filter(id=course_record_id,
                                                                      class_object_id=class_id).first()
            if not course_record_object:
                continue

            # 判断此上课记录对应的考勤记录是否已经存在
            study_record_exists = models.StudyRecord.objects.filter(course_record=course_record_object).exists()
            if study_record_exists:
                continue

            # 为每个学生在该天创建考勤记录
            study_record_object_list = [models.StudyRecord(student_id=stu.id, course_record_id=course_record_id) for stu
                                        in student_object_list]

            models.StudyRecord.objects.bulk_create(study_record_object_list, batch_size=50)

    action_multi_init.text = '批量初始化考勤'
    action_list = [action_multi_init, ]

    def attendance_view(self, request, course_record_id, *args, **kwargs):
        """
        考勤的批量设置
        :param request:
        :param course_record_id:
        :param args:
        :param kwargs:
        :return:
        """
        study_record_object_list = models.StudyRecord.objects.filter(course_record_id=course_record_id)
        study_model_formset = modelformset_factory(models.StudyRecord, form=StudyRecordModelForm, extra=0)

        if request.method == 'POST':
            formset = study_model_formset(queryset=study_record_object_list, data=request.POST)
            if formset.is_valid():
                formset.save()
            return render(request, 'attendance.html', {'formset': formset})

        formset = study_model_formset(queryset=study_record_object_list)
        return render(request, 'attendance.html', {'formset': formset})

    list_display = [StartXHandler.display_checkbox, 'class_object', 'day_num', 'teacher',
                    get_datetime_format('日期', 'date'), display_attendance]
