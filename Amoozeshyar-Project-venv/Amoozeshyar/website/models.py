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


class professor(models.Model):

    def image_saving_location(instance, filename):
        return f'professor/{instance.last_name}/{filename}'
    

    # ? general information
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor")
    first_name = models.CharField(max_length=70, blank=False, verbose_name="نام")
    last_name = models.CharField(max_length=100, blank=False, verbose_name="نام خانوادگی")
    date_of_birth = jmodels.jDateField(blank=False, verbose_name="تاریخ تولد")
    professor_id = models.CharField(max_length=10, blank=False, unique=True, verbose_name="کد ملی")
    photo = ResizedImageField(upload_to=image_saving_location, blank=False, scale=0.75, force_format="PNG", verbose_name="عکس")
    professor_major = models.CharField(max_length=255, blank=False, verbose_name="رشته تحصیلی")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    phone = PhoneNumberField(blank=False, region="IR", verbose_name="شماره موبایل")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    modified = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ تغییر")

    # ? university related information
    professor_code = models.CharField(max_length=10, primary_key=True, default=None, verbose_name="کد استاد")    # ? autofill - primary key
    universities = models.ManyToManyField(university, related_name="professor", blank=False, verbose_name="دانشگاه(های) مشغول به تحصیل")

    class Meta:
        indexes = [models.Index(
            fields=["professor_code"]
        )]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class student(models.Model):

    def image_saving_location(instance, filename):
        return f'student/{instance.student_id}/{filename}'
    
    
    class gender_choices(models.TextChoices):
        MALE = "مرد", ("مرد")
        FEMALE = "زن", ("زن")

    class status_choices(models.TextChoices):
        FINISHED = "فارغ", ("فارغ التحصیل")
        STUDYING = "مشغول", ("مشغول به تحصیل")
        OFF = "مرخصی", ("مرخصی")


    # ? student's general information
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="student")
    first_name = models.CharField(max_length=100, blank=False, verbose_name="نام")
    last_name = models.CharField(max_length=150, blank=False, verbose_name="نام خانوادگی")
    date_of_birth = jmodels.jDateField(blank=False, verbose_name="تاریخ تولد")
    student_id = models.CharField(max_length=10, blank=False, unique=True, verbose_name="کد ملی")
    photo = ResizedImageField(blank=False, upload_to=image_saving_location, scale=0.75, force_format="PNG", verbose_name="عکس")
    marriage = models.BooleanField(default=False, verbose_name="وضعیت تاهل")
    mobile = PhoneNumberField(blank=False, region="IR", verbose_name="موبایل")
    address = models.TextField(blank=False, verbose_name="آدرس")
    gender = models.CharField(max_length=3, blank=False, choices=gender_choices, default=gender_choices.MALE, verbose_name="جنسیت")
    modified = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ تغییر")

    # ? student's educational information
    student_number = models.CharField(max_length=12, primary_key=True, default=None, verbose_name="شماره دانشجویی")  # ? autofill - primary key
    entrance_year = jmodels.jDateField(auto_now_add=True, verbose_name="سال ورودی")
    last_year = models.SmallIntegerField(verbose_name="آخرین سال تحصیل", null=True, blank=True)     # ? autofill - entrance year + 5
    major = models.ForeignKey(major,on_delete=models.DO_NOTHING, related_name="student", default=None, verbose_name="رشته", blank=False)  
    # credit =  # ! auto calculate
    # average_score =   # ! auto calculate
    university = models.ForeignKey(university,on_delete=models.DO_NOTHING, related_name="student", default=None, verbose_name="دانشگاه", blank=False)
    status = models.CharField(max_length=5, blank=False, choices=status_choices, default=status_choices.STUDYING)


    class Meta:
        indexes = [models.Index(
            fields=["student_number"]
        )]

    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'



# todo - functions for models

@receiver(post_save, sender=student)
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



@receiver(pre_save, sender=professor)
def set_professor_code(sender, instance, **kwargs):
    if not instance.professor_code and hasattr(instance, "professor_code"):
        part_1 = str(instance.date_of_birth)[:4]
        part_2 = str(instance.created)[1:4]
        part_3 = "100"

        try:
            last_user = professor.objects.all().order_by("-professor_code")
        except TypeError:
            pass

        if last_user:
            part_3 = str(int(last_user[0].professor_code[6:]) + 1)

        instance.professor_code = part_1 + part_2 + part_3
    


@receiver(pre_save, sender=professor)
def set_created(sender, instance, **kwargs):
    if not instance.created:
        instance.created = jmodels.jdatetime.datetime.now()



def delete_image(sender, instance, **kwargs):
    if instance.photo:
        image_path = instance.photo.path
        folder_path = os.path.dirname(image_path)

        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)


def delete_user(sender, instance, **kwargs):
        if instance.user:
            username = instance.user.username
            password = instance.user.password
            user = User.objects.get(username=username, password=password)
            user.delete()


models_to_handle = [professor, student]

# ? Register the signal for each model
for model in models_to_handle:
    @receiver(post_delete, sender=model)
    def handle_post_delete(sender, instance, **kwargs):
        delete_image(sender, instance, **kwargs)

    @receiver(post_delete, sender=model)
    def handle_user_delete(sender, instance, **kwargs):
        delete_user(sender, instance, **kwargs)

