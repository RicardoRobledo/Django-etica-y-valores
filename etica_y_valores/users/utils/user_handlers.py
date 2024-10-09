__author__ = 'Ricardo'
__version__ = '1.0'


def get_grouped_user_permissions(user, user_level):

    permissions = [permission.name for permission in user.groups.all()]

    permissions_gotten = {
        'cities': [permission for permission in permissions if permission in [
            'Querétaro', 'León', 'Playa del Carmen', 'Guadalajara', 'Veracruz', 'Otro']],
        'priorities': [permission for permission in permissions if permission in [
            'Alta', 'Baja', 'Media']],
        'tasks': [permission for permission in permissions if permission in [
            'Usuarios', 'Comentarios']]
    }

    if user_level == 'Operador':
        permissions_gotten['statuses'] = [
            'Pendiente de Asignar', 'Análisis', 'Investigación']

    return permissions_gotten
