from startX.serivce.v1 import StartXHandler, get_field_display, get_m2m_display
from startX.serivce.v1 import StartXModelForm
from generic import models
from django.utils.safestring import mark_safe
from django.urls import re_path
from django.shortcuts import HttpResponse, render
from django.db import transaction


class PublicModelForm(StartXModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant']


class PublicCustomerHandler(StartXHandler):
    """公户设置"""

    def get_model_queryset(self, reqeust, *args, **kwargs):
        return self.model_class.objects.filter(consultant__isnull=True)

    def display_record(self, model=None, is_header=None):
        if is_header:
            return '跟进记录'
        record_url = self.reverse_commons_url(self.get_url_name('record'), pk=model.pk)
        return mark_safe('<a href="%s">查看跟进记录</a>' % record_url)

    def record_view(self, request, pk):
        records = self.model_class.objects.filter(id=pk).first().consultrecord_set.all()

        return render(request, 'record.html', {'records': records})

    def extra_url(self):
        patterns = [
            re_path(r'^record/(?P<pk>\d+)/$', self.wrapper(self.record_view),
                    name=self.get_url_name('record'))
        ]
        return patterns

    def action_multi_pull(self, request, *args, **kwargs):
        """
        批量将公户客户申请拉取到私户
        :return:
        """
        pk_list = request.POST.getlist('pk')
        current_consultant_id = request.session['staffinfo']['staff_id']

        # 做验证
        current_consultant_customers = models.Customer.objects.filter(consultant_id=current_consultant_id,
                                                                      status=2).count()
        if len(pk_list) + current_consultant_customers > 150:
            return HttpResponse(
                '超出最大值，您已有 %s 个客户，最多还能添加 %s 个客户' % (current_consultant_customers, 150 - current_consultant_customers))

        # 数据库中加锁
        flag = False
        with transaction.atomic():  # 事务
            queryset = models.Customer.objects.filter(id__in=pk_list, status=2, consultant__isnull=True)
            origin_queryset = queryset.select_for_update()  # 加数据库锁
            if len(origin_queryset) == len(pk_list):
                queryset.update(consultant_id=current_consultant_id)
                flag = True

        if not flag:
            return HttpResponse('手速太慢了，选中的客户已被其他人申请，请重新选择')

    action_multi_pull.text = "加入我的私户"

    action_list = [action_multi_pull, ]

    list_display = [StartXHandler.display_checkbox, 'name', 'qq', get_field_display('报名状态', 'status'),
                    get_m2m_display('咨询课程', 'course'),
                    display_record]
    model_form_class = PublicModelForm
