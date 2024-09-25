__author__ = 'Ricardo'
__version__ = '1.0'


def get_grouped_user_permissions(user):

    permissions = [permission.name for permission in user.groups.all()]

    return {
        'cities': [permission for permission in permissions if permission in [
            'Querétaro', 'León', 'Playa del carmen', 'Veracruz', 'Otro']],
        'priorities': [permission for permission in permissions if permission in [
            'Alta', 'Baja', 'Media']],
        'tasks': [permission for permission in permissions if permission in [
            'Usuarios', 'Comentarios']]
    }
