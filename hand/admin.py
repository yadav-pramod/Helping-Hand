from django.contrib import admin

from .models import hospital,delete_request,profile,feedback


admin.site.site_header = "Helping Hand administration"
admin.site.site_title = 'Helping Hand admin'

admin.site.index_template = 'admin/hand/my_custom_index.html'

# Register your models here.

admin.site.register(profile)
admin.site.register(hospital)
admin.site.register(feedback)

