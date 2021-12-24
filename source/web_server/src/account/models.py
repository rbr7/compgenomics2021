from django.db import models
import os
from uuid import uuid4

# Create your models here.

class End_user(models.Model):
	name = models.CharField(label="User name", max_length = 50)
    email_id = models.EmailField(max_length = 512)
    uid = models.UUIDField(primary_key = True, default = uuid4)
	account_date = models.DateField(auto_now_add = True , blank = False)

	def __str__(self):
        # capture info here
        val = f"The user: {self.name} has email id: {str(self.email_id) and account id: {str(self.uid)} on date: {str(self.account_date)}"
		return val