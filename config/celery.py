# celery.py

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# РЈСЃС‚Р°РЅРѕРІРєР° РїРµСЂРµРјРµРЅРЅРѕР№ РѕРєСЂСѓР¶РµРЅРёСЏ РґР»СЏ РЅР°СЃС‚СЂРѕРµРє РїСЂРѕРµРєС‚Р°
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# РЎРѕР·РґР°РЅРёРµ СЌРєР·РµРјРїР»СЏСЂР° РѕР±СЉРµРєС‚Р° Celery
app = Celery("config")

# Р—Р°РіСЂСѓР·РєР° РЅР°СЃС‚СЂРѕРµРє РёР· С„Р°Р№Р»Р° Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# РђРІС‚РѕРјР°С‚РёС‡РµСЃРєРѕРµ РѕР±РЅР°СЂСѓР¶РµРЅРёРµ Рё СЂРµРіРёСЃС‚СЂР°С†РёСЏ Р·Р°РґР°С‡ РёР· С„Р°Р№Р»РѕРІ tasks.py РІ РїСЂРёР»РѕР¶РµРЅРёСЏС… Django
app.autodiscover_tasks()
