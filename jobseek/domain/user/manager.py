from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager

class UserProfileManager(Manager):
    def get_id_by_user(self, user):
        user_profile = self.get_or_raise_403_by_user(user=user)
        return user_profile.user_profile_id

    def get_or_raise_401_by_user(self, user):
        try:
            user_profile = self.get(user=user)
            return user_profile

        except ObjectDoesNotExist:
            raise Exception("Error") #AuthenticationFailed()

    def get_or_raise_403_by_user(self, user):
        try:
            user_profile = self.get(user=user)
            return user_profile

        except ObjectDoesNotExist:
            raise Exception("Error") #NoMatchedUserProfile()

    def get_or_raise_403_by_id(self, user_profile_id):
        try:
            user_profile = self.get(user_profile_id=user_profile_id)
            return user_profile

        except ObjectDoesNotExist:
            raise Exception("Error") #NoMatchedUserProfile()

    def get_or_raise_403_by_customer_id(self, customer_id):
        try:
            user_profile = self.get(customer_id=customer_id)
            return user_profile

        except ObjectDoesNotExist:
            raise Exception("Error") #NoMatchedUserProfile()


