# 📊 API Gestor de Finanzas Personales

API REST desarrollada con **Django** y **Django REST Framework** para la gestión de finanzas personales. Permite administrar cuentas, categorías y transacciones, manteniendo reglas de dominio claras y consistencia en los balances.

Este proyecto fue creado con fines de **aprendizaje**, **práctica profesional** y **portafolio**, siguiendo buenas prácticas de backend, validaciones a nivel de modelo/serializador, testing y control de versiones.

---

## 🚀 Funcionalidades principales

* 👤 **Autenticación por usuario** (cada recurso pertenece a un usuario)
* 🏦 **Gestión de cuentas**

  * Límite máximo de 10 cuentas por usuario
  * Balance calculado automáticamente
  * `opening_balance` inmutable luego de la creación
* 🗂 **Categorías**

  * Tipos: `INCOME` / `EXPENSE`
  * Determinan el comportamiento de las transacciones
* 💸 **Transacciones**

  * Actualizan el balance de la cuenta asociada
  * Validaciones de pertenencia (cuenta y categoría del mismo usuario)
  * Lógica centralizada en `perform_create`, `perform_update` y `perform_destroy`
* 📈 **Reportes**

  * Balance mensual
  * Ingresos y gastos agrupados por categoría
* 🧪 **Testing**

  * Tests unitarios y de integración
  * Casos de error y validaciones de dominio

---

## 🛠 Tecnologías utilizadas

* Python 3
* Django
* Django REST Framework
* SQLite (desarrollo)
* Pytest / Django Test Framework
* Git & GitHub

---

## 📂 Estructura del proyecto

```text
api-gestor-finanzas/
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests/
├── categories/
│   ├── models.py
│   ├── serializers.py
│   └── tests/
├── transactions/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests/
├── utils/
│   └── choices.py
├── config/
│   ├── settings.py
│   └── urls.py
└── manage.py
```

---

## 🧠 Reglas de dominio destacadas

* Un usuario **no puede crear más de 10 cuentas**
* Una transacción solo puede usar:

  * cuentas del usuario autenticado
  * categorías del usuario autenticado
* El balance de la cuenta:

  * **no se edita manualmente**
  * se recalcula automáticamente según las transacciones
* El `opening_balance`:

  * solo se define al crear la cuenta
  * no puede modificarse posteriormente

---

## 🔐 Seguridad y validaciones

* `CurrentUserDefault` para asegurar el usuario autenticado
* Querysets filtrados por usuario en serializers
* Validaciones personalizadas (`validate_account`, `validate_category`)
* Reglas críticas implementadas en modelos y vistas

---

## ▶️ Instalación y ejecución local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/Django-REST-Finanzas.git
cd Django-REST-Finanzas

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
```

---

## 🧪 Ejecutar tests

```bash
python manage.py test
```

---

## 📌 Estado del proyecto

✔ Funcional
✔ En desarrollo activo
✔ Enfocado en buenas prácticas backend

Próximos pasos posibles:

* Autenticación con JWT
* Paginación y filtros avanzados
* Deploy en entorno productivo

---

## 👨‍💻 Autor

**Geremías Arguello**
Python Backend Developer en formación
Enfocado en Django, Django REST Framework y diseño de APIs

---

## 📄 Licencia

Proyecto de uso educativo y demostrativo.
