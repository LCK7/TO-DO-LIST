@echo off
REM Instalar dependencias si no están instaladas
pip install pytest pytest-cov

echo.
echo === Ejecutando tests con SQLAlchemy y generando reporte de cobertura ===
echo.

REM Ejecutar tests con coverage
pytest --cov=src tests/ -v

REM Generar reporte HTML
pytest --cov=src --cov-report=html tests/

echo.
echo El reporte de cobertura está disponible en ./htmlcov/index.html
echo Para verlo, abre este archivo en tu navegador.
echo.
