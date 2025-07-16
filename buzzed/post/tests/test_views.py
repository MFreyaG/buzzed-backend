from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from drink.models import Drink
from post.models import Post, PostImage, PostVideo
from user.models import User


class PostTestCase(APITestCase):
    fixtures = [
        "ingredients.json",
        "addresses.json",
        "users.json",
        "stores.json",
        "drinks.json",
        "posts.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="johnsnow")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.get(user__username="johnsnow")

    def test_get_post(self):
        filter_data = {"user": self.user.pk}
        response = self.client.get(reverse("post"), data=filter_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["user"]["id"], str(self.user.pk))
        self.assertEqual(
            response.data[0]["drink"]["id"], "11111111-1111-4111-a111-000000000001"
        )
        self.assertEqual(response.data[0]["review"], self.post.review)
        self.assertEqual(response.data[0]["score"], self.post.score)

    def test_get_post_with_wrong_data_raises_bad_request(self):
        filter_data = {"user": 1}
        response = self.client.get(reverse("post"), data=filter_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_post(self):
        drink = Drink.objects.get(name="The Suit Up")
        post_data = {
            "user": self.user.pk,
            "drink": drink.pk,
            "score": 8,
            "review": "I've never had anything so elegant in Westeros",
        }
        response = self.client.post(reverse("post"), data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(pk=response.data["id"])
        self.assertEqual(post_data["user"], post.user.pk)
        self.assertEqual(post_data["drink"], post.drink.pk)
        self.assertEqual(post_data["score"], post.score)
        self.assertEqual(post_data["review"], post.review)

    def test_post_post_with_wrong_data_raises_bad_request(self):
        post_data = {}
        response = self.client.post(reverse("post"), data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostDetailTestCase(APITestCase):
    fixtures = [
        "ingredients.json",
        "addresses.json",
        "users.json",
        "stores.json",
        "drinks.json",
        "posts.json",
    ]

    def setUp(self):
        self.post = Post.objects.get(user__username="elliewilliams")
        self.user = User.objects.get(username="elliewilliams")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_post(self):
        updated_post_data = {"score": 9, "review": "One of the best drinks in Jackson."}
        response = self.client.patch(
            reverse("post-detail", args=[self.post.pk]),
            data=updated_post_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.score, updated_post_data["score"])
        self.assertEqual(self.post.review, updated_post_data["review"])
        self.assertEqual(self.post.user.pk, response.data["user"])

    def test_update_post_with_wrong_pk_raises_not_found(self):
        updated_post_data = {"score": 9, "review": "One of the best drinks in Jackson."}
        response = self.client.patch(
            reverse("post-detail", args=["11111111-1111-4111-a111-000000000002"]),
            data=updated_post_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_with_wrong_data_raises_bad_request(self):
        updated_post_data = {
            "score": None,
            "review": "One of the best drinks in Jackson.",
        }
        response = self.client.patch(
            reverse("post-detail", args=[self.post.pk]),
            data=updated_post_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_post(self):
        response = self.client.delete(
            reverse("post-detail", args=[self.post.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_delete_post_with_wrong_pk_raises_not_found(self):
        response = self.client.delete(
            reverse("post-detail", args=["11111111-1111-4111-a111-000000000002"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostImageTestCase(APITestCase):
    fixtures = [
        "ingredients.json",
        "addresses.json",
        "users.json",
        "stores.json",
        "drinks.json",
        "posts.json",
        "post_images.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="elliewilliams")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.get(pk="11111111-1111-4111-a111-000000000001")

    def test_post_image_post(self):
        post_image_data = {
            "post": self.post.pk,
            "image_url": "https://example.com/jackson_review_image.jpg",
        }
        response = self.client.post(
            reverse("post-image"), data=post_image_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_image = PostImage.objects.get(pk=response.data["id"])
        self.assertEqual(response.data["post"], post_image.post.pk)
        self.assertEqual(response.data["image_url"], post_image.image_url)

    def test_post_image_with_wrong_data_raises_bad_request(self):
        post_image_data = {}
        response = self.client.post(
            reverse("post-image"), data=post_image_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_image_post(self):
        filter_data = {"post": self.post.pk}
        response = self.client.get(reverse("post-image"), data=filter_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["post"]["id"], str(self.post.pk))
        self.assertEqual(response.data[0]["image_url"], "https://example.com/winterfell_review_image.jpg")
    
    def test_get_image_post_with_wrong_data_raises_bad_request(self):
        filter_data = {"post": 1}
        response = self.client.get(reverse("post-image"), data=filter_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostImageDetailTestCase(APITestCase):
    fixtures = [
        "ingredients.json",
        "addresses.json",
        "users.json",
        "stores.json",
        "drinks.json",
        "posts.json",
        "post_images.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="elliewilliams")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post_image = PostImage.objects.get(
            pk="11111111-1111-4111-a111-000000000001"
        )

    def test_delete_post_image(self):
        response = self.client.delete(
            reverse("post-image-detail", args=[self.post_image.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PostImage.objects.filter(pk=self.post_image.pk).exists())

    def test_delete_post_image_with_wrong_pk_raises_not_found(self):
        response = self.client.delete(
            reverse("post-image-detail", args=["11111111-1111-4111-a111-000000000002"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PostVideoTestCase(APITestCase):
    fixtures = [
        "ingredients.json",
        "addresses.json",
        "users.json",
        "stores.json",
        "drinks.json",
        "posts.json",
        "post_videos.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="elliewilliams")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.get(pk="11111111-1111-4111-a111-000000000001")

    def test_post_video_post(self):
        post_video_data = {
            "post": self.post.pk,
            "video_url": "https://example.com/jackson_review_video.mp4",
        }
        response = self.client.post(
            reverse("post-video"), data=post_video_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_video = PostVideo.objects.get(pk=response.data["id"])
        self.assertEqual(response.data["post"], post_video.post.pk)
        self.assertEqual(response.data["video_url"], post_video.video_url)

    def test_post_video_with_wrong_data_raises_bad_request(self):
        post_video_data = {}
        response = self.client.post(
            reverse("post-video"), data=post_video_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_video_post(self):
        filter_data = {"post": self.post.pk}
        response = self.client.get(reverse("post-video"), data=filter_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["post"]["id"], str(self.post.pk))
        self.assertEqual(response.data[0]["video_url"], "https://example.com/winterfell_review_video.mp4")
    
    def test_get_video_post_with_wrong_data_raises_bad_request(self):
        filter_data = {"post": 1}
        response = self.client.get(reverse("post-video"), data=filter_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
class PostVideoDetailTestCase(APITestCase):
    fixtures = [
        "ingredients.json",
        "addresses.json",
        "users.json",
        "stores.json",
        "drinks.json",
        "posts.json",
        "post_videos.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="elliewilliams")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post_video = PostVideo.objects.get(
            pk="11111111-1111-4111-a111-000000000001"
        )

    def test_delete_post_video(self):
        response = self.client.delete(
            reverse("post-video-detail", args=[self.post_video.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PostVideo.objects.filter(pk=self.post_video.pk).exists())

    def test_delete_post_video_with_wrong_pk_raises_not_found(self):
        response = self.client.delete(
            reverse("post-video-detail", args=["11111111-1111-4111-a111-000000000002"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
