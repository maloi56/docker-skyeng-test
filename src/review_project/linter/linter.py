import logging
import subprocess
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)

def check_code(file_path):
    logger.info(f'check_code Started: file_path: {file_path}')
    media_root = Path(settings.MEDIA_ROOT)
    logger.info(f'check_code Started: media_root: {media_root}')
    full_path = media_root / Path(file_path)
    logger.info(f'check_code Started: full_path: {full_path}')
    try:
        result = subprocess.run(['flake8', str(full_path.absolute())], capture_output=True, text=True)
        logger.info(f'check_code Started: result: {result}')

        if result.returncode == 0:
            return "Код соответствует стандартам PEP 8."
        else:
            return result.stdout
    except Exception as e:
        print(e)
        return f"Произошла ошибка: {str(e)}"
