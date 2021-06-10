from django.contrib import admin

from api.models import Organization, AreasOfActivity, TopManagers, Links


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'location', 'creation_date')
    ordering = ('pk',)


@admin.register(AreasOfActivity)
class AreasOfActivityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company', 'title')
    ordering = ('pk',)


@admin.register(TopManagers)
class TopManagersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'company')
    ordering = ('pk',)


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company', 'inst', 'facebook', 'twitter', 'off_site',)
    ordering = ('pk',)
