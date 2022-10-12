import enum


class ChekFieldModel(enum.Enum):
    AutoField = 'int'
    ForeignKey = 'select_related'
    ManyToManyField = 'int'
    IntegerField = 'int'
    DateTimeField = 'datetime'
    TextField = 'str'
    CharField = 'str'
    SlugField = 'str'
