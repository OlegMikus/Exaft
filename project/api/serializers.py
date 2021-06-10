from rest_framework.serializers import ModelSerializer

from api.models import Organization


class OrgSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
