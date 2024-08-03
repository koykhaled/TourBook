from django.core import exceptions


class OfferValidationService:

    @staticmethod
    def num_of_seat_validation(advertiser, value):
        if advertiser.place_capacity < value:
            raise exceptions.ValidationError("Number of seats is exceeded")
        return value

    @staticmethod
    def service_validation(advertiser, value):
        if value not in advertiser.service.all():
            raise exceptions.ValidationError(
                "Choose one from the Advertiser Services")
        return value
