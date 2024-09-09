__author__ = 'Ricardo'
__version__ = '0.1'


def insert_initial_data(apps, schema_editor):

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

    phone_type_categories = (
        'Celular',
        'Casa',
        'Oficina',
        'Otro',
    )

    channel_categories = (
        'Correo Electrónico',
        'Póster',
        'Presentación',
        'Otra Persona',
        'Internet',
        'Otro',
    )

    relation_categories = (
        'Colaborador',
        'Ex Colaborador',
        'Proveedor',
        'Cliente'
    )

    city_categories = (
        'Guadalajara',
        'Querétaro',
        'León',
        'Playa del Carmen',
        'Veracruz',
        'Otro',
    )

    classification_categories = (
        'Fuga de Información',
        'Robo de Mercancía o Activos',
        'Relación Laboral',
        'Hostigamiento o Acoso',
        'Código de ética',
        'Corrupción o Soborno',
        'Otro',
    )

    status_categories = (
        'Pendiente de Asignar',
        'Análisis',
        'Investigación',
        'Resolución',
        'Desestimados',
    )

    priority_categories = (
        'Sin asignar',
        'Alta',
        'Media',
        'Baja',
    )

    for phone_type in phone_type_categories:
        PhoneTypeCategoryModel.objects.create(phone_type=phone_type)

    for channel_category in channel_categories:
        ChannelCategoryModel.objects.create(channel=channel_category)

    for relation_category in relation_categories:
        RelationCategoryModel.objects.create(relation=relation_category)

    for city_category in city_categories:
        CityCategoryModel.objects.create(city=city_category)

    for classification_category in classification_categories:
        ClassificationCategoryModel.objects.create(
            classification=classification_category)
    
    for status_category in status_categories:
        StatusCategoryModel.objects.create(status=status_category)
    
    for priority_category in priority_categories:
        PriorityCategoryModel.objects.create(priority=priority_category)
