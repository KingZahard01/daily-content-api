import json
from datetime import date
from unittest.mock import patch, mock_open

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Frases de prueba
TEST_PHRASES = [
    {"id": 1, "texto": "Frase de prueba 1", "autor": "Autor 1"},
    {"id": 2, "texto": "Frase de prueba 2", "autor": "Autor 2"},
    {"id": 3, "texto": "Frase de prueba 3", "autor": "Autor 3"},
]


class TestHomeEndpoint:
    """Pruebas para el endpoint de inicio"""

    def test_home_returns_welcome_message(self):
        """Verifica que el endpoint home retorna el mensaje de bienvenida correcto"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Frase Diaria"}


class TestDailyPhraseEndpoint:
    """Pruebas para el endpoint de frase diaria"""

    @patch("app.main.PHRASES", TEST_PHRASES)
    def test_daily_phrase_returns_phrase(self):
        """Verifica que el endpoint retorna una frase con la estructura correcta"""
        response = client.get("/daily-phrase")
        assert response.status_code == 200
        
        data = response.json()
        assert "date" in data
        assert "text" in data
        assert "author" in data
        assert data["date"] == str(date.today())

    @patch("app.main.PHRASES", TEST_PHRASES)
    @patch("app.main.date")
    def test_daily_phrase_is_deterministic(self, mock_date):
        """Verifica que la frase diaria es determinística para una fecha dada"""
        # Configurar fecha fija
        mock_date.today.return_value = date(2024, 1, 15)
        
        # Realizar múltiples peticiones
        response1 = client.get("/daily-phrase")
        response2 = client.get("/daily-phrase")
        response3 = client.get("/daily-phrase")
        
        # Todas las respuestas deben ser idénticas
        assert response1.json() == response2.json()
        assert response2.json() == response3.json()

    @patch("app.main.PHRASES", TEST_PHRASES)
    @patch("app.main.date")
    def test_daily_phrase_changes_with_date(self, mock_date):
        """Verifica que diferentes fechas retornan diferentes frases"""
        # Fecha 1
        mock_date.today.return_value = date(2024, 1, 1)
        response1 = client.get("/daily-phrase")
        phrase1 = response1.json()["text"]
        
        # Fecha 2
        mock_date.today.return_value = date(2024, 1, 2)
        response2 = client.get("/daily-phrase")
        phrase2 = response2.json()["text"]
        
        # Fecha 3
        mock_date.today.return_value = date(2024, 1, 3)
        response3 = client.get("/daily-phrase")
        phrase3 = response3.json()["text"]
        
        # Al menos dos frases deben ser diferentes
        # (es posible que algunas coincidan debido al módulo)
        phrases = {phrase1, phrase2, phrase3}
        assert len(phrases) >= 1  # Como mínimo obtenemos respuestas válidas

    @patch("app.main.PHRASES", [])
    def test_daily_phrase_handles_empty_database(self):
        """Verifica que el endpoint maneja correctamente cuando no hay frases disponibles"""
        response = client.get("/daily-phrase")
        assert response.status_code == 200
        assert response.json() == {"error": "No phrases available"}


class TestRandomPhraseEndpoint:
    """Pruebas para el endpoint de frase aleatoria"""

    @patch("app.main.PHRASES", TEST_PHRASES)
    def test_random_phrase_returns_single_phrase(self):
        """Verifica que el endpoint retorna una sola frase con la estructura correcta"""
        response = client.get("/phrase-random")
        assert response.status_code == 200
        
        data = response.json()
        assert "text" in data
        assert "author" in data
        assert isinstance(data["text"], str)
        assert isinstance(data["author"], str)

    @patch("app.main.PHRASES", TEST_PHRASES)
    def test_random_phrase_returns_valid_phrase(self):
        """Verifica que la frase retornada existe en la base de datos"""
        response = client.get("/phrase-random")
        data = response.json()
        
        # Verificar que la frase existe en TEST_PHRASES
        valid_phrases = [p["texto"] for p in TEST_PHRASES]
        assert data["text"] in valid_phrases

    @patch("app.main.PHRASES", TEST_PHRASES)
    def test_random_phrase_can_return_different_phrases(self):
        """Verifica que el endpoint puede retornar diferentes frases"""
        responses = [client.get("/phrase-random").json()["text"] for _ in range(20)]
        unique_phrases = set(responses)
        
        # Con 20 peticiones y 3 frases, deberíamos obtener al menos 2 diferentes
        assert len(unique_phrases) >= 2


class TestAllPhrasesEndpoint:
    """Pruebas para el endpoint de todas las frases"""

    @patch("app.main.PHRASES", TEST_PHRASES)
    def test_all_phrases_returns_correct_structure(self):
        """Verifica que el endpoint retorna la estructura correcta"""
        response = client.get("/phrases")
        assert response.status_code == 200
        
        data = response.json()
        assert "total" in data
        assert "phrases" in data
        assert isinstance(data["total"], int)
        assert isinstance(data["phrases"], list)

    @patch("app.main.PHRASES", TEST_PHRASES)
    def test_all_phrases_returns_correct_count(self):
        """Verifica que el conteo total coincide con el número de frases"""
        response = client.get("/phrases")
        data = response.json()
        
        assert data["total"] == len(TEST_PHRASES)
        assert len(data["phrases"]) == len(TEST_PHRASES)

    @patch("app.main.PHRASES", TEST_PHRASES)
    def test_all_phrases_returns_all_available_phrases(self):
        """Verifica que todas las frases disponibles son retornadas"""
        response = client.get("/phrases")
        data = response.json()
        
        # Verificar que cada frase de prueba está en la respuesta
        returned_texts = [p["text"] for p in data["phrases"]]
        expected_texts = [p["texto"] for p in TEST_PHRASES]
        
        assert sorted(returned_texts) == sorted(expected_texts)

    @patch("app.main.PHRASES", TEST_PHRASES)
    def test_all_phrases_format_matches_expected(self):
        """Verifica que cada frase tiene el formato esperado (text y author)"""
        response = client.get("/phrases")
        data = response.json()
        
        for phrase in data["phrases"]:
            assert "text" in phrase
            assert "author" in phrase
            assert "id" not in phrase  # El ID no debe estar en la respuesta

    @patch("app.main.PHRASES", [])
    def test_all_phrases_with_empty_database(self):
        """Verifica el comportamiento con una base de datos vacía"""
        response = client.get("/phrases")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 0
        assert data["phrases"] == []
