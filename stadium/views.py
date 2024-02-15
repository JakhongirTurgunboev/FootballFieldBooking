from datetime import datetime, timedelta

from django.db.models import F
from django.db.models.functions import Cos, Radians, Sin, ACos
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import FootballField, FootballFieldImages, Booking
from .permissions import IsAdminOwner
from .serializers import FootballFieldSerializer, FootballFieldImagesSerializer, BookingSerializers

# Create your views here.


class FootballFieldViewSet(viewsets.ModelViewSet):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    permission_classes = (IsAdminOwner,)


class FootballFieldImagesViewSet(viewsets.ModelViewSet):
    queryset = FootballFieldImages.objects.all()
    serializer_class = FootballFieldImagesSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAdminOwner,)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializers

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name='latitude',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='User latitude',
            required=True,
        ),
        openapi.Parameter(
            name='longitude',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='User longitude',
            required=True,
        ),
        openapi.Parameter(
            name='distance',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='Search radius in kilometers',
            required=True,
        ),
        openapi.Parameter(
            name='start_time',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Start time for availability (format: YYYY-MM-DD HH:MM:SS)',
            required=False,
        ),
        openapi.Parameter(
            name='end_time',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='End time for availability (format: YYYY-MM-DD HH:MM:SS)',
            required=False,
        ),
    ],
    responses={200: openapi.Response('List of Football Fields', serializer_name='FootballFieldSerializer')},
)
@api_view(['GET'])
def find_stadium(request, *args, **kwargs):
    try:
        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))
        distance = float(request.query_params.get('distance'))

        start_time_str = request.query_params.get('start_time')
        end_time_str = request.query_params.get('end_time')

        if start_time_str:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        else:
            start_time = datetime.now()

        if end_time_str:
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        else:
            end_time = start_time + timedelta(hours=1)

        football_fields = FootballField.objects.annotate(
            distance_km=6371 * ACos(
                Cos(Radians(user_latitude)) * Cos(Radians(F('latitude'))) *
                Cos(Radians(F('longitude')) - Radians(user_longitude)) +
                Sin(Radians(user_latitude)) * Sin(Radians(F('latitude')))
            )
        ).filter(distance_km__lte=distance)

        available_fields = []

        for field in football_fields:
            existing_bookings = Booking.objects.filter(
                football_field=field,
                booking_start_time__lt=end_time,
                booking_start_time__gte=start_time
            )

            if not existing_bookings.exists():
                available_fields.append(field)

        serializer = FootballFieldSerializer(available_fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)