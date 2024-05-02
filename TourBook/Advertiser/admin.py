from django.contrib import admin

from .models.advertiser import Advertiser
from .models.service import Service
from .models.advertiser import AdvertiserAttachments
from .models.offers import Offer, Offer_Attachments, OfferRequest


admin.site.register(Advertiser)
admin.site.register(Service)
admin.site.register(Offer)
admin.site.register(OfferRequest)
admin.site.register(Offer_Attachments)
admin.site.register(AdvertiserAttachments)
