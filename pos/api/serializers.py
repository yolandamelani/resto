from rest_framework import serializers
# from pos_app.models import (
#     User, StatusModel, Profile, TableResto, Category, MenuResto, OrderMenu, OrderMenuDetail,
# )

from app_pos.models import (
    User, TableResto, MenuResto
)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class TableRestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableResto
        fields = ('id', 'code', 'name', 'capacity', 'table_status', 'status')

class RegisterUserSelializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True,
        validators = [UniqueValidator(queryset = User.objects.all())])
    password1 = serializers.CharField(write_only = True,
        required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True,
        required = True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                  'is_active', 'is_waitress', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required' : True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password' : 'Kata sandi dan Ulang kata sandi tidak sama...'
            })
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            is_active = validated_data['is_active'],
            is_waitress = validated_data['is_waitress'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username = username, password = password)
            if user:
                # Check the user is_activate and he/she is a waitress
                if user.is_active and user.is_waitress:
                    data['user'] = user
                else:
                    msg = 'Status pengguna tidak aktif...'
                    raise ValidationError({'message' : msg})
            else:
                msg = 'Anda tidak memiliki akses masuk...'
                raise ValidationError({'message' : msg})
        else:
            msg = 'Mohon mengisi kolom nama pengguna dan kata sandi...'
            raise ValidationError({'message' : msg})
        return data
class MenuRestoSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = MenuResto
        fields = ['id', 'code', 'name', 'description', 'price', 'image_menu', 'category', 'menu_status', 'status', 'created_on', 'last_modified']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Harga menu harus lebih dari 0.")
        return value