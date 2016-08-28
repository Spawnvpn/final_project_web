from django.db import models


class SearchHistory(models.Model):
    PROCESS = 0
    HAVE_RESULTS = 1
    DONE = 2

    STATE_CHOICES = (
        (PROCESS, "Process"),
        (HAVE_RESULTS, "Have results"),
        (DONE, "Done"),
    )

    search_phrase = models.CharField(max_length=255, blank=True, null=True)
    search_state = models.IntegerField(choices=STATE_CHOICES, default=PROCESS)
    image_url = models.CharField(max_length=1000, blank=True, null=True)
    engine_url = models.CharField(max_length=255, blank=True, null=True)
