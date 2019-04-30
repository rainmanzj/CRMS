from startX.serivce.v1 import site
from generic import models
from generic.handlers.course import CourseHandler
from generic.handlers.school import SchoolHandler
from generic.handlers.staffinfo import StaffHandler
from generic.handlers.department import DepartMentHandler
from generic.handlers.classes import ClassesHandler
from generic.handlers.private_customer import PrivateCustomerHandler
from generic.handlers.public_customer import PublicCustomerHandler
from generic.handlers.consult_record import ConsultRecordHandler
from generic.handlers.payment_record import PayMentHandler
from generic.handlers.check_payment_record import CheckPayMentHandler
from generic.handlers.student import StudentHandler
from generic.handlers.score_record import ScoreRecordHandler
from generic.handlers.course_record import CourseRecordHandler
from generic.handlers.homework import HomeworkHandler
from generic.handlers.homework_detail import HomeworkDetailHandler

site.register(models.School, SchoolHandler)
site.register(models.DepartMent, DepartMentHandler)
site.register(models.Staffinfo, StaffHandler)
site.register(models.Course, CourseHandler)
site.register(models.Classes, ClassesHandler)
site.register(models.Customer, PublicCustomerHandler, prev='pub')
site.register(models.Customer, PrivateCustomerHandler, prev='pri')
site.register(models.ConsultRecord, ConsultRecordHandler)
site.register(models.PaymentRecord, PayMentHandler)
site.register(models.PaymentRecord, CheckPayMentHandler, prev='check')
site.register(models.Student, StudentHandler)
site.register(models.ScoreRecord, ScoreRecordHandler)
site.register(models.CourseRecord, CourseRecordHandler)
site.register(models.Homework, HomeworkHandler)
site.register(models.HomeworkDetail, HomeworkDetailHandler)
