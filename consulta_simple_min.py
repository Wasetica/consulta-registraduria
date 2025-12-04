#!/usr/bin/env python3
"""Versión minimalista para pruebas"""
import time
import random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def realizar_consulta(documento: str, **kwargs):
    """Función mock para pruebas"""
    tiempo = random.uniform(1.0, 3.0)
    time.sleep(tiempo)
    
    return {
        'success': random.random() > 0.2,
        'documento': documento,
        'nombre': f'CIUDADANO {documento}',
        'estado_vigencia': 'VIGENTE',
        'tiempo_respuesta': tiempo,
        'pdf_path': f'pdfs/{documento}.pdf'
    }

def consulta_individual(cedula: str, fecha: str = None):
    """Wrapper para compatibilidad"""
    return realizar_consulta(cedula)

if __name__ == "__main__":
    print("✅ Módulo cargado")
