from rest_framework.exceptions import APIException


class PurchaseError(APIException):
    status_code = 400
    default_detail = 'Transaction failed. Please try again.'
    default_code = 'purchase_error'

class PermissionDenied(APIException):
    status_code = 403
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'permission_denied'

class NotActivated(APIException):
    status_code = 400
    default_detail = 'Your account is not activated yet. Please check your email.'
    default_code = 'not_activated'