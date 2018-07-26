from local_land_charges_api_stub.constants.constants import AddChargeConstants
from local_land_charges_api_stub.validation import validation


def add_vary_validate(payload):
    errors = []
    if 'item' not in payload:
        errors.append({"location": "$.", "error_message": "'item' is a required property"})
    else:
        charge_data = payload['item']
        if 'local-land-charge' in charge_data:
            errors.append({"location": "$.item", "error_message":
                           "Additional properties are not allowed ('local-land-charge' was unexpected)"})

        if 'start-date' in charge_data:
            errors.append({"location": "$.item", "error_message":
                           "Additional properties are not allowed ('start-date' was unexpected)"})

        # Prevent Author being set as we set this before submission
        if 'author' in charge_data:
            errors.append({"location": "$.item",
                           "error_message": "Additional properties are not allowed ('author' was unexpected)"})

        if 'statutory-provision' in charge_data:
            stat_prov_list = AddChargeConstants.STATUTORY_PROVISION
            if charge_data['statutory-provision'] not in stat_prov_list:
                errors.append({"location": "$.item.statutory-provision",
                               "error_message": "'{}' is not valid".format(charge_data['statutory-provision'])})

        # For an add, need to simulate system setting these values
        charge_data['local-land-charge'] = 0
        charge_data['start-date'] = "2000-01-01"
        charge_data['registration-date'] = "2000-01-01"

        schema_errors = validation.get_item_errors(charge_data)
        if schema_errors:
            errors.extend(schema_errors)

    return errors
