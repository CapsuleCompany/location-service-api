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
    city = CitySerializer()
    state = StateSerializer()
    country = CountrySerializer()

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

        data["city"] = city
        data["state"] = state
        data["country"] = country
        data["address_line_1"] = address_line_1
        data["address_line_2"] = address_line_2
        return data

    def to_representation(self, instance):
        return {
            "id": str(instance.id),
            "address_line_1": instance.address_line_1,
            "address_line_2": instance.address_line_2,
            "postal_code": instance.postal_code,
            "city": instance.city.name if instance.city else None,
            "state": instance.state.name if instance.state else None,
            "country": instance.country.code if instance.country else None,
            "is_billing": instance.is_billing,
        }

    def create(self, validated_data):
        user = self.context.pop("user", "")
        validated_data["user_id"] = user.user_id if user else None
        return Address.objects.get_or_create(**validated_data)[0]

    def update(self, instance, validated_data):
        address_1 = validated_data.pop("address_line_1", {})
        postal_code = validated_data.pop("postal_code", {})
        city_name = validated_data.pop("city", {})
        state_name = validated_data.pop("state", {})
        country_code = validated_data.pop("country", None)

        if not address_1:
            raise serializers.ValidationError({"error": "Address 1 is required"})
        if not postal_code:
            raise serializers.ValidationError({"error": "Postal Code is required"})
        if not city_name:
            raise serializers.ValidationError({"error": "City is required."})
        if not state_name:
            raise serializers.ValidationError({"error": "State is required."})
        if not country_code:
            raise serializers.ValidationError({"error": "Country is required."})

        country, _ = Country.objects.get_or_create(code=country_code.code)
        state, _ = State.objects.get_or_create(name=state_name.name, country=country)
        city, _ = City.objects.get_or_create(name=city_name.name, state=state, country=country)

        validated_data["address_line_1"] = address_1
        validated_data["postal_code"] = postal_code
        validated_data["city"] = city
        validated_data["state"] = state
        validated_data["country"] = country

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance