from rest_framework import serializers
from rest_framework.serializers import FileField
from .models import cliente, ejecutivo, User, Archivo, Servicio
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ServiciosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class dbClientesSerializer(serializers.ModelSerializer):
    def validate_nombre(self, value):
        if value == '':
            value='value'
            raise serializers.ValidationError('Nombre es obligatorio')
        return value
    
    def validate_email(self, value):
        if value == '':
            value='value'
            raise serializers.ValidationError('Email es obligatorio')
        return value

    servicios = serializers.StringRelatedField(read_only=True, many=True)
    class Meta:
        model = cliente
        fields = ('id','nombre', 'numeroContacto', 'email', 'tipoContrato', 'fechaFinContrato', 'fechaInicioContrato', 'ejecutivoCierre', 'ejecutivoActual', 'servicios', 'desistido')

class dbEjecutivosSerializer(serializers.ModelSerializer):
    def validate_nombre(self, value):
        if value == '':
            value='value'
            raise serializers.ValidationError('Nombre es obligatorio')
        return value
    
    class Meta:
        model = ejecutivo
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model= User
    fields=['id', 'name', 'email', 'password','is_superuser','is_staff','first_name','last_name']
    extra_kwargs ={
      'password': {'write_only': True}
    }

  def create(self,validated_data):
    password = validated_data.pop('password', None)
    instance = self.Meta.model(**validated_data)
    if password is not None:
        instance.set_password(password)
    instance.save()
    return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
      token = super().get_token(user)

      # Custom claims
      token['is_superuser'] = user.is_superuser
      token['name'] = user.name

      return token


