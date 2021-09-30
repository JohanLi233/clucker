from django.test import TestCase
from .models import User
from django.core.exceptions import ValidationError

# def factorial(integer):
#     if(integer < 0):
#         raise ValueError()
#     if(integer == 0):
#         return 1
#     if(integer == 1):
#         return integer
#     return integer * factorial(integer - 1)
#
# class UnitTestCase(TestCase):
#     def test_factorial_of_1(self):
#         self.assertEqual(factorial(1), 1)
#
#     def test_factorial_of_2(self):
#         self.assertEqual(factorial(2), 2)
#
#     def test_factorial_of_3(self):
#         self.assertEqual(factorial(3), 6)
#
#     def test_factorial_of_4(self):
#         self.assertEqual(factorial(4), 24)
#
#     def test_factorial_of_5(self):
#         self.assertEqual(factorial(5), 120)
#
#     def test_factorial_of_minus_1(self):
#         with self.assertRaises(ValueError):
#             factorial(-1)

class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            '@Jaha',
            first_name='Zhonghan',
            last_name='Li',
            email='947563221@qq.com',
            password='Johan@2003',
            bio='super ADMIN!'
        )

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_no_blank_username(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_is_unique(self):
        second_user = self.create_second_user()
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_user_name_must_starts_with_at_symbol(self):
        self.user.username = 'Jaha'
        self._assert_user_is_invalid()

    def test_user_name_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@Jah!a'
        self._assert_user_is_invalid()

    def test_user_name_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@Ja'
        self._assert_user_is_invalid()

    def test_user_name_may_contain_number_after_at(self):
        self.user.username = '@Ja1'
        self._assert_user_is_valid()

    def test_user_name_cannot_have_2_or_more_at(self):
        self.user.username = '@Jaha@'
        self._assert_user_is_invalid()

    def test_first_name_cannot_be_empty(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_last_name_cannot_be_empty(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_first_name_cannot_be_longer_than_50(self):
        self.user.first_name = 'x' + 'x' * 50
        self._assert_user_is_invalid()

    def test_last_name_cannot_be_longer_than_50(self):
        self.user.last_name = 'x' + 'x' * 50
        self._assert_user_is_invalid()

    def test_first_name_has_not_to_be_unique(self):
        second_user = self.create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_last_name_has_not_to_be_unique(self):
        second_user = self.create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_email_not_blak(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_emial_must_be_unique(self):
        second_user = self.create_second_user()
        self.user.email = second_user.email

    def test_email_must_contain_username(self):
        self.user.email = '@examplt.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = '1234.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = '1234@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = '1234@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = '1234@@example.org'
        self._assert_user_is_invalid()

    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_bio_need_not_be_unique(self):
        second_user = self.create_second_user()
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    def test_bio_may_contain_520_characters(self):
        self.user.bio = 'x' + 'x' * 519
        self._assert_user_is_valid()

    def test_bio_may_not_exceed_520_characters(self):
        self.user.bio = 'x' + 'x' * 520
        self._assert_user_is_invalid()



    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except(ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
             self.user.full_clean()

    def create_second_user(self):
        user = User.objects.create_user(
            '@Shally',
            first_name='Yuqiong',
            last_name='Fang',
            email='2034220298@qq.com',
            password='Fyq@0918',
            bio='super ADMIN!'
        )
        return user
