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



