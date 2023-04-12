from django.contrib import admin
from conv_dep.models import *

# Register your models here.
admin.site.register(Conv)
admin.site.register(Utterance)
admin.site.register(Word)
admin.site.register(Relation)
admin.site.register(Relationship)
