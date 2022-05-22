#!/usr/bin/python3
"""Tests for index API"""
import unittest
from api.v1.app import app


class TestIndexAPI(unittest.TestCase):
    """test for correct function API"""
    @classmethod
    def setUpClass(self):
        """Create test client for all calls to api/app"""
        app.testing = True
        self.client = app.test_client()

    def test_get_status(self):
        """Test get_status() function returning 200 status from '/status'"""
        route = self.client.get('/api/v1/status')
        self.assertEqual(route.status_code, 200)
        self.assertTrue('Content-Type' in route.headers)
        self.assertEqual(route.headers.get('Content-Type'), 'application/json')

    def test_404(self):
        """Test the result of querying a route that does not exist"""
        route = self.client.get('/api/v1/nop')
        self.assertEqual(route.status_code, 404)
        self.assertTrue('Content-Type' in route.headers)
        self.assertEqual(route.headers.get('Content-Type'), 'application/json')
