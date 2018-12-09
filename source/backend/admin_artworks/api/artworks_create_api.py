from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from PIL import Image

from .serializers import (
    ArtworkTitlesSerializer,
    ArtworkDetailsSerializer,
    ArtworkImagesSerializer,
    AddImagesSerializer, # !! REMOVE !!
)
from ..models import (
    ArtworkTitles,
    ArtworkDetails,
)


"""
Create artwork titles
"""
@api_view(['POST'])
def artwork_create_title(request):

    if request.method == 'POST':
        title_serialized = ArtworkTitlesSerializer(data = request.data)

        if title_serialized.is_valid():
            title_serialized.save()

            return Response(
                title_serialized.data,
                status = status.HTTP_201_CREATED,
                )
        
        return Response(
            title_serialized.errors,
            status = status.HTTP_400_BAD_REQUEST,
        )


"""
Create artwork details
"""
@api_view(['POST'])
def artwork_create_details(request, id):

    if request.method == 'POST':
        # Add details to a specific artwork or raise
        # exception if details already exist
        try:
            ArtworkDetails.objects.get(title_id = id)

        except ArtworkDetails.DoesNotExist:
            details_serialized = ArtworkDetailsSerializer(data = request.data)

            if details_serialized.is_valid():
                details_serialized.save(title_id = id)
    
        else:
            # Retrieve and display artwork title in exception message
            artwork_title = ArtworkTitles.objects.get(id = id)

            return Response(
                ('Unable to create new details for '
                + artwork_title.title
                + ', details already exist'),
                status = status.HTTP_409_CONFLICT
            )


"""
Add artwork images
"""
@api_view(['POST'])
# Parser classes for accepting requests with various media types
@parser_classes((MultiPartParser, FormParser))
def artwork_add_images(request):

    if request.method == 'POST':
        image_serialized = AddImagesSerializer(data = request.data)

        if image_serialized.is_valid():

            """
            Image manipulation
            """
            image = image_serialized.validated_data['image']
            image_title = str(image)

            # Load image from file
            image_file = Image.open(image_serialized.validated_data['image'])

            # Modify image
            modified_image = image_file.resize((200, 200))
            modified_image = modified_image.rotate(45)

            # Save modified image to in memory buffer and
            # change InMemoryUploadedFile to modified image
            buffer = BytesIO()
            modified_image.save(buffer, format = 'JPEG', quality = 10)
            image_serialized.validated_data['image'] = InMemoryUploadedFile(
                buffer,
                None,
                image_title,
                None,
                None,
                None
            )

            image_serialized.save()

            return Response (
                image_serialized.data,
                status = status.HTTP_201_CREATED
            )