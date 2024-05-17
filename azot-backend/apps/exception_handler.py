# exception_handler.py
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    The function `custom_exception_handler` handles custom exceptions by mapping them to specific
    handlers and returning a response with the appropriate status code and message.

    :param exc: The `exc` parameter is the exception object that was raised. It contains information
    about the exception, such as its type, message, and traceback
    :param context: The `context` parameter in the `custom_exception_handler` function is a dictionary
    that contains information about the current request and view that raised the exception. It typically
    includes the following keys:
    :return: a response object.
    """
    try:
        exception_class = exc.__class__.__name__
        handlers = {
            # 'NotAuthenticated': _handler_authentication_error,
            # 'IntegrityError': _handler_integrity_error,
            # 'ValidationError': _handler_validation_error,
            # 'DoesNotExist': _handler_not_found,
            # 'PurchaseError': _handler_purchase_error,
            # Add more handlers as needed
        }
        res = exception_handler(exc, context)
        if exception_class in handlers:
            # calling hanlder based on the custom
            message, status_code = handlers[exception_class](exc, context, res)
        else:
            # if there is no hanlder is presnet
            message = str(exc)
            status_code = HTTP_500_INTERNAL_SERVER_ERROR

        return Response(data={'error': message}, status=status_code)
    except Exception as e:
        return Response(data={'error': 'Internal server error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


def _handler_validation_error(exc, context, res):
    return "Invalid data", 400


def _handler_authentication_error(exc, context, res):
    return "Password is incorrect", 400


def _handler_integrity_error(exc, context, res):
    if 'Client' in context['view'].__class__.__name__:
        return "Client already exists", 400
    elif 'Seller' in context['view'].__class__.__name__:
        return "Seller already exists", 400
    else:
        return "Integrity error", 400


def _handler_not_found(exc, context, res):
    if 'Client' in context['view'].__class__.__name__:
        return "Client not found", 400
    elif 'Seller' in context['view'].__class__.__name__:
        return "Seller not found", 400
    else:
        return "Not found", 400

def _handler_purchase_error(exc, context, res):
    return "Transaction failed.", 400