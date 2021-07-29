from django.contrib.auth.models import User
from rest_framework import serializers

from nora.models import Menu, MenuUser, Ingredient, Profile


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'ingredient', 'date_menu')

    def validate(self, data):
        menu = Menu.objects.filter(name=data.get('name'), date_menu=data.get('date_menu'))
        if menu:
            raise serializers.ValidationError({"name": "already exist name menu in this date "})
        return data

    def validated_name(self, value):
        """
        Validate name menu, return raise exception if name is None else return
        name of menu instance
        """
        if value is None:
            raise serializers.ValidationError({"name": "Name menu cant be empty"})
        return value


class SerializerSelectUserMenu(serializers.ModelSerializer):
    class Meta:
        model = MenuUser
        fields = ('user', 'menu')

    def validate(self, data):
        """
        validation so that the user can only have one menu assigned per day
        """
        menu = data.get('menu')
        user = data.get('user')
        menu_user = MenuUser.objects.filter(user=user, menu=menu, date=menu.date_menu)
        if menu_user:
            raise serializers.ValidationError({"date": "the user has already selected menu for this day"})

    def create(self, validated_data):
        """
        Create instance of model MenuUser, that is a representation of relation
        between user and menu is specific date
        """
        menu = validated_data.get('menu')
        instance = MenuUser.objects.create(user=validated_data.get('user'), menu=menu,
                                           date=menu.date_menu)
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """
    serializer of model Profile
    """

    class Meta:
        model = Profile
        fields = ('role', )


class CreateUserSerializer(serializers.ModelSerializer):
    """
    serializer of user model , save one instance of user and create one instance into model
    profile
    """
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """"
        overwrite function create for create user instance and create profile of user
        """
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        email=validated_data['email'],
                                        is_staff=False
                                        )
        profile = validated_data.pop('profile')
        user.profile.role = profile['role']
        user.profile.save()
        return user
