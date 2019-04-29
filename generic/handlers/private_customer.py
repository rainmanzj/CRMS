from startX.serivce.v1 import StartXHandler, get_field_display, get_m2m_display, StartXModelForm
from django.urls import reverse
from generic import models
from django.utils.safestring import mark_safe
from .base_promission import PermissionHandler


class PrivateModelForm(StartXModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant']


class PrivateCustomerHandler(PermissionHandler, StartXHandler):
    """
    私户设置
    """

    def display_record(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '跟进记录'
        record_url = reverse('startX:generic_consultrecord_list', kwargs={'customer_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">跟进记录</a>' % record_url)

    def display_pay_record(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '缴费'
        record_url = reverse('startX:generic_paymentrecord_list', kwargs={'customer_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">缴费记录</a>' % record_url)

    def get_model_queryset(self, request, *args, **kwargs):
        current_consultant_id = request.session['staffinfo']['staff_id']
        return self.model_class.objects.filter(consultant_id=current_consultant_id)

    def action_multi_remove(self, request, *args, **kwargs):
        """
        批量将私户客户拉取到公户
        :return:
        """
        pk_list = request.POST.getlist('pk')
        current_consultant_id = request.session['staffinfo']['staff_id']

        self.model_class.objects.filter(consultant_id=current_consultant_id, id__in=pk_list).update(consultant=None)

    action_multi_remove.text = "移除到公户"

    def save(self, request, form, is_update, *args, **kwargs):
        """
        添加数据时，重写save方法，直接保存到当前用户的私户里
        :param request:
        :param form:
        :param is_update:
        :param args:
        :param kwargs:
        :return:
        """
        if not is_update:
            current_consultant_id = request.session['staffinfo']['staff_id']
            form.instance.consultant_id = current_consultant_id
        form.save()

    action_list = [action_multi_remove, ]

    model_form_class = PrivateModelForm

    list_display = [StartXHandler.display_checkbox, 'name', 'qq', get_field_display('报名状态', 'status'),
                    get_m2m_display('咨询课程', 'course'), display_record, display_pay_record]
