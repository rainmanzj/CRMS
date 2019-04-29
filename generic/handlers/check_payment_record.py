from startX.serivce.v1 import StartXHandler, get_datetime_format, get_field_display
from django.urls import re_path
from .base_promission import PermissionHandler


class CheckPayMentHandler(PermissionHandler, StartXHandler):
    order_by = ['-id', 'confirm_status']
    list_display = [StartXHandler.display_checkbox, 'customer', get_field_display('费用类型', 'pay_type'), 'paid_fee',
                    'classes', get_datetime_format('支付日期', 'apply_date'),
                    get_field_display('确认状态', 'confirm_status'), 'consultant']

    def get_urls(self):
        """只有查看和审批功能"""

        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist), name=self.get_list_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def get_list_display(self, request, *args, **kwargs):
        """
        取消默认的编辑和删除
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    def get_add_btn(self, request, *args, **kwargs):
        """没有添加的功能"""
        return None

    def action_multi_check(self, request, *args, **kwargs):
        """
        批量审批确认
        :return:
        """
        pk_list = request.POST.getlist('pk')

        for pk in pk_list:
            payment_object = self.model_class.objects.filter(id=pk, confirm_status=1).first()
            if not payment_object:
                continue
            # 缴费记录
            payment_object.confirm_status = 2
            payment_object.save()

            # 客户表
            payment_object.customer.status = 1
            payment_object.customer.save()

            # 学生表
            payment_object.customer.student.student_status = 2
            payment_object.customer.student.save()

    action_multi_check.text = "批量确认"

    def action_multi_cancel(self, request, *args, **kwargs):
        """
        批量审批驳回
        :return:
        """
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list, confirm_status=1).update(confirm_status=3)

    action_multi_cancel.text = "批量驳回"

    def action_multi_drop_out(self, request, *args, **kwargs):
        """
        批量审批退学
        :return:
        """
        pk_list = request.POST.getlist('pk')
        for pk in pk_list:
            payment_object = self.model_class.objects.filter(id=pk, confirm_status=2).first()
            if not payment_object:
                continue
            # 客户表
            payment_object.pay_type = 3
            payment_object.save()

            # 学生表
            payment_object.customer.student.student_status = 4
            payment_object.customer.student.save()

    action_multi_drop_out.text = "批量退学"

    action_list = [action_multi_check, action_multi_cancel, action_multi_drop_out]
