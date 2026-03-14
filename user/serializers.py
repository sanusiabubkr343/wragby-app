from  rest_framework import serializers

from user.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    transaction_limit = serializers.FloatField(default=0,min_value=0)

    class Meta:
        model=User
        fields= ("username", "password", "transaction_limit",)



class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model=User
       fields= '__all__'
