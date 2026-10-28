from rest_framework import serializers

from infrastructure.users.models import User


class UserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required = True,
        error_messages = {
            "required":"User email is required",
            "blank":"email cannot be blank",
            "invalid":"Enter a valaid email address",
        })
    
    role = User._meta.get_field("role").choices
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            )
