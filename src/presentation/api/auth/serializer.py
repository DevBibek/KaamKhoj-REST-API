import re

from rest_framework import serializers

from infrastructure.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        clean_email = value.strip()
        if not re.match(r"^[A-Za-z0-9._%+-]+@gmail\.com$", clean_email):
            raise serializers.ValidationError(
            "Only Gmail addresses are allowed."
            )
        if any(char.isupper() for char in clean_email):
                raise serializers.ValidationError("Email must contain only lowercase letters.")
            
        return clean_email
    
    def validate_password(self,value):
        if len(value)<8:
            raise serializers.ValidationError("password must be at least 8 characters")
        return value
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
        )
        extra_kwargs = { 
            "username":{"required":True},
            "first_name":{"required":True},
            "last_name":{"required":True},
            "email":{"required":True},
            "password":{"required":True,
                        "write_only":True,
                        },
            "role":{"required":True},
        }
    
    
    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]
    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "At least one field is required to update."
            )
        return attrs    

    
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)