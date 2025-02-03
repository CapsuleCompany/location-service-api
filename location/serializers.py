from rest_framework import serializers
from .models import Address, City, State, Country


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "address_line_1",
            "address_line_2",
            "postal_code",
            "city",
            "state",
            "country",
            "latitude",
            "longitude",
            "is_billing",
        ]

    def to_internal_value(self, data):
        address_line_1 = data.get("address_line_1", "").strip().title()
        address_line_2 = data.get("address_line_2", "").strip().upper()
        city_name = data.get("city", "").strip().upper()
        state_name = data.get("state", "").strip().upper()
        country_code = data.get("country", "").strip().upper()
        try:
            country, _ = Country.objects.get_or_create(code=country_code)
            state, _ = State.objects.get_or_create(name=state_name, country=country)
            city, _ = City.objects.get_or_create(name=city_name, state=state, country=country)
        except Exception as e:
            raise serializers.ValidationError({"error": f"Error creating location objects: {str(e)}"})

        data["city"] = city.pk
        data["state"] = state.pk
        data["country"] = country.pk
        data["address_line_1"] = address_line_1
        data["address_line_2"] = address_line_2
        validated_data = super().to_internal_value(data)
        return validated_data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["city"] = instance.city.name if instance.city else None
        data["state"] = instance.state.name if instance.state else None
        data["country"] = instance.country.code if instance.country else None
        return data

    def create(self, validated_data):
        user = self.context.get("user", "")
        validated_data["user_id"] = user.user_id if user else None

        return Address.objects.get_or_create(**validated_data)[0]

    def update(self, instance, validated_data):
        city_name = validated_data.pop("city", None)
        state_name = validated_data.pop("state", None)
        country_code = validated_data.pop("country", None)

        if city_name and state_name and country_code:
            country, _ = Country.objects.get_or_create(code=country_code)
            state, _ = State.objects.get_or_create(name=state_name, country=country)
            city, _ = City.objects.get_or_create(name=city_name, state=state, country=country)

            validated_data["city"] = city
            validated_data["state"] = state
            validated_data["country"] = country

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance