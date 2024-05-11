from rest_framework.exceptions import APIException


class PurchaseError(APIException):
    status_code = 400
    default_detail = 'Transaction failed. Please try again.'
    default_code = 'purchase_error'