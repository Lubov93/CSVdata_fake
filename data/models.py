from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class DataStatusChoises:
    READY = "Ready"
    PROCESSING = "Process"
    FAILED = "Failed"

    CHOICES = (
        (READY, "Ready to download"),
        (PROCESSING, "In progress"),
        (FAILED, "Error"),
    )


class ColumnChoicesType:
    INT = "integer"
    DATE = "date"
    EMAIL = "email"
    PHONE = "phone"
    JOB = "job"
    NAME = "name"

    CHOICES = (
        (NAME, "Full name"),
        (INT, "Number range"),
        (DATE, "Date time"),
        (EMAIL, "E-mail"),
        (PHONE, "Phone number"),
        (JOB, "Job"),
    )


class Data(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    separator = models.CharField(max_length=1,
                                 default=',',
                                 verbose_name='Separator')
    status = models.CharField(choices=DataStatusChoises.CHOICES,
                              max_length=255,
                              verbose_name='Status')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             verbose_name='User')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'The data {} created at {}'.format(self.name, self.created_at)


class DataFile(models.Model):
    file = models.FileField(blank=True, null=True,
                            verbose_name="Files with data")
    schema = models.ForeignKey(Data, on_delete=models.CASCADE,
                               related_name='schema_files')
    status = models.CharField(choices=DataStatusChoises.CHOICES,
                              max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-created_at',)


class DataColumn(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    column_type = models.CharField(choices=ColumnChoicesType.CHOICES,
                                   max_length=30)
    integer_range_from = models.PositiveSmallIntegerField(null=True,
                                                          blank=True,
                                                          verbose_name='From')
    integer_range_to = models.PositiveSmallIntegerField(null=True,
                                                        blank=True,
                                                        verbose_name='To')
    order = models.PositiveSmallIntegerField(default=1,
                                             validators=[MinValueValidator(1)],
                                             verbose_name='Column order')
    data = models.ForeignKey(Data, on_delete=models.CASCADE, null=True,
                             blank=True, verbose_name='Data',
                             related_name='column_in_data')

    class Meta:
        verbose_name = "Column in data"
        verbose_name_plural = "Columns in data"

    def __str__(self):
        return "Column {} in data".format(self.name)

