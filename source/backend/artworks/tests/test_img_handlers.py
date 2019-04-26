import os
import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from ..models import ArtworkDetails, ArtworkImages
from ..img_handlers import ImgPathHandler, ImgManipulationHandler


def create_temp_test_img_file(img_name, img_file_format):
    temp_img_file = tempfile.NamedTemporaryFile()
    img = Image.new('RGB', size=(1200, 950), color=0)
    img.save(temp_img_file, format=f'{img_file_format}')
    temp_img_file.name = f'{img_name}' + '.' + f'{img_file_format}'
    temp_img_file.seek(0)
    return temp_img_file

def create_artwork_test_obj(img_file):
    artwork_details = ArtworkDetails.objects.create(
        title='#sTArry niGHT 1!8.,8?9;  (vInCEnt: vAN GÖogH)'
    )

    artwork_img = ArtworkImages.objects.create(
        artwork_details=artwork_details,
        img=SimpleUploadedFile(
            name=img_file.name,
            content=img_file.read()
        )
    )

    uploaded_artwork = []
    uploaded_artwork.append(artwork_details)
    uploaded_artwork.append(artwork_img)
    return uploaded_artwork


@override_settings(
    # os.path.realpath returns the absolute path,
    # not just the path prefixed with a symlink.
    MEDIA_ROOT=os.path.realpath(tempfile.TemporaryDirectory(
        prefix='biancabasan_test_files').name))
class TestImgPathHandler(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_img = create_temp_test_img_file('starry_night', 'jpeg')
        artwork_test_obj = create_artwork_test_obj(test_img)
        uploaded_artwork_img = artwork_test_obj[1]
        cls.img_path_handler_obj = ImgPathHandler(uploaded_artwork_img)

        print('\nTemp test directories and files are being created at path:\n'
            + uploaded_artwork_img.img.path)
    
    def test_artwork_title_formatting(self):
        formatted_title = self.img_path_handler_obj.artwork_title

        self.assertEqual(formatted_title, 'starry_night_1889__vincent_van_gogh')

    def test_new_img_path(self):
        initial_img_path = self.img_path_handler_obj.initial_img_path
        new_img_path = self.img_path_handler_obj.new_img_path

        self.assertEqual(
            new_img_path,
            (initial_img_path + '/' + 'starry_night_1889__vincent_van_gogh')
        )

    def test_mkdir_from_artwork_title(self):
        new_dir = self.img_path_handler_obj.mkdir_from_artwork_title()
        new_img_path = self.img_path_handler_obj.new_img_path
        os.chdir(new_dir)

        self.assertEqual(os.getcwd(), new_img_path)


class TestImgManipulationsHandler(TestCase):
    @classmethod
    def setUpTestData(cls):
        created_test_img = create_temp_test_img_file('starry_night', 'jpeg')
        cls.test_img = Image.open(created_test_img)

    def test_resize_img_proportionally(self):
        resized_img = ImgManipulationHandler(
            self.test_img,
            1024
        ).resize_img_proportionally()

        self.assertEqual(resized_img.width, 1024)
        self.assertEqual(resized_img.height, 811)