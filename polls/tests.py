from django.test import TestCase, Client
from django.urls import reverse
from .models import Topic, Subject, TopicOwner, Vote, Ranking
from user_app.models import CustomUser
from django.utils import timezone


class PollsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email="testuser@email.com", password="12345")
        self.topic = Topic.objects.create(topic_text="Test Topic", pub_date=timezone.now())
        self.subject = Subject.objects.create(
            topic=self.topic, subject_text="Test Subject", pub_date=timezone.now()
        )
        self.topic_owner = TopicOwner.objects.create(user=self.user, topic=self.topic)

        # Create a topic that a client has access to
        # Create a topic that a client doesn't have access to
        # Create a topic that a client has access to but is not the owner

    def test_home_view_render(self):
        response = self.client.get(reverse("polls:home"))
        self.client.login(email="testemail@email.com", password="12345")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "polls/home.html")

    def test_home_view_render_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("polls:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "polls/home.html")
        self.assertNotContains(response, "New Topic")
        self.assertNotContains(response, "Suggest Topic")

    def test_topics_search_authenticated(self):
        response = self.client.post(reverse("polls:topics_search"), {"search": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "polls/partials/topics-search.html")

    def test_topics_search_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse("polls:topics_search"), {"search": "Test"})

        self.assertTemplateUsed(response, "polls/partials/topics-search.html")

    # def test_home_view(self):
    #     response = self.client.get(reverse("polls:home"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "polls/home.html")

    # def test_topics_search_view(self):
    #     response = self.client.post(reverse("polls:topics_search"), {"search": "Test"})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "polls/partials/topics-search.html")

    # def test_topic_detail_view(self):
    #     response = self.client.get(reverse("polls:topic_detail", args=[self.topic.id]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "polls/topic-detail.html")

    # def test_random_topic_detail_view(self):
    #     response = self.client.get(reverse("polls:random_topic_detail"))
    #     self.assertEqual(response.status_code, 302)  # Redirects to topic detail

    # def test_render_modal_view(self):
    #     # self.client.login(username="testuser", password="12345")
    #     self.client.login(email="testuser@email.com", password="12345")
    #     response = self.client.get(reverse("polls:render_modal"), {"trigger": "new-topic"})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "polls/modals/new-topic.html")

    # def test_add_topic_view(self):
    #     self.client.login(email="testuser@email.com", password="12345")
    #     response = self.client.post(
    #         reverse("polls:add_topic"),
    #         {"topic": "New Topic", "reference-link": "http://example.com", "btn-save-return": True},
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_suggest_topic_view(self):
    #     response = self.client.post(reverse("polls:suggest_topic"), {"topic": "Suggestion"})
    #     self.assertEqual(response.status_code, 200)

    # def test_add_subject_view(self):
    #     self.client.login(email="testuser@email.com", password="12345")
    #     response = self.client.post(
    #         reverse("polls:add_subject"),
    #         {
    #             "topic": self.topic.id,
    #             "subject": "New Subject",
    #             "details": "Details about the subject",
    #             "btn-save-return": True,
    #         },
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_load_subjects_view(self):
    #     response = self.client.get(reverse("polls:load_subjects"), {"topic": self.topic.id})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "polls/partials/subjects.html")

    # def test_sort_subjects_view(self):
    #     self.client.login(email="testuser@email.com", password="12345")
    #     response = self.client.post(
    #         reverse("polls:sort_subjects"),
    #         {"topic": self.topic.id, "subject": [self.subject.id], "save-ballot-btn": True},
    #     )
    #     self.assertEqual(response.status_code, 200)
