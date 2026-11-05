from rest_framework import serializers

from infrastructure.users.models import JobSeeker, User


class JobSeekerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        required= True,
        max_length = 50,
        error_messages = {
            "required":"Full name is required",
            "max_length":"Full name cannot exceed 50 characters ",
            "blank":"Full name cannot be blank",
            
            
        })
    phone_number = serializers.RegexField(
        regex=r"^(?:\+977)?(?:96|97|98)\d{8}$",

        error_messages={
            "required": "Phone number is required.",
            "blank": "Phone number cannot be blank.",
            "invalid": "Enter a valid Nepali phone number.",
        },
    )
    
    
    address = serializers.CharField(
        required= True,
        max_length = 100,
        error_messages = {
            "required":"address is required",
            "blank":"address cannot be blank",
            "max_length":"address cannot exceed 100 characters",
            })
    
    
    skills = serializers.CharField(
        required = True,
        error_messages = {
            "required":"Skills is required",
            "blank":"skills cannot be blank"
        })
    education = serializers.CharField(
        required = True,
        max_length = 100,
        error_messages = {
            "required":"education is required",
            "blank":"education cannot be blank",
            "max_length":"education cannot be exceed 100 characters"
        })
    
    experience = serializers.IntegerField(
        required = True,
        min_value= 0,
        error_messages = {
            "required":"experience is required",
            "blank":"experience cannot be blank",
            "min_value":"experience cannnot be negative"
            
        })
    
    class Meta:
        model = JobSeeker
        fields = (
            "id",
            "full_name",
            "phone_number",
            "address",
            "skills",
            "education",
            "experience",
            "resume",
            "created_at",
            "updated_at"
            
        )
        
        read_only_fields = (
        "user",
        "created_at",
        "updated_at",
        )
    
    
class JobseekerUserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length = 150,
        required = False
    )
        
    first_name = serializers.CharField(
        max_length = 100,
        required = False
    )      
        
    last_name = serializers.CharField(
        max_length = 100,
        required = False
    )
        
    email = serializers.EmailField(required = False)
    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
            "Provied as least on user field to update"
            )
        return attrs




class JobseekerReadSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = JobSeeker
        fields = (
            "id",
            "user",
            "full_name",
            "phone_number",
            "address",
            "skills",
            "education",
            "experience",
            "resume",
        )
        
    def get_user(self,obj):
        return {
            "username": obj.user.username,
            "first_name":obj.user.first_name,
            "last_name":obj.user.last_name,
            "email":obj.user.email,
            }
        
    
    
    
class JobseekerUpdateSerializer(serializers.ModelSerializer):
    user = JobseekerUserUpdateSerializer(required=False)
    class Meta:
        model = JobSeeker
        fields = (
            "id",
            "user",
            "full_name",
            "phone_number",
            "address",
            "skills",
            "education",
            "experience",
            "resume",
        )
        
        
    def validate(self, attrs):
            user_data = attrs.get("user",{})
            company = self.instance
            
            if "username" in user_data:
                username_exists = User.objects.filter(
                    username =user_data["username"]
                ).exclude(id=company.user_id).exists()
                if username_exists:
                    raise serializers.ValidationError({
                        "user": {"username": "This username  is already registered."}
                    })
            
            if "email" in user_data:
                username_exists = User.objects.filter(
                    email__iexact =user_data["email"]# __iexact :case-insensitive exact matching
                ).exclude(id=company.user_id).exists()
                if username_exists:
                    raise serializers.ValidationError({
                        "user": {"username": "This username  is already registered."}
                })
                    
                    
            return attrs