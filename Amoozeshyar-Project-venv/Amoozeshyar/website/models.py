from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from django_jalali.db import models as jmodels
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import os, shutil

# Create your models here.

class major(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="نام رشته")
    code = models.PositiveIntegerField(verbose_name="کد رشته", primary_key=True, blank=False, unique=True)
    capacity = models.SmallIntegerField(verbose_name="ظرفیت", blank=False)

    class Meta:
        indexes = [models.Index(
            fields=["code"]
        )]

    def __str__(self):
        return self.name
    

class university(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دانشگاه", blank=False)
    code = models.PositiveIntegerField(verbose_name="کد دانشگاه", unique=True, primary_key=True)

    class Meta:
        indexes = [models.Index(
            fields=["code"]
        )]

    def __str__(self):
        return self.name


class student(models.Model):

    def image_saving_location(instance, filename):
        return f'{instance.student_id}/{filename}'
    
    
    class gender_choices(models.TextChoices):
        MALE = "مرد", ("مرد")
        FEMALE = "زن", ("زن")


    # ? student's general information
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="student")
    first_name = models.CharField(max_length=100, blank=False, verbose_name="نام")
    last_name = models.CharField(max_length=150, blank=False, verbose_name="نام خانوادگی")
    date_of_birth = jmodels.jDateField(blank=False, verbose_name="تاریخ تولد")
    student_id = models.CharField(max_length = 10, blank=False, unique=True, verbose_name="کد ملی")
    photo = ResizedImageField(blank=False, upload_to=image_saving_location, scale=0.75, force_format="PNG", verbose_name="عکس")
    marriage = models.BooleanField(default=False, verbose_name="وضعیت تاهل")
    mobile = PhoneNumberField(blank=False, region="IR", verbose_name="موبایل")
    address = models.TextField(blank=False, verbose_name="آدرس")
    gender = models.CharField(max_length=3, blank=False, choices=gender_choices, default=gender_choices.MALE, verbose_name="جنسیت")

    # ? student's educational information
    student_number = models.CharField(max_length=12, primary_key=True, default=None, verbose_name="شماره دانشجویی")  # ? auto complete - primary key
    entrance_year = jmodels.jDateField(auto_now_add=True, verbose_name="سال ورودی")
    last_year = models.SmallIntegerField(verbose_name="آخرین سال تحصیل", null=True, blank=True)     # ? auto complete - entrance year + 5
    major = models.ForeignKey(major,on_delete=models.DO_NOTHING, related_name="major", default=None, verbose_name="رشته", blank=False)  
    # credit =  # ! auto calculate
    # average_score =   # ! auto calculate
    university = models.ForeignKey(university,on_delete=models.DO_NOTHING, related_name="unversity", default=None, verbose_name="دانشگاه", blank=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



@receiver(pre_save, sender=student)
def set_last_year(sender, instance, **kwargs):
    if not instance.last_year and hasattr(instance, 'entrance_year'):
        temp = int(str(instance.entrance_year)[:4])
        instance.last_year = temp + 5


@receiver(pre_save, sender=student)
def set_student_number(sender, instance, **kwargs):

    if hasattr(instance, 'student_number') and not instance.student_number:
        part_1 = str(instance.entrance_year)[1:4]
        part_2 = str(instance.university.code)
        part_3 = str(instance.major.code)
        part_4 = '100'
        try:
            last_user = student.objects.all().order_by("-student_number")
        except TypeError:
            pass

        if last_user:
            part_4 = str(int(last_user[0].student_number[9:12]) + 1)

        instance.student_number = part_1 + part_2 + part_3 + part_4


@receiver(pre_save, sender=student)
def set_entrance_year(sender, instance, **kwargs):
    if not instance.entrance_year and hasattr(instance, "entrance_year"):
        instance.entrance_year = jmodels.jdatetime.date.today()


@receiver(post_delete, sender=student)
def delete_image(sender, instance, **kwargs):
    if instance.photo:
        image_path = instance.photo.path
        folder_path = os.path.dirname(image_path)

        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)