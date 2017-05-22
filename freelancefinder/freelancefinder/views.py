"""Simple views for no specific app."""
import logging
from datetime import datetime

import stripe

from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.base import TemplateView, View

logger = logging.getLogger(__name__)


class IndexPageView(TemplateView):
    """A simple homepage template view."""

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """Add the stripe key."""
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class AcceptPaymentView(View):
    """A view to process a payment."""

    def post(self, request, *args, **kwargs):
        """Process POST info."""

        token = request.POST.get('token')
        subscription_type = request.POST.get('subscription')

        description = 'Monthly ($50 billed monthly)'
        if subscription_type == 'yearly':
            description = 'Yearly ($480 billed annually)'

        stripe.api_key = settings.STRIPE_SECRET_KEY

        # TODO(Paul): Probably do the most:
        # https://stripe.com/docs/api?lang=python#error_handling
        try:
            # TODO(Paul): If we already have a customer id, probably the source
            # should be updated, but I guess we can re-use the old one?
            customer = stripe.Customer.create(
                email=request.user.email,
                source=token,
                metadata={
                    'username': request.user.username,
                }
            )

            # charge = stripe.Charge.create(
            #    customer=customer.id,
            #    amount=amount,
            #    currency='usd',
            #    description=description,
            # )

            subscription = stripe.Subscription.create(
                customer=customer.id,
                # source=token,
                plan=subscription_type,
            )
            created = datetime.utcfromtimestamp(subscription.created)

            request.user.account.subscription = subscription_type
            request.user.account.stripe_customer_id = customer.id
            request.user.account.stripe_subscription_id = subscription.id
            request.user.account.stripe_subscription_created = created
            request.user.account.save()
        except stripe.error.CardError as carde:
            logger.exception("Stripe Card Error: %s", carde)
            raise Exception("Charge Card Error: %s" % carde)
        except Exception as chargee:
            logger.exception("Stripe Other Error: %s", chargee)
            raise Exception("Charge Exception: %s" % chargee)

        logger.info("Post info: %s", request.POST)
        messages.success(request, "Payment received for {}.".format(description))
        return HttpResponseRedirect(reverse('index'))
