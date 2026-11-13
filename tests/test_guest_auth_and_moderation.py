import io
import re
import unittest
from unittest.mock import patch

from app import create_app
from app.extensions import db
from app.models.question import Question
from app.models.user import User


class TestConfig:
    SECRET_KEY = "test-secret-key-with-enough-entropy"
    ADMIN_USERNAME = "test-admin"
    ADMIN_PASSWORD = "test-admin-password-with-length"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False
    TESTING = True
    MAX_CONTENT_LENGTH = 26 * 1024 * 1024


class GuestAuthAndModerationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _sign_in_guest(self):
        response = self.client.get("/login")
        match = re.search(rb"Your ID: <strong>(User_\d{4})</strong>", response.data)
        self.assertIsNotNone(match)
        response = self.client.post(
            "/login",
            data={"department": "CSE", "avatar": "avatar2.webp"},
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            return User.query.one()

    def test_guest_login_assigns_pseudonymous_id_without_personal_fields(self):
        guest = self._sign_in_guest()

        self.assertRegex(guest.anonymous_id, r"^User_\d{4}$")
        self.assertEqual(guest.name, guest.anonymous_id)
        self.assertEqual(guest.department, "CSE")
        self.assertEqual(guest.avatar, "avatar2.webp")
        self.assertFalse(guest.is_admin)
        self.assertFalse(hasattr(guest, "email"))
        self.assertFalse(hasattr(guest, "google_sub"))

    def test_question_is_private_until_admin_approval(self):
        guest = self._sign_in_guest()
        response = self.client.post(
            "/qa/ask",
            data={
                "title": "Pending question",
                "body": "This should not be public yet.",
                "subject": "Calculus",
                "is_anonymous": "y",
            },
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            question = Question.query.one()
        self.assertEqual(question.user_id, guest.id)
        self.assertEqual(question.status, "pending")
        self.assertNotIn(b"Pending question", self.client.get("/qa/").data)
        self.assertEqual(self.client.get(f"/qa/{question.id}").status_code, 200)

        stranger = self.app.test_client()
        self.assertEqual(stranger.get(f"/qa/{question.id}").status_code, 404)

        admin = self.app.test_client()
        response = admin.post(
            "/admin-login",
            data={
                "username": TestConfig.ADMIN_USERNAME,
                "password": TestConfig.ADMIN_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)
        review_page = admin.get("/admin/qa")
        self.assertEqual(review_page.status_code, 200)
        self.assertIn(b"Pending question", review_page.data)
        response = admin.post(f"/admin/qa/{question.id}/approve")
        self.assertEqual(response.status_code, 302)

        with self.app.app_context():
            reviewed_question = db.session.get(Question, question.id)
            self.assertEqual(reviewed_question.status, "approved")
        self.assertIn(b"Pending question", stranger.get("/qa/").data)

    def test_admin_login_is_rate_limited(self):
        for _ in range(5):
            response = self.client.post(
                "/admin-login",
                data={"username": "test-admin", "password": "wrong-password"},
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/admin-login",
            data={"username": "test-admin", "password": "wrong-password"},
        )
        self.assertEqual(response.status_code, 429)

    def test_user_uploads_are_private_until_approved_then_public(self):
        guest = self._sign_in_guest()

        with patch("app.routes.paper.save_file", return_value="papers/calculus.pdf"):
            paper_response = self.client.post(
                "/papers/upload",
                data={
                    "subject": "Calculus",
                    "exam_type": "semester",
                    "year": "2024",
                    "file": (io.BytesIO(b"%PDF-1.4 test"), "calculus.pdf", "application/pdf"),
                },
                content_type="multipart/form-data",
            )
        self.assertEqual(paper_response.status_code, 302)

        with patch("app.routes.materials.save_file", return_value="materials/physics.pdf"):
            material_response = self.client.post(
                "/materials/upload",
                data={
                    "title": "Physics Notes",
                    "subject": "Physics",
                    "category": "Notes",
                    "description": "Lecture notes",
                    "file": (io.BytesIO(b"%PDF-1.4 test"), "physics.pdf", "application/pdf"),
                },
                content_type="multipart/form-data",
            )
        self.assertEqual(material_response.status_code, 302)

        link_response = self.client.post(
            "/materials/upload",
            data={
                "title": "External Notes",
                "subject": "Physics",
                "category": "Notes",
                "description": "Linked lecture notes",
                "file_url": "https://example.com/physics-notes.pdf",
            },
        )
        self.assertEqual(link_response.status_code, 302)

        with patch(
            "app.routes.video.get_playlist_videos",
            return_value=[
                {"title": "Introduction", "video_id": "abcdefghijk", "duration_seconds": 60}
            ],
        ):
            playlist_response = self.client.post(
                "/video/upload",
                data={
                    "title": "Calculus Lectures",
                    "subject": "Mathematics",
                    "description": "Course playlist",
                    "playlist_url": "https://www.youtube.com/playlist?list=PLtest",
                },
            )
        self.assertEqual(playlist_response.status_code, 302)

        with self.app.app_context():
            from app.models.material import Material
            from app.models.paper import Paper
            from app.models.video import Playlist

            paper = Paper.query.one()
            materials = Material.query.order_by(Material.id).all()
            playlist = Playlist.query.one()
            self.assertEqual(paper.uploaded_by, guest.id)
            self.assertEqual(paper.status, "pending")
            self.assertEqual(len(materials), 2)
            self.assertTrue(all(material.uploaded_by == guest.id for material in materials))
            self.assertTrue(all(material.status == "pending" for material in materials))
            self.assertEqual(playlist.uploaded_by, guest.id)
            self.assertEqual(playlist.status, "pending")
            paper_id = paper.id
            material_ids = [material.id for material in materials]
            playlist_id = playlist.id

        public_client = self.app.test_client()
        self.assertNotIn(b"Calculus (2024)", public_client.get("/papers/").data)
        self.assertNotIn(b"Physics Notes", public_client.get("/materials/").data)
        self.assertNotIn(b"External Notes", public_client.get("/materials/").data)
        self.assertNotIn(b"Calculus Lectures", public_client.get("/video/").data)

        admin = self.app.test_client()
        response = admin.post(
            "/admin-login",
            data={
                "username": TestConfig.ADMIN_USERNAME,
                "password": TestConfig.ADMIN_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(admin.post(f"/admin/papers/{paper_id}/approve").status_code, 302)
        for material_id in material_ids:
            self.assertEqual(admin.post(f"/admin/materials/{material_id}/approve").status_code, 302)
        self.assertEqual(admin.post(f"/admin/playlists/{playlist_id}/approve").status_code, 302)

        with patch.dict(
            self.app.jinja_env.filters,
            {
                "file_url": lambda key: (
                    key if key.startswith("https://") else f"https://files.example/{key}"
                )
            },
        ):
            self.assertIn(b"Calculus (2024)", public_client.get("/papers/").data)
            self.assertIn(b"Physics Notes", public_client.get("/materials/").data)
            self.assertIn(b"External Notes", public_client.get("/materials/").data)
            self.assertIn(b"Calculus Lectures", public_client.get("/video/").data)


if __name__ == "__main__":
    unittest.main()
