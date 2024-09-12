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
Inicia el servidor de desarrollo de Django en el puerto 8000.

## 3. Ejecutar Docker Compose Sin Construcción (Para Ejecuciones Futuras)
Para ejecutar el proyecto sin reconstruir las imágenes (esto es útil después de la primera ejecución):
```bash
docker-compose up
```

## **Guía básica de uso de las APIs REST del proyecto.**

Esta guía explica cómo interactuar con los diferentes endpoints de la APIs para gestionar vulnerabilidades, alertas y usuarios. A través de estos pasos, puedes obtener vulnerabilidades desde la base de datos NIST, marcarlas como corregidas y recibir notificaciones por correo. También veremos cómo registrar, autenticar y administrar usuarios. 

### 1. Obtener todas las vulnerabilidades

#### Endpoint
**GET**: `http://127.0.0.1:8000/v1/vulnerabilities/`

Este endpoint te permite obtener una lista de todas las vulnerabilidades registradas en la base de datos de NIST. La respuesta incluye información relevante, como el ID de la vulnerabilidad (CVE), una descripción y su severidad.

Ejemplo de respuesta:
![image](https://github.com/user-attachments/assets/1142f664-96e1-4969-9d3c-850071832dab)
  
### 2. Marcar una vulnerabilidad como corregida

#### Endpoint
**POST**: `http://127.0.0.1:8000/v1/vulnerabilities/fixed/`

Para marcar una vulnerabilidad como corregida, envía la información correspondiente en un formato JSON. Aquí se indica que la vulnerabilidad **CVE-1999-0095** ha sido corregida.

Entrada JSON de ejemplo:
```json
{
    "id": "CVE-1999-0095",
    "description": "The debug command in Sendmail is enabled, allowing attackers to execute commands as root.",
    "severity": "HIGH"
}
```

![image](https://github.com/user-attachments/assets/84cae98b-53f5-4d0b-8795-41b14812d7a8)

### 3. Obtener vulnerabilidades no corregidas

#### Endpoint
**GET**: `http://127.0.0.1:8000/v1/vulnerabilities/unfixed/`

Este endpoint devuelve una lista de vulnerabilidades que aún no han sido marcadas como corregidas. Si consultas este endpoint después de marcar una vulnerabilidad como corregida, esta ya no aparecerá en la lista.

Por ejemplo, si acabas de corregir **CVE-1999-0095**, ya no debería figurar en los resultados, pero sí las demas vulnerabilidades

![image](https://github.com/user-attachments/assets/eee16bc2-5648-414b-98e0-235f01259497)

Este comportamiento es importante porque confirma que la acción de marcación ha tenido efecto.

### 4. Obtener un resumen de vulnerabilidades agrupadas por severidad

#### Endpoint
**GET**: `http://127.0.0.1:8000/v1/vulnerabilities/summary/`

Este endpoint proporciona un resumen general de todas las vulnerabilidades, agrupadas según su severidad (por ejemplo, **HIGH**, **MEDIUM**, **LOW**). Te permite ver cuántas vulnerabilidades existen en cada categoría.

![image](https://github.com/user-attachments/assets/cbabd65d-a6b9-47ee-99e9-0aaccf811628)

El resumen es útil para comprender la gravedad general de las vulnerabilidades en el sistema y priorizar las correcciones.

### 5. Ver todas las alertas

#### Endpoint
**GET**: `http://127.0.0.1:8000/v1/alerts/`

Cuando se marca una vulnerabilidad como corregida, se genera una alerta o notificación que se envía al destinatario especificado. En este caso, una alerta será enviada notificando que la vulnerabilidad **CVE-1999-0095** ha sido corregida. Puedes consultar todas las alertas utilizando este endpoint.

Las alertas se envían dependiendo de la severidad de la vulnerabilidad fixeada por un medio de notificación diferene, por ejemplo para la vulnerabilidad fixeada que ingresamos cuya severidad es HIGH sera enviada la alerta por correo electrónico:

![image](https://github.com/user-attachments/assets/772ee576-2078-4961-a63c-f1f38c7b196b)

### 6. Registrar un nuevo usuario

#### Endpoint
**POST**: `http://127.0.0.1:8000/v1/auth/register/`

Para registrar un nuevo usuario, se envían detalles como el nombre de usuario, la contraseña y el correo electrónico. En este ejemplo, estamos registrando un usuario con rol de administrador.

Entrada JSON:
```json
{
    "username": "prueba",
    "password": "123",
    "email": "prueba@correo.com",
    "role": "admin"
}
```

Después de realizar esta acción, el sistema confirmará que el usuario se ha registrado con éxito.

![image](https://github.com/user-attachments/assets/cb3273ab-a7e3-40d2-87de-d8392a2e57e4)

### 7. Iniciar sesión

#### Endpoint
**POST**: `http://127.0.0.1:8000/v1/auth/login/`

Este endpoint es para iniciar sesión en el sistema. Debes enviar el nombre de usuario y la contraseña que se utilizaron al registrarse. El sistema te devolverá un token de acceso y un token de refresco que puedes usar para futuras solicitudes autenticadas.

Entrada JSON:
```json
{
    "username": "prueba",
    "password": "123"
}
```

![image](https://github.com/user-attachments/assets/cb0ffd92-b3e9-4404-b54f-286ecc4ee66d)

El token de acceso te permite realizar solicitudes protegidas, mientras que el token de refresco sirve para obtener un nuevo token de acceso cuando expire.

### 8. Refrescar el token de acceso

#### Endpoint
**POST**: `http://127.0.0.1:8000/v1/auth/refresh/`

Cuando el token de acceso expira, puedes usar este endpoint para obtener uno nuevo usando el token de refresco. Esto asegura que el usuario no tenga que iniciar sesión nuevamente.
El token de acceso debe ser dado por el JWT Bearer y en el cuerdo de la solicitud el token de refresh:

Entrada JSON:
```json
{
    "refresh": "token_de_refresh_aquí"
}
```

![image](https://github.com/user-attachments/assets/ba6d49ce-572c-4f1b-b8bf-e1c618d50047)

El sistema devolverá un nuevo token de acceso que puedes usar en futuras solicitudes.

### 9. Cerrar sesión

#### Endpoint
**POST**: `http://127.0.0.1:8000/v1/auth/logout/`

Para cerrar sesión, utiliza este endpoint. Debes enviar el token de refresco junto con el token de acceso en el encabezado de la solicitud. Esto revocará el token, y si intentas usarlo después de cerrar sesión, recibirás un error de "Token is blacklisted".
El token de acceso debe ser dado por el JWT Bearer y en el cuerdo de la solicitud el token de refresh:

Entrada JSON:
```json
{
    "refresh": "token_de_refresh_aquí"
}
```

![image](https://github.com/user-attachments/assets/95680f2c-a15a-414e-afea-080ff181e209)

![image](https://github.com/user-attachments/assets/f5029767-8b2b-4faf-b9af-85b46616caac)

Esto garantiza que no puedas utilizar tokens que ya han sido revocados, añadiendo una capa extra de seguridad.

---




# **Descripciones y algunas explicaciones cortas de funcionalidades y apps django del proyecto**

# Implementación de Rate Limiting
El proyecto implementa un rate limiter o limitador de tasa que restringe el número de peticiones que se pueden realizar a la API. Este rate limiter ha sido configurado para permitir un máximo de 15 peticiones por minuto, lo que previene que un solo cliente realice demasiadas solicitudes en un corto periodo, evitando una sobrecarga en la API.

Cuando se supera este límite, el cliente recibe una respuesta de error (429 Too Many Requests), indicando que deberá esperar antes de realizar más solicitudes. Este mecanismo protege tanto el servidor como el cliente al regular el flujo de datos y asegurar un acceso justo para todos los usuarios.

# Logging
En el proyecto, se implementó el uso de logging para mejorar la visibilidad y el rastreo de los eventos y errores dentro de la aplicación. Este enfoque nos permite registrar información clave sobre la ejecución del código, como la recuperación de datos desde una API externa o el estado de la caché. Gracias a los logs, podemos monitorizar la aplicación de manera más efectiva, identificar y diagnosticar problemas rápidamente y mantener un registro detallado de las operaciones realizadas, lo cual es fundamental para el mantenimiento y la depuración del sistema. El uso de logging contribuye significativamente a la robustez y la transparencia del proyecto.

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


