from django.contrib import admin
from .models import *
# Register your models here.
@admin.action(description='Create Academic Years for Batch')
def create_academic_years(modeladmin, request, queryset):
    for batch in queryset:
        starting_year = batch.batch_name.split("-")[0]
        ending_year = batch.batch_name.split("-")[1]
        for i in range(int(starting_year),int(ending_year)):
            AcademicYear.objects.create(year=str(i)+"-"+str(i+1),batch=batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id','batch_name','program')
    search_fields = ('id','batch_name','program__program_name')
    list_filter = ('program',)
    list_per_page = 25
    actions = [create_academic_years]
admin.site.register(Batch,BatchAdmin)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('id','year','batch')
    search_fields = ('id','year','batch__batch_name')
    list_filter = ('batch',)
    list_per_page = 25
admin.site.register(AcademicYear,AcademicYearAdmin)