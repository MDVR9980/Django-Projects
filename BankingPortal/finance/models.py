import json
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from finance.utils.zarinpal import zpal_request_handler, zpal_payment_checker


class Gateway(models.Model):
    """
    Save Gateways name and credentials to the db and use them to handle payments
    """

    # CAUTION: do not change bellow function name
    FUNCTIONS_SAMAN = 'saman'
    FUNCTIONS_SHAPARAK = 'shaparak'
    FUNCTIONS_FINOTECH = 'finotech'
    FUNCTIONS_ZARINPAL = 'zarinpal'
    FUNCTIONS_PARSIAN = 'parsian'
    GATEWAY_FUNCTIONS = (
        (FUNCTIONS_SAMAN, _('saman')),
        (FUNCTIONS_SHAPARAK, _('shaparak')),
        (FUNCTIONS_FINOTECH, _('finotech')),
        (FUNCTIONS_ZARINPAL, _('zarinpal')),
        (FUNCTIONS_PARSIAN, _('parsian')),
    )

    title = models.CharField(max_length=100, verbose_name=_("gateway_title"))
    gateway_request_url = models.CharField(max_length=150, verbose_name=_('request url'), null=True, blank=True)
    gateway_verify_url = models.CharField(max_length=150, verbose_name=_('verify url'), null=True, blank=True)
    gateway_code = models.CharField(max_length=12, verbose_name=_('gateway code'), choices=GATEWAY_FUNCTIONS)
    is_enable = models.BooleanField(_('is enable'), default=True)
    auth_data = models.TextField(verbose_name=_('auth_data'), null=True, blank=True)

    class Meta:
        verbose_name = _('Gateway')
        verbose_name_plural = _('Gateways')

    def __str__(self):
        return self.title

    def get_request_handler(self):
        handlers = {
            self.FUNCTIONS_SAMAN: None,
            self.FUNCTIONS_SHAPARAK: None,
            self.FUNCTIONS_FINOTECH: None,
            self.FUNCTIONS_ZARINPAL: zpal_request_handler,
            self.FUNCTIONS_PARSIAN: None
        }
        return handlers[self.gateway_code]

    def get_verify_handler(self):
        handlers = {
            self.FUNCTIONS_SAMAN: None,
            self.FUNCTIONS_SHAPARAK: None,
            self.FUNCTIONS_FINOTECH: None,
            self.FUNCTIONS_ZARINPAL: zpal_payment_checker,
            self.FUNCTIONS_PARSIAN: None
        }
        return handlers[self.gateway_code]

    @property
    def credentials(self):
        return json.loads(self.auth_data)


class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name=_('invoice number'), unique=True, default=uuid.uuid4)
    amount = models.PositiveIntegerField(verbose_name=_('payment amount'), editable=True)
    # آخر خط ۷۴ ناقص موندش درستش میکنم.
    gateway = models.ForeignKey(Gateway, related_name='payments', null=True, blank=True, verbose_name=_('gateway'), on_delete=models.CASCADE)
    is_paid = models.BooleanField(verbose_name=_('is paid status'), default=False)
    payment_log = models.TextField(verbose_name=_('logs'), blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), null=True, on_delete=models.SET_NULL)
    authority = models.CharField(max_length=64, verbose_name=_('authority'), blank=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return self.invoice_number.hex

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_paid = self.is_paid

    @property
    def title(self):
        return _('Instant payment')

    def status_changed(self):
        return self.is_paid != self._b_is_paid

    def verify(self, data):
        handler = self.gateway.get_verify_handler()
        if not self.is_paid and handler is not None:
            handler(self, data)
        return self.is_paid

    def get_gateway(self):
        gateway = Gateway.objects.filter(is_enable=True).first()
        return gateway.gateway_code

    def save_log(self, data, scope='Request handler', save=True):
        generated_log = "[{}][{}]{}\n".format(timezone.now(), scope, data)
        if self.generated_log != '':
            self.generated_log += generated_log
        else:
            self.payment_log = generated_log
        if save:
            self.save()
