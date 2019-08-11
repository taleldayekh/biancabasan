from django.db import models


class Work(models.Model):
    YEARS = [year for year in range(1990, 2090)]
    YEAR_CHOICES = tuple((year, year) for year in YEARS)

    title = models.CharField(verbose_name="Title", max_length=80)
    year_from = models.IntegerField(
        verbose_name="Year (from)", choices=YEAR_CHOICES, blank=True, null=True
    )
    year_to = models.IntegerField(
        verbose_name="Year (to)", choices=YEAR_CHOICES
    )
    technique = models.CharField(verbose_name="Technique", max_length=255)
    height = models.FloatField(verbose_name="Height", blank=True, null=True)
    width = models.FloatField(verbose_name="Width", blank=True, null=True)
    depth = models.FloatField(verbose_name="Depth", blank=True, null=True)
    description = models.TextField(verbose_name="Description")
    date_added = models.DateTimeField(
        verbose_name="Date Added", auto_now_add=True
    )

    class Meta:
        verbose_name = "Work"
        verbose_name_plural = "Works"

    def __str__(self) -> str:
        return self.title
