from rest_framework.exceptions import APIException


class PurchaseError(APIException):
    status_code = 400
    default_detail = 'Transaction failed. Please try again.'
    default_code = 'purchase_error'

class PermissionDenied(APIException):
    status_code = 400
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'permission_denied'

class WrongPasswordError(APIException):
    status_code = 400
    default_detail = 'Password is incorrect.'
    default_code = 'wrong_password'