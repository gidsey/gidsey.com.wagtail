import pytest
from wagtail import images


@pytest.mark.django_db(transaction=False, reset_sequences=False, databases=None)
class TestImageSlug:
    Image = images.get_image_model()
    title = 'test wiTh a New Image Title & Slug'
    file = 'tests/test_data/test.jpg'
    copyright_default = 'Chris Guy'
    copyright_new = 'laboris odio'

    def test_image_slug(self, auto_login_user):
        client, user = auto_login_user()

        assert len(self.Image.objects.all()) == 0

        self.Image.objects.create(
            title=self.title,
            file=self.file,
            uploaded_by_user=user
        )

        new_image = self.Image.objects.first()
        assert len(self.Image.objects.all()) == 1
        assert new_image.slug == 'test-with-a-new-image-title-slug'

        new_image.save()
        assert new_image.slug != 'test-with-a-new-image-title-slug'
        assert len(new_image.slug) == len('test-with-a-new-image-title-slug') + 5

    def test_image_copyright_default(self, auto_login_user):
        client, user = auto_login_user()

        assert len(self.Image.objects.all()) == 0

        self.Image.objects.create(
            title=self.title,
            file=self.file,
            uploaded_by_user=user
        )

        new_image = self.Image.objects.first()
        assert len(self.Image.objects.all()) == 1
        assert new_image.copyright == self.copyright_default

    def test_image_copyright_new(self, auto_login_user):
            client, user = auto_login_user()

            assert len(self.Image.objects.all()) == 0

            self.Image.objects.create(
                title=self.title,
                file=self.file,
                uploaded_by_user=user,
                copyright=self.copyright_new
            )

            new_image = self.Image.objects.first()
            assert len(self.Image.objects.all()) == 1
            assert new_image.copyright == self.copyright_new

