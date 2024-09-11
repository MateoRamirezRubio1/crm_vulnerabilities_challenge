# Instrucciones para ejecutar la aplicación con Docker Compose
## 1. Clonar el repositorio
Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/MateoRamirezRubio1/crm_vulnerabilities_challenge.git
cd crm_vulnerabilities
```

## 2. Construir la imagen y ejecutar los servicios
Para ejecutar la aplicación con Docker Compose, asegúrate de estar en la raíz del proyecto (donde está el archivo docker-compose.yml) y ejecuta el siguiente comando:

```bash
docker-compose up --build
```

Esto realizará las siguientes acciones:

Construir la imagen Docker definida en el Dockerfile.
Ejecutar los comandos necesarios de migración de la base de datos:
python manage.py makemigrations
python manage.py migrate
python manage.py migrate token_blacklist zero
Iniciar el servidor de desarrollo de Django en el puerto 8000.

## 3. Acceder a la aplicación
Una vez que el contenedor esté en funcionamiento, puedes acceder a la aplicación desde tu navegador en la siguiente URL:

```
http://localhost:8000
```

# Implementación de Rate Limiting
El proyecto implementa un rate limiter o limitador de tasa que restringe el número de peticiones que se pueden realizar a la API. Este rate limiter ha sido configurado para permitir un máximo de 15 peticiones por minuto, lo que previene que un solo cliente realice demasiadas solicitudes en un corto periodo, evitando una sobrecarga en la API.

Cuando se supera este límite, el cliente recibe una respuesta de error (429 Too Many Requests), indicando que deberá esperar antes de realizar más solicitudes. Este mecanismo protege tanto el servidor como el cliente al regular el flujo de datos y asegurar un acceso justo para todos los usuarios.

# Módulo de Vulnerabilidades

## Descripción

El módulo de `vulnerabilities` gestiona las vulnerabilidades del sistema, permitiendo la obtención, almacenamiento y resumen de las mismas. Además, se divide en varias capas de funcionalidad, como servicios, serializadores, observadores, clientes y especificaciones, siguiendo principios de arquitectura limpia y patrones de diseño que hacen que el sistema sea extensible y fácil de mantener.

## Estructura del Módulo

### 1. `clients/`
Contiene la clase `NVDClient`, que se encarga de interactuar con fuentes externas, como la **National Vulnerability Database (NVD)**, para recuperar información relacionada con las vulnerabilidades del sistema.

- **Patrón utilizado**: **Cliente Externo** (External Client), que abstrae la comunicación con un servicio externo (NVD).

### 2. `observers/`
Este directorio contiene la implementación del patrón de diseño **Observer**. En este caso, el `VulnerabilityObserver` observa los cambios en las vulnerabilidades y actúa en consecuencia, como crear alertas cuando se ingresa una nueva vulnerabilidad fixeada.

- **Patrón utilizado**: **Observer**, utilizado para suscribirse a cambios en el estado de vulnerabilidades.

### 3. `repositories/`
El repositorio almacena las vulnerabilidades y proporciona una interfaz abstracta para las operaciones de base de datos. Permite el acceso y manejo de datos de forma desacoplada de la lógica del negocio.

- **Patrón utilizado**: **Repositorio** (Repository), utilizado para encapsular el acceso a la base de datos.

### 4. `serializers/`
Este directorio contiene varios serializadores que convierten los objetos del modelo de vulnerabilidad en datos que pueden ser enviados a través de la API. Aquí se definen:
   - `FixedVulnerabilitySerializer`: Serializa vulnerabilidades que ya han sido solucionadas.
   - `NISTVulnerabilitySerializer`: Serializa vulnerabilidades según los estándares de la NIST.
   - `VulnerabilitySummarySerializer`: Proporciona un resumen de las vulnerabilidades.

- **Patrón utilizado**: **Adapter/Bridge**, para la transformación de objetos entre la capa de datos y la API.

### 5. `services/`
Define la lógica de negocio principal a través del `VulnerabilityService`, que gestiona todas las acciones relacionadas con las vulnerabilidades. Además, se utiliza el `ServiceFactory` para crear instancias de los servicios requeridos e inyección de dependencias.

- **Patrón utilizado**: 
   - **Servicio** (Service Layer) para encapsular la lógica del negocio relacionada con vulnerabilidades.

### 6. `specifications/`
Define las reglas de filtrado de vulnerabilidades no solucionadas a través del patrón **Specification**, lo que facilita agregar nuevas reglas de negocio sin modificar el código existente.

- **Patrón utilizado**: **Specification**, utilizado para encapsular reglas de negocio reutilizables como en el caso saber si una vulnerabilidad ya ha sido fixeada.

### 7. `views/`
Contiene las vistas basadas en clases que exponen la API para la gestión de vulnerabilidades:
   - **`VulnerabilityListView`**: Devuelve la lista completa de vulnerabilidades.
   - **`UnfixedVulnerabilitiesView`**: Muestra vulnerabilidades que no han sido solucionadas.
   - **`VulnerabilityFixedView`**: Muestra vulnerabilidades que ya han sido solucionadas.
   - **`VulnerabilitySummaryView`**: Proporciona un resumen de las vulnerabilidades por tipo.

## Endpoints

El módulo proporciona los siguientes endpoints para interactuar con las vulnerabilidades:

- **`GET /api/vulnerabilities/`**: Obtiene la lista completa de vulnerabilidades.
- **`GET /api/vulnerabilities/unfixed/`**: Obtiene la lista de vulnerabilidades que no han sido solucionadas.
- **`GET /api/vulnerabilities/fixed/`**: Obtiene la lista de vulnerabilidades solucionadas.
- **`GET /api/vulnerabilities/summary/`**: Obtiene un resumen de las vulnerabilidades (solucionadas y no solucionadas).

## Uso de Cache en el Cliente NIST

El cliente de la API de NVD (National Vulnerability Database) ha sido diseñado para optimizar las solicitudes utilizando **caché en memoria**. Cada vez que se solicita la lista de vulnerabilidades, el cliente primero verifica si los datos previamente obtenidos siguen siendo válidos, basándose en un tiempo de expiración definido (`CACHE_TIMEOUT` de 3600 segundos o 1 hora).

### Detalles de la Implementación:
- **Almacena el resultado** de la consulta a la API en una variable privada (`_vulnerabilities_cache`) y registra el tiempo de la última actualización.
- Antes de realizar una nueva solicitud, verifica si los datos en cache aún son válidos mediante el método `_is_cache_valid()`, comparando el tiempo actual con el de la última actualización.
- Si el cache ha expirado o no existe, realiza una nueva solicitud a la API y actualiza el cache.
- Si el cache es válido, devuelve los datos almacenados, mejorando así la eficiencia y reduciendo la cantidad de llamadas a la API.

Este mecanismo de cache permite reducir la latencia de las consultas y evitar el exceso de solicitudes a la API de NIST, especialmente cuando se manejan grandes volúmenes de datos.

Si los datos en cache siguen siendo válidos, se devolverán sin necesidad de realizar una nueva consulta al servidor.


# Módulo de Alertas

## Descripción

El módulo de `alerts` está diseñado para gestionar las alertas generadas a partir de vulnerabilidades u otros eventos relevantes. Implementa un sistema de notificaciones que utiliza múltiples canales de comunicación, como correos electrónicos, SMS, notificaciones push, y Slack. Este módulo sigue patrones de diseño, incluyendo el patrón **Observer**, **Factory**, y **Singleton**, para gestionar eficientemente la creación, distribución y observación de alertas.

## Estructura del Módulo

### 1. `observers/`
Este directorio contiene el **Subject** del patrón **Observer**: `AlertSubject`. Aquí se define el comportamiento que permite suscribir a diferentes observadores para reaccionar ante cambios, como la creación de una nueva alerta.

- **Patrón utilizado**: **Observer**, con `AlertSubject` gestionando la suscripción de observadores y distribuyendo notificaciones de nuevas alertas.

### 2. `repositories/`
Contiene el repositorio de alertas (`AlertsRepository`), que maneja el acceso a los datos relacionados con las alertas y sus detalles.

- **Patrón utilizado**: **Repository**, para encapsular las operaciones de acceso a la base de datos y desacoplar la lógica de negocio de la lógica de persistencia.

### 3. `serializers/`
Incluye el serializador `ListAlertSerializer`, el cual convierte las alertas en un formato que puede ser enviado a través de la API.

- **Patrón utilizado**: **Adapter**, ya que transforma las entidades del sistema en datos listos para ser consumidos por la API.

### 4. `services/`
#### `alert_factory_services/`
Esta subcarpeta contiene los servicios de la **Fábrica de Alertas**. Se utiliza para crear y despachar alertas a través de múltiples canales.

- `AlertFactory`: Es responsable de crear diferentes tipos de alertas.
- `AlertDispatcher`: Se encarga de despachar las alertas generadas a los canales correspondientes.
- `EmailAlertService`, `PushAlertService`, `SlackAlertService`, `SMSAlertService`: Estos servicios representan las alertas enviadas a través de diferentes medios de comunicación.

- **Patrón utilizado**: 
  - **Factory** para la creación de diferentes tipos de alertas según la severidad de la vulnerabilidad (Al momento de ingresar una nueva vulnerabilidad por medio del POST de la app vulnerabilities, dependiendo de la severidad de la vulnerabilidad ingresada se envía un tipo de alerta u otra).

#### `api_alert_services/`
En esta subcarpeta se define `AlertService`, que gestiona la lógica de negocio de las alertas desde el punto de vista de la API.

### 5. `views/`
Contiene las vistas basadas en clases que exponen la API para la gestión de alertas:
   - **`AlertListView`**: Devuelve la lista completa de alertas registradas en el sistema.

- **Patrón utilizado**: **View Layer** de Django, utilizando vistas basadas en clases.

## Endpoints

El módulo expone el siguiente endpoint para interactuar con las alertas:

- **`GET /api/alerts/`**: Obtiene la lista completa de alertas.


# Módulo de Autenticación

## Descripción

El módulo de `authentication` proporciona funcionalidades para la autenticación de usuarios utilizando **JWT (JSON Web Tokens)**. Este módulo permite a los usuarios registrarse, iniciar sesión, y manejar la autorización mediante diferentes roles (admin, advanced, basic). Los permisos son gestionados a través de clases personalizadas de permisos que definen qué tipo de usuario puede acceder a ciertas vistas.

## Estructura del Módulo

### 4. `models.py`
Contiene el modelo de usuario extendido, que incluye campos adicionales como `role` para manejar roles personalizados (`admin`, `advanced`, `basic`).

- **Roles de usuario**:
  - `admin`: Administrador con acceso completo a todas las funcionalidades.
  - `advanced`: Usuario avanzado con permisos adicionales.
  - `basic`: Usuario básico con acceso limitado.

### 5. `permissions.py`
Define permisos personalizados para los diferentes roles. Cada clase de permiso (`IsAdmin`, `IsAdvancedUser`, `IsBasicUser`) comprueba el rol del usuario que realiza la solicitud.

- **Permisos personalizados**:
  - `IsAdmin`: Solo usuarios con rol de `admin`.
  - `IsAdvancedUser`: Solo usuarios con rol de `advanced`.
  - `IsBasicUser`: Solo usuarios con rol de `basic`.

### 6. `repositories.py`
Encapsula la lógica de acceso a la base de datos relacionada con la autenticación de usuarios. Gestiona las consultas a la base de datos para la creación de usuarios.

### 7. `serializers.py`
Define los serializadores que convierten los datos de los usuarios en JSON y viceversa. También se utiliza para validar los datos de registro e inicio de sesión.

- `RegisterSerializer`: Gestiona el registro de nuevos usuarios.
- `CustomTokenObtainPairSerializer`: Personaliza el token JWT, incluyendo información adicional como el rol del usuario en la respuesta.

### 8. `services.py`
Incluye la lógica de negocio para el registro de usuarios.

### 10. `urls.py`
Define las rutas para las vistas relacionadas con la autenticación. Las rutas disponibles son:

- `/login/`: Iniciar sesión y obtener el token JWT.
- `/register/`: Registrar un nuevo usuario.
- `/logout/`: Hacer logout y añadir el refresh token a la lista negra.
- `/refresh/`: Obtener un nuevo access token mediante el refresh token.

### 11. `views.py`
Define las vistas que manejan las solicitudes HTTP relacionadas con la autenticación:

- `CustomTokenObtainPairView`: Vista para obtener los tokens JWT (access y refresh) al iniciar sesión.
- `RegisterView`: Vista para registrar nuevos usuarios.
- `LogoutAndBlacklistRefreshTokenView`: Vista para hacer logout y añadir el token de refresh a la lista negra.

## Endpoints

El módulo expone los siguientes endpoints para la autenticación y manejo de roles:

- **`POST /api/authentication/login/`**: Inicia sesión y devuelve el `access` y `refresh` tokens.
- **`POST /api/authentication/register/`**: Registra un nuevo usuario.
- **`POST /api/authentication/logout/`**: Añade el `refresh` token a la lista negra y cierra sesión.
- **`POST /api/authentication/refresh/`**: Renueva el `access` token utilizando el `refresh` token.

## Permisos

El sistema de permisos está basado en roles de usuario, definidos en el modelo de usuario. Los permisos están gestionados por las clases de permisos personalizados:

1. **IsAdmin**: Solo permite el acceso a usuarios con rol `admin`.
2. **IsAdvancedUser**: Solo permite el acceso a usuarios con rol `advanced`.
3. **IsBasicUser**: Solo permite el acceso a usuarios con rol `basic`.


