from startX.serivce.v1 import StartXHandler


class PrivateCustomerHandler(StartXHandler):
    def get_model_queryset(self, reqeust, *args, **kwargs):
        return self.model_class.objects.filter(consultant__isnull=False)
    list_display = ['name']
