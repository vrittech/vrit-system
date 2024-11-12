from rest_framework import serializers
from ..models import Country

class CountryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CountryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CountryWriteSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Country
        fields = ['id', 'name']

    def create(self, validated_data):
        countries_data = validated_data.get('countries', [])
        created_countries = []

        for country_data in countries_data:
            # Create a new country if no ID is provided
            if 'id' not in country_data:
                country = Country.objects.create(name=country_data['name'])
                created_countries.append(country)

        return created_countries

    def update(self, instance, validated_data):
        countries_data = validated_data.get('countries', [])
        updated_countries = []

        for country_data in countries_data:
            country_id = country_data.get('id')

            # Update an existing country if ID is provided
            if country_id:
                country = Country.objects.filter(id=country_id).first()
                if country:
                    country.name = country_data['name']
                    country.save()
                    updated_countries.append(country)
                else:
                    # Optionally, handle the case where the ID does not exist
                    # Raise an exception or handle as needed
                    pass

        return updated_countries