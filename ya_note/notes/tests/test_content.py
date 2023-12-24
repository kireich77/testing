from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )

    def test_notes_of_different_users(self):
        users_notes = (
            (self.author, True),
            (self.reader, False),
        )
        for user, note_in_list in users_notes:
            self.client.force_login(user)
            url = reverse('notes:list')
            response = self.client.get(url)
            self.assertIn('object_list', response.context)
            note_in_object_list = self.note in response.context['object_list']
            with self.subTest(user=user.username, note_in_list=note_in_list):
                self.assertEqual(note_in_object_list, note_in_list)

    def test_pages_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for page, args in urls:
            with self.subTest(page=page):
                url = reverse(page, args=args)
                self.client.force_login(self.author)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                form = response.context['form']
                self.assertIsInstance(form, NoteForm)
