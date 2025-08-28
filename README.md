# AWS Architecture Enhancer

Aplicación Streamlit que utiliza AWS Agent Strands para mejorar descripciones de arquitectura de nube, generar diagramas Mermaid y código Terraform automáticamente.

## ¿Qué hace esta aplicación?

Si eres nuevo en AWS, esta herramienta te ayuda a:
- ✨ Convertir ideas simples en arquitecturas profesionales
- 🎯 Descubrir qué servicios AWS necesitas
- 📊 Ver tu arquitectura en diagramas bonitos
- 🏗️ Generar código Terraform listo para usar

## Características

- 🤖 **Agent Strands Integration**: Utiliza AWS Agent Strands con Amazon Nova Pro para análisis inteligente
- 📝 **Mejora de Descripciones**: Transforma descripciones básicas en arquitecturas detalladas
- ☁️ **Inventario de Servicios**: Identifica y recomienda servicios AWS apropiados
- 🔄 **Flujo de Datos**: Mapea el flujo de información en la arquitectura
- 📊 **Diagramas Mermaid**: Genera diagramas visuales automáticamente con renderizado en tiempo real
- 🏗️ **Infrastructure as Code**: Genera código Terraform completo usando MCP Terraform Server
- 🔒 **Consideraciones de Seguridad**: Incluye recomendaciones de seguridad
- 📈 **Escalabilidad**: Proporciona notas sobre escalabilidad
- 🎨 **Interfaz Interactiva**: Streaming de respuestas en tiempo real

## Instalación

### Permisos necesarios
- Amazon Bedrock (modelo Nova Pro y Claude Sonnet 4.0)

### Configuración de Amazon Bedrock
Para este taller utilizaremos Amazon Bedrock, un servicio completamente administrado que ofrece una selección de modelos fundacionales (FMs) de alto rendimiento de empresas líderes en IA como Stability AI, Anthropic y Meta, a través de una única API, junto con un amplio conjunto de capacidades que necesitas para construir aplicaciones de IA generativa con seguridad, privacidad e IA responsable.

Antes de poder construir nuestros agentes, necesitamos habilitar el acceso a los modelos en nuestra cuenta.

#### Acceso a Modelos
Antes de comenzar a construir con Bedrock, necesitaremos conceder acceso a modelos para nuestra cuenta.

* Inicia sesión en AWS Console y dirígete a la página de acceso a modelos de <a href="https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/" target="_blank">Amazon Bedrock</a>

* Selecciona el botón "Enable specific models".
* Selecciona las casillas de verificación listadas a continuación:
  * Amazon (selecciona Amazon para seleccionar automáticamente todos los modelos de Amazon).
  * Anthropic: Claude 4 Sonnet, Claude 3.7 Sonnet, Claude 3.5 Sonnet v2, Claude 3.5 Haiku

* Haz clic en "Request model access" para activar los modelos en tu cuenta.

Verifica que el estado de acceso al modelo sea "Access granted" para los modelos seleccionados anteriormente.
Supervisa el estado de acceso al modelo. Puede tomar unos minutos para que los modelos pasen del estado **"In Progress"** a **"Access granted"**. Puedes usar el botón "Refresh" para verificar periódicamente las actualizaciones.


### Prerrequisitos
- Python 3.8+
- Credenciales AWS configuradas
- uvx instalado

### Instalación
```bash
git clone https://github.com/abarrales/autoarchdemo.git
cd autoarchdemo

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
python3 -m pip install -r requirements.txt
```

## Uso

1. **Ejecutar:** `streamlit run app.py`
2. **Abrir:** `http://localhost:8501`
3. **Describir:** Tu idea de arquitectura o usar ejemplos
4. **Generar:** Haz clic en "🚀 Mejorar Arquitectura"

## Ejemplos para Probar

### Para Principiantes
```
Una aplicación web simple con base de datos y almacenamiento de imágenes
```

### Más Avanzado
```
Plataforma de comercio electrónico con alta disponibilidad
```

### ¿No sabes qué escribir?
Usa los ejemplos predefinidos en la aplicación - ¡están listos para usar!

## ¿Cómo Funciona? (Para Curiosos)

### 🧠 Agente 1: Mejorador de Arquitectura
- Lee tu descripción simple
- Piensa qué servicios AWS necesitas
- Te explica por qué cada servicio es útil
- Añade tips de seguridad

### 🎨 Agente 2: Creador de Diagramas
- Toma la arquitectura mejorada
- Crea un diagrama visual bonito
- Organiza todo de manera lógica
- Usa colores para que sea fácil de entender

### 🏗️ Agente 3: Generador de Terraform
- Convierte todo en código real
- Crea archivos que puedes usar en AWS
- Incluye redes, seguridad y servicios
- ¡Listo para implementar!

## Estructura

```
AutoArchDemo/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
└── README.md          # Documentación
```

## Configuración AWS

### Credenciales
Configura AWS CLI o variables de entorno:
```bash
aws configure
# O exporta variables:
export AWS_ACCESS_KEY_ID=tu_key
export AWS_SECRET_ACCESS_KEY=tu_secret
export AWS_DEFAULT_REGION=us-east-1
```

## Tecnologías

- **Streamlit**: Interfaz web
- **AWS Agent Strands**: Agentes IA
- **Amazon Bedrock**: Modelo Nova Pro
- **MCP Terraform**: Generación IaC
- **Mermaid**: Diagramas visuales

## Troubleshooting

- **Error AWS**: Verifica credenciales y permisos Bedrock
- **Error Python**: Instala Python 3.8+
- **Interfaz**: Actualiza navegador o usa incógnito

## Contribuir

1. Fork el proyecto
2. Crea una rama
3. Haz cambios
4. Abre Pull Request

## Licencia

Código abierto - úsalo libremente.