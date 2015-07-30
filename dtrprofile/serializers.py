
from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers
from dtrprofile.models import UserPic, UserMsg, UserProfile, UserFlag

# ------------------------------------------------------------------------------

class UserMsgSerializer(serializers.ModelSerializer):
    """Messages with authuser, shown when lookig at a user's profile page."""
    created = serializers.DateTimeField(format='iso-8601')
    is_read = serializers.ReadOnlyField()
    is_replied = serializers.ReadOnlyField()

    class Meta:
        model = UserMsg
        fields = ('id', 'from_user', 'to_user', 
                  'created', 'text', 'is_read', 'is_replied')

# ------------------------------------------------------------------------------

'''
class UserProfileSerializer(serializers.ModelSerializer):
    """Returns full user profile."""
    pic = serializers.ReadOnlyField(source='profile.pic.pk')
    age = serializers.ReadOnlyField(source='profile.age')
    gender = serializers.ReadOnlyField(source='profile.gender')
    crc = serializers.ReadOnlyField(source='profile.crc') # <-- Need to get language version of crc! Hoe to do that?
    city = serializers.ReadOnlyField(source='profile.city.pk')

    class Meta:
        model = User
        fields = ('id', 'username', 'pic', 'age', 'gender', 
                  'crc', 'city', 'country', 'lat', 'lng')
'''

class UserPnaslSerializer(serializers.ModelSerializer):
    """Returns only PNASL (picture, name, age, sex, location) of user."""
    pic = serializers.ReadOnlyField(source='profile.pic.pk')
    age = serializers.ReadOnlyField(source='profile.age')
    gender = serializers.ReadOnlyField(source='profile.gender')
    crc = serializers.ReadOnlyField(source='profile.crc') # <-- Need to get language version of crc! How to do that?
    city = serializers.ReadOnlyField(source='profile.city.pk')
    country = serializers.ReadOnlyField(source='profile.country.pk')
    lat = serializers.ReadOnlyField(source='profile.lat')
    lng = serializers.ReadOnlyField(source='profile.lng')

    class Meta:
        model = User
        fields = ('id', 'username', 'pic', 'age', 'gender', 
                  'crc', 'city', 'country', 'lat', 'lng')

class InboxSerializer(serializers.ModelSerializer):
    """Messages authuser received or sent, shown on the "inbox" views."""
    created = serializers.DateTimeField(format='iso-8601')
    is_read = serializers.ReadOnlyField()
    is_replied = serializers.ReadOnlyField()
    from_user = UserPnaslSerializer()
    to_user = UserPnaslSerializer()

    class Meta:
        model = UserMsg
        fields = ('id', 'created', 'text', 'from_user', 'to_user',
                  'is_read', 'is_replied', 'is_blocked')

# ------------------------------------------------------------------------------


