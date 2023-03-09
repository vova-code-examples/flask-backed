def get_field(request, field_name):
    if request and field_name in request.json:
        return request.json[field_name]
    return None
