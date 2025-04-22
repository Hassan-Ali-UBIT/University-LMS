from typing import Optional

from django.db.models import Q
from django.core.exceptions import ValidationError

from common.debug import print_parameters


def apply_filter(request, queryset, filter_lookup:dict,
                 defaults: Optional[dict] = None, 
                 required_filter: Optional[set] = None) -> tuple:

    applied_filters = []
    filter_errors = {}
    has_missing_or_incorrect_filter = False

    for param, lookup in filter_lookup.items():
        value = request.query_params.get(param)
        if value:
            try:
                if isinstance(lookup, tuple):
                    formatter = lookup[1]
                    lookup = lookup[0]
                    queryset = queryset.filter(**{lookup: formatter(value)})
                else:
                    queryset = queryset.filter(**{lookup: value})
                applied_filters.append(f"{param.replace('_', ' ').capitalize()}: {value}")
            except (ValidationError, ValueError):
                filter_errors[param] = "Incorrect Format was passed."
                has_missing_or_incorrect_filter = True

        elif defaults and param in defaults:
            try:
                cur_val = defaults[param]
                queryset = queryset.filter(**{lookup: cur_val})
                applied_filters.append(f"{param.replace('_', ' ').capitalize()}: {cur_val}")
            except (ValidationError, ValueError):
                filter_errors[param] = "Incorrect Format was passed."
                has_missing_or_incorrect_filter = True

        elif  required_filter and param in required_filter:
            filter_errors[param] = "This filter is required"
            has_missing_or_incorrect_filter = True

    if has_missing_or_incorrect_filter:
        return (False, applied_filters, filter_errors)
    
    return (queryset, applied_filters, filter_errors)

def apply_query_filter(request, queryset, lookups):

    query = request.query_params.get("q")

    fil = Q()

    for lookup in lookups:
        fil |= Q(**{lookup: query})

    try:

        if query is not None:
            queryset = queryset.filter(fil)

            queryset = queryset.distinct()


    except ValidationError:
        return False

    return queryset

def validate_required_filter_in_request(request, filters_to_check, error_messages:dict = None):

    are_all_filter_values_provided = True
    incorrect_filter_format = False
    filter_errors = {}
    filter_values = {}
    
    for filter in filters_to_check:
        required_filter = filter
        filter_formatter = None

        if isinstance(filter, tuple):
            required_filter = filter[0]
            filter_formatter = filter[1]

        filter_value = request.query_params.get(required_filter)

        if filter_value is None:
            filter_errors[required_filter] = "This filter is required"
            are_all_filter_values_provided = False
        else:
            if filter_formatter:
                try:
                    actual_filter_value = filter_formatter(filter_value)
                    filter_values[required_filter] = actual_filter_value
                except:
                    incorrect_filter_format = True
                    if error_messages and required_filter in error_messages:
                        filter_errors[required_filter] = error_messages[required_filter]
                    else:
                        filter_errors[required_filter] = "Incorrect Format was provided"
            else:            
                filter_values[required_filter] = filter_value

    
    return (filter_values, filter_errors, are_all_filter_values_provided, incorrect_filter_format)

# def required_filter(request, required_filters):

#     is_user_input_given = True
#     required_params = {}
#     user_param_value = {}
    
#     for filter in required_filters:
#         filter_value = request.query_params.get(filter)
#         if filter_value is None:
#             required_params[filter] = "This filter is required"
#             is_user_input_given = False
#         else:
#             user_param_value[filter] = filter_value
    
#     return (user_param_value, required_params, is_user_input_given)

