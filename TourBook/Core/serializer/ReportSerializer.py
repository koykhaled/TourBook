from rest_framework import serializers
from ..models.report import Report
from accounts.serializers import UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    respondent = UserSerializer(read_only=True)
    complainant = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('reason', 'report_type', 'respondent', 'complainant')

    def complainant_data(self, represent):
        complainant_data = represent.pop('complainant')
        complainant_data = {
            "complainant": complainant_data['username'],
            "complainant_role": complainant_data['role']
        }
        represent.update(complainant_data)

    def respondent_data(self, represent):
        respondent_data = represent.pop('respondent')
        respondent_data = {
            "respondent": respondent_data['username'],
        }
        represent.update(respondent_data)

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        self.complainant_data(represent)
        self.respondent_data(represent)
        return represent
