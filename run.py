#!/usr/bin/env python
"""
Production-ready application runner
"""
import os
# Development ortamında localhost için http kullanımına izin ver
if os.getenv('FLASK_ENV', 'development') == 'development':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from app import app, db

if __name__ == '__main__':
    # Veritabanı tablolarını oluştur
    with app.app_context():
        db.create_all()
        print("✅ Veritabanı hazır")
    
    # Port ve host ayarları
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"🚀 Uygulama başlatılıyor: http://{host}:{port}")
    print(f"📝 Environment: {os.getenv('FLASK_ENV', 'development')}")
    
    app.run(debug=debug, host=host, port=port)

