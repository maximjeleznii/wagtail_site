from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import ContactInfo
from import_export import resources
from wagtail_exportcsv.admin import ExportModelAdminMixin

class ContactInfoResource(resources.ModelResource):

    class Meta:
        model = ContactInfo
        fields = ('first_name', 'last_name', 'email', 'message')


class ContactInfoAdmin(ExportModelAdminMixin, ModelAdmin):
    model = ContactInfo
    resource_class = ContactInfoResource
    menu_icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('first_name', 'last_name', 'email', 'message')
    list_filter = ('email',)
    search_fields = ('email',)

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(ContactInfoAdmin)