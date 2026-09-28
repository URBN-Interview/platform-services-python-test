import unittest

from rewardsservice.helpers.validation import ValidationError, parse_order_body


class TestParseOrderBody(unittest.TestCase):
    def test_valid_body(self):
        body = '{"email_address": " Customer01@Gmail.com ", "order_total": 100.80}'
        self.assertEqual(parse_order_body(body), ("customer01@gmail.com", 100.80))

    def test_invalid_json(self):
        with self.assertRaises(ValidationError):
            parse_order_body("not json")

    def test_missing_email(self):
        with self.assertRaises(ValidationError):
            parse_order_body('{"order_total": 100}')

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            parse_order_body('{"email_address": "not-an-email", "order_total": 100}')

    def test_order_total_must_be_positive(self):
        with self.assertRaises(ValidationError):
            parse_order_body('{"email_address": "a@b.com", "order_total": 0}')

    def test_order_total_must_be_a_number(self):
        with self.assertRaises(ValidationError):
            parse_order_body('{"email_address": "a@b.com", "order_total": "100"}')


if __name__ == "__main__":
    unittest.main()
