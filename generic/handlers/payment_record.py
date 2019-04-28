from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm
from django.urls import re_path
from generic import models
from django.shortcuts import HttpResponse


class PaymentRecordModelForm(StartXModelForm):
    class Meta:
        model = models.PaymentRecord
        fields = ['pay_type', 'paid_fee', 'classes', 'note']


class PayMentHandler(StartXHandler):
    list_display = ['customer', get_field_display('缴费类型', 'pay_type'), 'paid_fee', 'classes', 'consultant',
                    get_field_display('状态', 'confirm_status')]
    model_form_class = PaymentRecordModelForm

    def get_list_display(self):
        """
        获取页面上应该显示的列，预留的自定义扩展，例如：以后根据用户的不同显示不同的列
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def get_model_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_consultant_id = request.session['staffinfo']['staff_id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_consultant_id)

    def save(self, request, form, is_update, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_consultant_id = request.session['staffinfo']['staff_id']

        object_exists = models.Customer.objects.filter(id=customer_id,
                                                       consultant_id=current_consultant_id).exists()
        if not object_exists:
            return HttpResponse('非法操作')

        form.instance.customer_id = customer_id
        form.instance.consultant_id = current_consultant_id

        form.save()
