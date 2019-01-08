from rest_framework import serializers
from users.models import User
from rest_auth.serializers import PasswordResetSerializer as OldPasswordResetSerializer
from django.conf import settings

class UserSerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'send_email_for_downtime', 
                  'send_email_for_issues')


class UserPublicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',)

class PasswordResetSeralizer(OldPasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'extra_email_context': {'base_url': settings.BASE_URL},
            'email_template_name': 'password_reset_email.txt',
            'subject_template_name': 'password_reset_subject_text.txt'
        }
        self.reset_form.save(**opts)