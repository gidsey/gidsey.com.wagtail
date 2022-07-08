import pytest
from wagtail import images


@pytest.mark.django_db(transaction=False, reset_sequences=False, databases=None)
class TestImageSlug:
    Image = images.get_image_model()

    def test_image_slug(self):
        assert len(self.Image.objects.all()) == 0





