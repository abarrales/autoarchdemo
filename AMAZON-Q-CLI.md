# Amazon Q Developer CLI - Guía de Instalación

## 🚀 Instalación Automática

Este directorio incluye el script `install-amazon-q-cli.sh` que automatiza completamente la instalación de Amazon Q Developer CLI en Ubuntu ARM64.

### Uso Rápido

```bash
# Ejecutar desde el directorio autoarchdemo
./install-amazon-q-cli.sh
```

## 📋 ¿Qué hace el script?

El script `install-amazon-q-cli.sh` realiza las siguientes acciones:

1. **📦 Actualización del sistema**
   - Ejecuta `sudo apt update -y`
   - Instala dependencias: `curl` y `unzip`

2. **⬇️ Descarga automática**
   - Descarga la versión ARM64 de Amazon Q CLI
   - URL: `https://desktop-release.codewhisperer.us-east-1.amazonaws.com/latest/q-aarch64-linux.zip`

3. **🔧 Instalación**
   - Extrae el archivo ZIP descargado
   - Ejecuta el instalador oficial: `bash ./q/install.sh`

4. **🧹 Limpieza**
   - Elimina archivos temporales (`q.zip`, directorio `q/`)
   - Deja el sistema limpio

## ✅ Verificación Post-Instalación

Después de ejecutar el script, verifica que la instalación fue exitosa:

```bash
# Verificar versión instalada
q --version

# Debería mostrar algo como:
# Amazon Q CLI version x.x.x
```

## ⚙️ Configuración Inicial

### Configurar Credenciales AWS (Opcional)

```bash
# Configurar Amazon Q CLI con tus credenciales
q configure

# Seguir las instrucciones en pantalla para:
# - AWS Access Key ID
# - AWS Secret Access Key  
# - Default region
```

### Configuración con AWS SSO (Recomendado)

```bash
# Si usas AWS SSO
q configure sso
```

## 🎯 Comandos Útiles

### Asistencia General
```bash
# Hacer preguntas sobre AWS
q ask "¿Cómo crear un bucket S3?"
q ask "¿Cuáles son las mejores prácticas para Lambda?"
```

### Generación de Código
```bash
# Generar código específico
q generate "función Python para conectar a DynamoDB"
q generate "template CloudFormation para VPC"
```

### Ayuda y Documentación
```bash
# Ver todos los comandos disponibles
q --help

# Ayuda específica para un comando
q ask --help
q generate --help
```

## 🔧 Troubleshooting

### Problema: "q: command not found"

**Solución:**
```bash
# Verificar que el PATH incluya ~/.local/bin
echo $PATH

# Si no está incluido, agregar a ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Problema: Permisos de ejecución

**Solución:**
```bash
# Dar permisos de ejecución al script
chmod +x install-amazon-q-cli.sh
```

### Problema: Error de descarga

**Verificar:**
- Conexión a internet
- Disponibilidad del servidor de Amazon

**Solución alternativa:**
```bash
# Descargar manualmente
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.codewhisperer.us-east-1.amazonaws.com/latest/q-aarch64-linux.zip" \
  -o "q.zip"
```

## 🏗️ Integración con AutoArchDemo

Amazon Q CLI complementa perfectamente esta aplicación:

1. **Durante el desarrollo**: Usa Q CLI para generar código adicional
2. **Para debugging**: Pregunta sobre errores específicos
3. **Mejores prácticas**: Consulta optimizaciones para tu arquitectura
4. **Aprendizaje**: Explora servicios AWS mencionados en los diagramas

### Ejemplo de Flujo de Trabajo

```bash
# 1. Ejecutar AutoArchDemo
streamlit run app.py

# 2. Generar arquitectura en la app web

# 3. Usar Q CLI para código adicional
q generate "función Lambda para el flujo generado"

# 4. Preguntar sobre optimizaciones
q ask "¿Cómo optimizar costos en esta arquitectura?"
```

## 📚 Recursos Adicionales

- [Documentación oficial Amazon Q](https://docs.aws.amazon.com/amazonq/)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [Ejemplos de uso en GitHub](https://github.com/aws/amazon-q-developer-cli)

## 🆘 Soporte

Si encuentras problemas:

1. Verifica los logs del script durante la instalación
2. Consulta la documentación oficial de Amazon Q
3. Revisa que tu sistema cumple los requisitos mínimos
4. Usa `q ask` para preguntas específicas sobre errores

---

**Nota**: Este script está optimizado para Ubuntu ARM64. Para otras arquitecturas, consulta la documentación oficial de Amazon Q CLI.