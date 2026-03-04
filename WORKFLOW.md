# Flujo de Desarrollo - Bongles.food

## 📋 Estructura Completada

### Proyecto Django
- ✅ Configuración base (settings.py, urls.py, wsgi.py, asgi.py)
- ✅ 5 Aplicaciones Django:
  - **Users**: Gestión de usuarios y autenticación
  - **Businesses**: Negocios/cafeterías con reseñas
  - **Products**: Menú y productos
  - **Orders**: Órdenes/pedidos con estados
  - **Payments**: Procesamiento de pagos

### Modelos de Base de Datos
- CustomUser con roles (customer, business, admin)
- Business con información completa
- BusinessReview para calificaciones
- Product con categorías
- Order con múltiples items
- Payment con diferentes métodos

### API REST Completa
- Endpoints para usuarios (registro, login)
- CRUD para businesses con filtros
- Gestión de productos
- Creación y seguimiento de órdenes
- Procesamiento de pagos

### Tecnologías Incluidas
- Django REST Framework
- Django CORS Headers
- Simple JWT (autenticación)
- DRF Spectacular (documentación API)
- Pillow (imágenes)
- Django Filter

## 🔄 Flujo Local → GitHub → Droplet

### 1️⃣ Desarrollo Local (tu PC - Windows)
```bash
cd C:\Users\Pruzhk4\Desktop\Bongles

# Crear cambios locales
# ... editar archivos ...

# Hacer commit
git add .
git commit -m "Descripción del cambio"

# Push a GitHub
git push origin main
```

### 2️⃣ En GitHub
- Repositorio: https://github.com/Przk4/Bongles
- Rama: main
- Todos los cambios se guardan aquí

### 3️⃣ En el Droplet (146.190.172.2)
```bash
# Conectar al droplet
ssh -i ~/.ssh/bongles_do root@146.190.172.2

cd /var/www/bongles.food

# Obtener últimos cambios
git pull origin main

# Si es primera vez:
# git clone https://github.com/Przk4/Bongles.git .

# Activar entorno
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Reiniciar servicios
systemctl restart gunicorn-bongles
systemctl restart nginx

# Ver logs
tail -f /var/log/bongles/error.log
```

## 🚀 Próximos Pasos

1. **Frontend** (React/Vue)
   - Páginas de usuario
   - Dashboard de negocios
   - Carrito de compras
   - Tracking de órdenes

2. **Notificaciones Reales**
   - WebSockets con Channels
   - Notificaciones de órdenes
   - Chat en tiempo real

3. **Pagos Reales**
   - Integrar Stripe/PayPal
   - Webhooks de pagos
   - Confirmaciones automáticas

4. **Tests**
   - Tests unitarios
   - Tests de integración
   - Coverage report

5. **Deployment**
   - Configurar SSL/HTTPS
   - Configurar dominio bongles.food
   - Backup automático
   - Monitoreo

## 📊 Estructura Actual

```
Bongles/
├── apps/
│   ├── users/
│   ├── businesses/
│   ├── products/
│   ├── orders/
│   └── payments/
├── bongles_config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/
├── media/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔑 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Tests
python manage.py test

# Shell interactivo
python manage.py shell

# Ver URL patterns
python manage.py show_urls
```

## API Docs

Una vez en producción:
- Swagger UI: http://bongles.food/api/docs/
- ReDoc: http://bongles.food/api/redoc/
- Schema JSON: http://bongles.food/api/schema/

## 📝 Variables de Entorno (.env)

```
DEBUG=True
SECRET_KEY=tu-super-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bongles_db
DB_USER=bongles_user
DB_PASSWORD=tu-contraseña-segura
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,bongles.food
```

---

**Estado**: Proyecto base completado ✅
**Repo**: https://github.com/Przk4/Bongles
**Hosting**: DigitalOcean (146.190.172.2)
