from django.db import models
from project.utils import send_templated_email


class Subscription(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True)
    created_ip_address = models.GenericIPAddressField(editable=False, null=True, blank=True)
    sent_emails = models.PositiveIntegerField(default=0, editable=False, help_text='Counts how many time an email is sent to this address.')

    email = models.EmailField()

    def __str__(self):
        return self.email

    def notify(self):
        """
        Send the given subscription an email with the voucher code.
        """
        send_templated_email(
            subject='Here is Your Promo Code!',
            to=self.email,
            txt_template='subscriptions/email.txt',
            html_template='subscriptions/email.html',
            context=dict(voucher=Voucher.get_code())
        )

        self.increase_sent_emails()

    def increase_sent_emails(self):
        self.sent_emails = self.sent_emails + 1
        self.save()


class Voucher(models.Model):
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.code

    @classmethod
    def get_code(cls):
        """
        Returns the voucher code
        """
        return cls.objects.first().code
