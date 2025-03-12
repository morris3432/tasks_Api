from invoke import task
from src.config.config import Config
from rich.console import  Console
# Configuración
config = Config()
console = Console()
# Puerto
port = config.port

@task
def dev(c): 
  """Ejecutar en modo desarrollo"""
  console.print(f"[green]ok[/green] modo desarrollo en: [cyan]http://localhost:{port} [/cyan]")
  c.run(f"uvicorn src.index:app --reload --port {port}")

@task
def run(c):
  """Ejecutar en modo producción"""
  console.print(f"[green]ok[/green] producción en: [cyan]http://localhost:{port} [/cyan]")
  c.run(f"uvicorn src.index:app --port {port}")

@task
def lint(c):
  """Ejecutar linters"""
  c.run("flake8 src")

@task
def format(c):
  """Formatear código con autopep8"""
  c.run("autopep8 --in-place --recursive --indent-size 2 src")
  console.print("[cyan]OK[/cyan] codigo formatiado")

@task  
def requirements(c):
  """Actualizar requerimientos"""
  c.run('pip freeze > requirements.txt')
  console.print("[blue]ok[/blue] requeriment actualizado")
  
@task
def install(c):
  """Instalar requerimientos"""
  c.run('pip install -r requirements.txt')
  console.print("[cyan]OK[/cyan] requerimientos instalados")