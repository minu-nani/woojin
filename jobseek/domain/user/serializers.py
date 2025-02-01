from rest_framework import serializers

from .models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d")
    last_login = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = User
        fields = ('username', 'id', 'is_active', 'first_name', 'is_authenticated', 'date_joined', 'last_login')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )


class UserProfileCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'user',
            'name',
            'tel_num',
            'birthday',
            'sex',
        )

    def create(self, validated_data):
        user = User()
        user.email = validated_data['user']['email']
        user.username = validated_data['user']['email']
        user.password = validated_data['user']['password']
        user.save()

        user_profile, is_created = UserProfile.objects.get_or_create(user=user)

        user_update_serializer = UserProfileUpdateSerializer(user_profile, data=validated_data)
        user_update_serializer.is_valid()
        user_update_serializer.save()
        return user_profile


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'name',
            'tel_num',
            'birthday',
            'sex',
        )

    def save(self):
        if 'name' in self.initial_data.keys():
            self.instance.name = self.initial_data['name']
            self.instance.masked_name = self.instance.get_masked_name(self.initial_data['name'])

        if 'tel_num' in self.initial_data.keys():
            self.instance.tel_num = self.initial_data['tel_num']
            self.instance.masked_tel_num = self.instance.get_masked_tel_num(self.validated_data['tel_num'])

        if 'birthday' in self.initial_data.keys():
            self.instance.birthday = self.initial_data['birthday']

        if 'sex' in self.initial_data.keys():
            self.instance.sex = self.initial_data['sex']
        return self.instance.save()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
        )


class UserAndUserProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'user',
            'name',
            'tel_num',
            'birthday',
            'sex',
        )

    def update(self, instance, validated_data):
        if 'name' in self.initial_data.keys():
            self.instance.name = self.initial_data['name']
            self.instance.masked_name = self.instance.get_masked_name(self.initial_data['name'])

        if 'tel_num' in self.initial_data.keys():
            self.instance.tel_num = self.initial_data['tel_num']
            self.instance.masked_tel_num = self.instance.get_masked_tel_num(self.validated_data['tel_num'])

        if 'birthday' in self.initial_data.keys():
            self.instance.birthday = self.initial_data['birthday']

        if 'sex' in self.initial_data.keys():
            self.instance.sex = self.initial_data['sex']
        return self.instance.save()