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
