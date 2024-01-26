from rest_framework import serializers
from superadmin.models import superadmin_data,emra_coin,external_expenses,subscription,commision,third_party_user
from apiapp.models import ProfileFinder
class superadminSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField()

class emra_coin_all_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    country = serializers.CharField()
    currency = serializers.CharField()
    emra_coin_value = serializers.CharField()

class emra_coin_Serializer(serializers.Serializer):
    country = serializers.CharField()
    currency = serializers.CharField()
    emra_coin_value = serializers.CharField()

    def create(self, data):
        return emra_coin.objects.create(
            country = data['country'],
            currency = data['currency'],
            emra_coin_value = data['emra_coin_value'],
        )

class external_expenses_all_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    details = serializers.CharField()
    to = serializers.CharField()
    date = serializers.CharField()
    currency = serializers.CharField()
    amount = serializers.CharField()
    frequency = serializers.CharField()
    attachment=serializers.CharField()

class external_expenses_Serializer(serializers.Serializer):
    details = serializers.CharField()
    to = serializers.CharField()
    date = serializers.CharField()
    currency = serializers.CharField()
    amount = serializers.CharField()
    frequency = serializers.CharField()
    attachment=serializers.CharField()

    def create(self, data):
        return external_expenses.objects.create(
            details = data['details'],
            to = data['to'],
            date = data['date'],
            currency = data['currency'],
            amount = data['amount'],
            frequency = data['frequency'],
            attachment = data['attachment']

        )
        
class subscription_all_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    Subscription_Country = serializers.CharField()
    Title_of_the_plan = serializers.CharField()
    Type_Of_Subscription = serializers.CharField()
    Amount_with_ad = serializers.IntegerField()
    Amount_without_ad = serializers.IntegerField()
    Validity = serializers.CharField()
    Option1 = serializers.CharField()
    value1 = serializers.CharField()
    Option2 = serializers.CharField()
    value2 = serializers.CharField()
    Option3 = serializers.CharField()
    value3 = serializers.CharField()
    # class Meta:
    #     model = subscription
    #     fields = "__all__"

class subscription_Serializer(serializers.ModelSerializer):
     class Meta:
        model = subscription
        fields = "__all__"
    # Subscription_Country = serializers.CharField()
    # Title_of_the_plan = serializers.CharField()
    # Type_Of_Subscription = serializers.CharField()
    # Amount_with_ad = serializers.IntegerField()
    # Amount_without_ad = serializers.IntegerField()
    # Validity_from = serializers.DateField()
    # Validity_to=serializers.DateField()
    # Option1 = serializers.CharField()
    # value1 = serializers.CharField()
    # Option2 = serializers.CharField()
    # value2 = serializers.CharField()
    # Option3 = serializers.CharField()
    # value3 = serializers.CharField()
    
    # def create(self, data):
    #     return subscription.objects.create(
    #         Subscription_Country = data['Subscription_Country'],
    #         Title_of_the_plan = data['Title_of_the_plan'],
    #         Type_Of_Subscription = data['Type_Of_Subscription'],
    #         Amount_with_ad = data['Amount_with_ad'],
    #         Amount_without_ad = data['Amount_without_ad'],
    #         Validity_from = data['Validity_from'],
    #         Validity_to = data['Validity_to'],
    #         Option1 = data['Option1'],
    #         value1 = data['value1'],
    #         Option2 = data['Option2'],
    #         value2 = data['value2'],
    #         Option3 = data['Option3'],
    #         value3 = data['value3']
            
    #     )

class commision_all_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    commision_start = serializers.CharField()
    commision_end = serializers.CharField()
    to_whom = serializers.CharField()
    from_whom = serializers.CharField()
    for_what = serializers.CharField()
    how_many = serializers.CharField()
    subscription = serializers.CharField()
    commision = serializers.CharField()
    how_many_coin = serializers.CharField()
    how_many_views = serializers.CharField()

class commision_Serializer(serializers.ModelSerializer):
     class Meta:
        model = commision
        fields = "__all__"

class third_party_user_all_serializer(serializers.ModelSerializer):
    class Meta:
        model = third_party_user
        fields = "__all__"

class third_party_user_serializer(serializers.ModelSerializer):
    class Meta:
        model = third_party_user
        fields = ["first_name","last_name","email","phone_no","password","access_privilage"]
        
class profile_manager_serializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileFinder
        fields = "__all__"