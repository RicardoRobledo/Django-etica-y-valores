__author__ = 'Ricardo'
__version__ = '0.1'


def insert_initial_data(apps, schema_editor):

    UserLevelCategoryModel = apps.get_model('users', 'UserLevelCategory')

    UserLevelCategoryModel.objects.bulk_create([
        UserLevelCategoryModel(user_level=user_level) for user_level in (
            'Superusuario',
            'Supervisor',
            'Operador',
        )
    ])
