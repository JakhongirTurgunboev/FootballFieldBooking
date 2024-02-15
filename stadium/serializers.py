from rest_framework import serializers

from .models import FootballField, FootballFieldImages, Booking


class FootballFieldImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballFieldImages
        fields = ['image', 'football_field']


class FootballFieldSerializer(serializers.ModelSerializer):
    images = FootballFieldImagesSerializer(many=True, read_only=True)

    class Meta:
        model = FootballField
        fields = ['id', 'name', 'address', 'contact', 'price_per_hour', 'owner', 'latitude', 'longitude', 'images']

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist(
            'images')  # Assumes 'images' is the field name in the request
        football_field = FootballField.objects.create(**validated_data)

        for image_data in images_data:
            FootballFieldImages.objects.create(football_field=football_field, image=image_data)

        return football_field


class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
