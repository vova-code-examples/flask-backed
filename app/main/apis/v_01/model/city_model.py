from flask_restx import Namespace, fields


class CityModel:
    namespace = Namespace('city')

    add_model = namespace.model('add_city_model', {
        'name_ua': fields.String(required=True),
        'name_en': fields.String(required=True),
    })
    update_model = namespace.model('update_city_model', {
        'id': fields.Integer(),
        'name_ua': fields.String(),
        'name_en': fields.String(),
    })
    return_model = namespace.model('return_city_model', {
        'id': fields.Integer(),
        'name_ua': fields.String(),
        'name_en': fields.String(),
    })
