from django.contrib import admin
from conv_dep.models import Conv, Utterance, Word, Relation, Relationship, Utr_Word

# Register your models here.
admin.site.register(Conv)
admin.site.register(Utterance)
admin.site.register(Utr_Word)
admin.site.register(Word)
admin.site.register(Relation)
admin.site.register(Relationship)
