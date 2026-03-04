# Bongles.food - Servicio de Órdenes de Comida

Plataforma en línea para que los clientes ordenen comida de cafeterías y negocios locales sin hacer fila.

## Características

- 📱 Interfaz móvil-first para ordenar comida
- 🏬 Sistema de negocios (cafeterías, restaurantes)
- 💰 Procesamiento de pagos integrado
- ⏱️ Órdenes con recogida sin fila
- 📊 Panel de administración para negocios
- 🔔 Notificaciones en tiempo real
- ⭐ Sistema de calificaciones y comentarios

## Tecnología

- **Backend:** Django 5.0.3 + Django REST Framework
- **Base de Datos:** PostgreSQL
- **Servidor:** Gunicorn + Nginx
- **Cache/Queue:** Redis + Celery
- **Frontend:** (Próximamente - React/Vue)
- **Hosting:** DigitalOcean

## Instalación Local

### Requisitos
- Python 3.12+
- PostgreSQL 12+
- Redis (opcional para desarrollo)
- Git

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/Przk4/Bongles.git
cd Bongles
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus datos
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

Accede a `http://localhost:8000/admin/` con tus credenciales.

## Estructura del Proyecto

```
Bongles/
├── bongles_config/          # Configuración principal de Django
│   ├── settings.py         # Configuración del proyecto
│   ├── urls.py            # URLs raíz
│   ├── wsgi.py            # WSGI para producción
│   └── asgi.py            # ASGI para WebSockets
├── apps/
│   ├── users/             # App de usuarios y autenticación
│   ├── businesses/        # App de negocios/cafeterías
│   ├── products/          # App de productos/menú
│   ├── orders/            # App de órdenes
│   └── payments/          # App de pagos
├── manage.py              # Manage.py de Django
├── requirements.txt       # Dependencias Python
├── .env.example           # Plantilla de variables
├── .gitignore            # Archivos a ignorar en Git
├── README.md             # Este archivo
└── static/               # Archivos estáticos (CSS, JS, etc)
```

## API Endpoints

- `GET /api/businesses/` - Listar negocios
- `GET /api/products/` - Listar productos
- `POST /api/orders/` - Crear orden
- `GET /api/orders/<id>/` - Obtener orden
- `POST /api/payments/` - Procesar pago

## Desarrollo

### Crear nueva app de Django
```bash
python manage.py startapp nombre_app apps/nombre_app
```

### Crear migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Ejecutar tests
```bash
python manage.py test
```

## Despliegue en Producción

Ver `DEPLOYMENT_GUIDE.md` para instrucciones detalladas de despliegue en DigitalOcean.

## Flujo de Trabajo Git

1. Crea una rama para tu feature: `git checkout -b feature/nombre-feature`
2. Haz commits con mensajes claros: `git commit -m "Agregar [feature]"`
3. Push a tu rama: `git push origin feature/nombre-feature`
4. Abre un Pull Request en GitHub

## Contribuidores

- Bongles Dev Team

## Licencia

Privado - Bongles.food

## Contacto

Para preguntas o sugerencias, contacta a: dev@bongles.food
