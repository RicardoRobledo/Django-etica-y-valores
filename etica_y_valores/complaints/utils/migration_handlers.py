__author__ = 'Ricardo'
__version__ = '0.1'


def insert_initial_data(apps, schema_editor):

    GroupModel = apps.get_model('auth', 'Group')
    PhoneTypeCategoryModel = apps.get_model(
        'complaints', 'PhoneTypeCategoryModel')
    ChannelCategoryModel = apps.get_model(
        'complaints', 'ChannelCategoryModel')
    RelationCategoryModel = apps.get_model(
        'complaints', 'RelationCategoryModel')
    CityCategoryModel = apps.get_model(
        'complaints', 'CityCategoryModel')
    ClassificationCategoryModel = apps.get_model(
        'complaints', 'ClassificationCategoryModel')
    StatusCategoryModel = apps.get_model(
        'complaints', 'StatusCategoryModel')
    PriorityCategoryModel = apps.get_model(
        'complaints', 'PriorityCategoryModel')

    GroupModel.objects.bulk_create([
        GroupModel(name=name) for name in (
            'Querétaro',
            'León',
            'Playa del carmen',
            'Veracruz',
            'Otro',
            'Alta',
            'Media',
            'Baja',
            'Usuarios',
            'Comentarios',
        )
    ])

    PhoneTypeCategoryModel.objects.bulk_create([
        PhoneTypeCategoryModel(phone_type=phone_type) for phone_type in (
            'Celular',
            'Casa',
            'Oficina',
            'Otro',
        )
    ])

    ChannelCategoryModel.objects.bulk_create([
        ChannelCategoryModel(channel=channel_category) for channel_category in (
            'Correo Electrónico',
            'Póster',
            'Presentación',
            'Otra Persona',
            'Internet',
            'Otro',
        )
    ])

    RelationCategoryModel.objects.bulk_create([
        RelationCategoryModel(relation=relation_category) for relation_category in (
            'Colaborador',
            'Ex Colaborador',
            'Proveedor',
            'Cliente',
        )
    ])

    CityCategoryModel.objects.bulk_create([
        CityCategoryModel(city=city_category) for city_category in (
            'Guadalajara',
            'Querétaro',
            'León',
            'Playa del Carmen',
            'Veracruz',
            'Otro',
        )
    ])

    ClassificationCategoryModel.objects.bulk_create([
        ClassificationCategoryModel(classification=classification_category) for classification_category in (
            'Fuga de Información',
            'Robo de Mercancía o Activos',
            'Relación Laboral',
            'Hostigamiento o Acoso',
            'Código de ética',
            'Corrupción o Soborno',
            'Otro',
        )
    ])

    StatusCategoryModel.objects.bulk_create([
        StatusCategoryModel(status=status_category) for status_category in (
            'Pendiente de Asignar',
            'Análisis',
            'Investigación',
            'Resolución',
            'Desestimados',
        )
    ])

    PriorityCategoryModel.objects.bulk_create([
        PriorityCategoryModel(priority=priority_category) for priority_category in (
            'Sin asignar',
            'Alta',
            'Media',
            'Baja',
        )
    ])
