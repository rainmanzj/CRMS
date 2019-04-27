from startX.serivce.v1 import site
from generic import models
from generic.handlers.course import CourseHandler
from generic.handlers.school import SchoolHandler
from generic.handlers.staffinfo import StaffHandler
from generic.handlers.department import DepartMentHandler
from generic.handlers.classes import ClassesHandler
from generic.handlers.private_customer import PrivateCustomerHandler
from generic.handlers.public_customer import PublicCustomerHandler

site.register(models.School, SchoolHandler)
site.register(models.DepartMent, DepartMentHandler)
site.register(models.Staffinfo, StaffHandler)
site.register(models.Course, CourseHandler)
site.register(models.Classes, ClassesHandler)
site.register(models.Customer, PublicCustomerHandler, prev='pub')
site.register(models.Customer, PrivateCustomerHandler, prev='pri')
