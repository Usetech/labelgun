from django.http import HttpResponse
from structlog import get_logger

from calc.logs import CalcLabel

logger = get_logger()


def addition(request, *args, **kwargs):
    logger.log(**CalcLabel.RECEIVED_REQUEST_FOR_ADDITION)

    try:
        a, b = [int(request.GET.get(arg_name)) for arg_name in ('a', 'b')]
    except TypeError:
        logger.log(
            **CalcLabel.REQUEST_FOR_ADDITION_CONTAINS_NOT_VALID_ARGS,
            get_args={arg_name: request.GET.get(arg_name) for arg_name in ('a', 'b')}
        )
        return HttpResponse(CalcLabel.REQUEST_FOR_ADDITION_CONTAINS_NOT_VALID_ARGS.description)

    result = a + b

    return HttpResponse(f'{a} + {b} = {result}')
