from unittest.mock import patch

from django.contrib.auth.models import User
from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse

from .models import Chat


class ChatErrorHandlingTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="pixel-user", password="test-password")
		self.chat = Chat.objects.create(title="test-chat", user=self.user)
		self.client.force_login(self.user)
		self.url = reverse("chat_detail", kwargs={"chat_id": self.chat.title})

	def test_invalid_generation_form_renders_field_errors(self):
		response = self.client.post(self.url, {"prompt": ""})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please correct the following")
		self.assertContains(response, "This field is required.")

	def test_generation_failure_shows_safe_feedback_and_logs_exception(self):
		with patch("chat.views.generate_image", side_effect=RuntimeError("private model details")):
			with self.assertLogs("chat", level="ERROR"):
				response = self.client.post(self.url, {"prompt": "A peaceful mountain lake"})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "We couldn't generate the image.")
		self.assertNotContains(response, "private model details")

	def test_missing_chat_keeps_django_404_response(self):
		response = self.client.get(reverse("chat_detail", kwargs={"chat_id": "missing-chat"}))

		self.assertEqual(response.status_code, 404)

	def test_chat_creation_database_failure_shows_friendly_message(self):
		with patch("chat.views.Chat.objects.create", side_effect=DatabaseError("database internals")):
			with self.assertLogs("chat", level="ERROR"):
				response = self.client.post(reverse("chat_detail", kwargs={"chat_id": "none"}), {
					"title": "another-chat",
				})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "We couldn't create your chat.")
		self.assertNotContains(response, "database internals")
