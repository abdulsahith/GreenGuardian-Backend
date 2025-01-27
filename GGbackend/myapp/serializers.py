from rest_framework import serializers
from .models import MachinePyro,MachineBsfl,Admingreen,Usergreen
class Pyro_serial(serializers.ModelSerializer):
    class Meta:
        model=MachinePyro
        fields = '__all__'

class bsfl_serial(serializers.ModelSerializer):
    class Meta:
        model=MachineBsfl
        fields='__all__'


class admin_serial(serializers.ModelSerializer):
    class Meta:
        model=Admingreen
        fields='__all__'
class user_serial(serializers.ModelSerializer):
    class Meta:
        model=Usergreen
        fields='__all__'
        

