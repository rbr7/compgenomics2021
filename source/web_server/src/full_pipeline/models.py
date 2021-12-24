from django.db import models

# Create your models here.
from account.models import End-user

# Create your models here.

class FullPipeline(models.Model):
    #
    input_folder = models.CharField(max_length=512)
    output_folder = models.CharField(max_length=512)
    charts_folder = models.CharField(max_length=512)
    run_flag = models.BooleanField(default = False)
    person = models.ForeignKey(End-user, related_name = "fa", blank = True, on_delete=models.CASCADE)

	def __str__(self):
        #
        # capture logs here
        print(self.person.email_id)
        #
		return ("End-user " + str(self.person.email_id) + " with specific folder = " + str(self.input_folder))
