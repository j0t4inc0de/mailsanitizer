import json
import logging
import time
import os
import signal
import sys
from django.core.management.base import BaseCommand
from django.utils import timezone
import redis
from core.models import ValidationTask, EmailResult
from core.validators import validate_email

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Procesa la cola de validación de correos en segundo plano usando Redis'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_exit = False

    def handle_signal(self, signum, frame):
        self.stdout.write(self.style.WARNING('\nSeñal de apagado recibida. Terminando limpiamente...'))
        self.should_exit = True

    def handle(self, *args, **options):
        # Graceful shutdown signals
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
        self.stdout.write(self.style.SUCCESS(f'Conectando a Redis en {redis_url}...'))
        
        try:
            r = redis.from_url(redis_url)
            r.ping()
        except redis.ConnectionError:
            self.stdout.write(self.style.ERROR('No se pudo conectar a Redis. Abortando.'))
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS('Worker asíncrono iniciado. Esperando tareas en la cola "cleanmail:tasks"...'))

        while not self.should_exit:
            try:
                # BLPOP waits up to 2 seconds for an item
                task_data = r.blpop('cleanmail:tasks', timeout=2)
                
                if task_data:
                    task_id = task_data[1].decode('utf-8')
                    self.process_task(task_id)
            
            except Exception as e:
                logger.error(f'Error en el ciclo del worker: {str(e)}')
                time.sleep(2)  # Pause briefly on error

        self.stdout.write(self.style.SUCCESS('Worker terminado limpiamente.'))

    def process_task(self, task_id):
        self.stdout.write(self.style.WARNING(f'Procesando tarea: {task_id}'))
        
        try:
            task = ValidationTask.objects.get(id=task_id)
        except ValidationTask.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Tarea {task_id} no encontrada en DB.'))
            return

        if task.estado != 'pendiente':
            self.stdout.write(self.style.WARNING(f'Tarea {task_id} ya no está pendiente (estado={task.estado}). Omitiendo.'))
            return

        task.estado = 'procesando'
        task.save(update_fields=['estado'])

        batch_size = 100
        offset = 0

        while not self.should_exit:
            # Obtener el siguiente batch de EmailResults pendientes
            batch = list(EmailResult.objects.filter(tarea=task, estado='pendiente')[0:batch_size])
            
            if not batch:
                break  # Terminamos la tarea
            
            validos = 0
            invalidos = 0
            desechables = 0
            
            for email_obj in batch:
                if self.should_exit:
                    break
                    
                result = validate_email(email_obj.correo)
                
                email_obj.estado = result['estado']
                email_obj.motivo = result['motivo']
                
                if result['estado'] == 'valido':
                    validos += 1
                elif result['estado'] == 'invalido':
                    invalidos += 1
                elif result['estado'] == 'desechable':
                    desechables += 1
            
            # Guardar resultados en bloque
            EmailResult.objects.bulk_update(batch, ['estado', 'motivo'])
            
            # Actualizar contadores en la tarea
            task.procesados += len(batch)
            task.validos += validos
            task.invalidos += invalidos
            task.desechables += desechables
            task.save(update_fields=['procesados', 'validos', 'invalidos', 'desechables'])
            
            self.stdout.write(f'  - Procesados {task.procesados}/{task.total_correos}...')
            
            # Pausa de cortesía para no ahogar DNS o CPU
            time.sleep(0.3)
            offset += batch_size

        if self.should_exit:
            self.stdout.write(self.style.WARNING(f'Procesamiento interrumpido en la tarea {task_id}.'))
            # Dejamos en estado 'procesando' o lo volvemos a encolar? Por ahora lo dejamos procesando.
            return

        # Marcar tarea completada
        task.estado = 'completado'
        task.completed_at = timezone.now()
        task.save(update_fields=['estado', 'completed_at'])
        
        self.stdout.write(self.style.SUCCESS(f'Tarea {task_id} completada con éxito.'))
