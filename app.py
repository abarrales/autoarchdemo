import streamlit as st
import streamlit.components.v1
import json
from typing import Dict, Any
from strands import Agent, tool
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
from strands_tools import image_reader
from strands.models import BedrockModel

import asyncio
import nest_asyncio
nest_asyncio.apply()

import tempfile

# Configuración de la página
st.set_page_config(
    page_title="AWS Architecture Enhancer",
    page_icon="🏗️",
    layout="wide"
)

async def enhance_architecture(description: str, image_file=None) -> Dict[str, Any]:
    """Mejora descripción usando Strands Agent inline"""
    try:
        my_msg = st.empty()
        acumulated_data = ""
        
        # Agent con modelo multimodal
        agent = Agent(
            tools=[image_reader],
            system_prompt="""Eres un arquitecto AWS experto. Puedes recibir una imagen o una descripcion de la solución, analízala detalladamente identificando todos los componentes y servicios y genera solo el JSON con el siguiente formato:
            {"enhanced_description": "...", "aws_services": [{"service": "...", "purpose": "..."}], 
                "data_flow": "...", "security_considerations": "..."}
                 MOST CRITICAL: respond with raw JSON only. No markdown, no explanations. No code block formatting""",
                callback_handler=None
        )

        user_prompt = f"Analiza y mejora esta arquitectura: {description}"

        # Si hay imagen, procesarla como archivo temporal para utilizar la tool del Agente image_reader
        if image_file:
            st.image(image_file, caption="Imagen de arquitectura cargada", width=300)
            ext_map = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/jpg': '.jpg'}
            file_ext = ext_map.get(image_file.type, '.png')
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(image_file.read())
                tmp_filepath = tmp_file.name
            user_prompt = f"Analiza la arquitectura en la imagen: {tmp_filepath}"
            
        # Ejecutamos Agente y enviamos Stream de analisis de descripción o de imagen de Arquitectura
        async for event in agent.stream_async(user_prompt):
            if "data" in event:
                acumulated_data += event['data']
                my_msg.code(acumulated_data, language="json", height=250, wrap_lines=True)

        result = json.loads(str(acumulated_data))
        st.success("✅ Arquitectura mejorada!")

        return result
    except Exception as e:
        st.warning(f"⚠️ Fallback activo: {str(e)}")
    
    # Fallback
    return {
        "enhanced_description": f"Arquitectura mejorada: {description}. Implementa alta disponibilidad con múltiples AZ.",
        "aws_services": [
            {"service": "Amazon EC2", "purpose": "Computación escalable"},
            {"service": "Application Load Balancer", "purpose": "Distribución de tráfico"},
            {"service": "Amazon RDS", "purpose": "Base de datos gestionada"}
        ],
        "data_flow": "Usuario → ALB → EC2 → RDS",
        "security_considerations": "VPC, Security Groups, cifrado"
    }

def generate_mermaid_diagram(enhanced_architecture: Dict[str, Any]) -> str:
    """Genera diagrama Mermaid usando Strands Agent"""

    try:
        # Agent inline para diagramas
        agent = Agent(
            system_prompt="""Eres un experto en diagramas Mermaid.
            Usa sintaxis: graph TD, incluye subgrafos para VPC/subredes cuando aplique, aplica estilos con colores.
            NO agregues explicaciones."""
        )
        
        services = [s['service'] for s in enhanced_architecture['aws_services']]
        prompt = f"""Crea un diagrama Mermaid para esta arquitectura AWS:
        
        Servicios: {', '.join(services)}
        Flujo: {enhanced_architecture['data_flow']}
        
        Genera ÚNICAMENTE código Mermaid válido y funcional without code block formatting."""
        
        response = agent(prompt)
        diagram_code = str(response).strip()
        st.success("✅ Diagrama generado!")

        return diagram_code
        
    except Exception as e:
        st.warning(f"⚠️ Usando diagrama básico: {str(e)}")
        
    # Fallback
    return """
graph TD
    A[Usuario] --> B[CloudFront]
    B --> C[ALB]
    C --> D[EC2-AZ1]
    C --> E[EC2-AZ2]
    D --> F[RDS]
    E --> F
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    """

def build_user_prompt(enhanced_architecture: Dict[str, Any]) -> str:
    """Construye el prompt para el agente de Strands"""

    services = [s['service'] for s in enhanced_architecture['aws_services']]
    return f"""Genera una arquitectura AWS basada en esta descripción:

    Descripción: {enhanced_architecture['enhanced_description']}
    Servicios: {', '.join(services)}
    Flujo: {enhanced_architecture['data_flow']}
    Seguridad: {enhanced_architecture['security_considerations']}

    Genera ÚNICAMENTE código Terraform válido y completo."""



stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=["awslabs.terraform-mcp-server@latest"]
    )
))

async def generate_terraform_code(enhanced_architecture: Dict[str, Any]) -> str:
    """Genera código Terraform usando Strands Agent"""

    try:
        my_msg = st.empty()
        acumulated_data = ""

        bedrock_model = BedrockModel(
            model_id="us.amazon.nova-pro-v1:0",
            temperature=0.1,
            max_tokens=8000
        )
    
        with stdio_mcp_client:
            tools = stdio_mcp_client.list_tools_sync()

            agent = Agent(
                model=bedrock_model,
                tools=tools,
                system_prompt="""Eres un experto en Terraform y AWS.
                    Genera código Terraform completo y funcional basado en la arquitectura.
                    Incluye VPC, subnets, security groups y todos los servicios mencionados.
                    Usa solo las tools (Terraform Best Practices) y (Checkov) para generar el template.
                    NO agregues explicaciones, CRITICO: solo crea código Terraform válido"""
            )

            user_prompt = build_user_prompt(enhanced_architecture)
            
            async for event in agent.stream_async(user_prompt):
                if "data" in event:
                    acumulated_data += event['data']
                    my_msg.code(acumulated_data, language="hcl", height=400, wrap_lines=True)

        terraform_code = str(acumulated_data).strip()
        st.success("✅ Terraform generado!")
        return terraform_code
    
    except Exception as e:
        st.warning(f"⚠️ Usando template de ejemplo: {str(e)}")


    # Fallback
    services = [s['service'] for s in enhanced_architecture['aws_services']]
    return f"""# Terraform configuration for: {enhanced_architecture['enhanced_description'][:50]}...
resource "aws_vpc" "main" {{
  cidr_block = "10.0.0.0/16"
  tags = {{ Name = "main-vpc" }}
}}
# Add resources based on services: {', '.join(services)}"""



async def main():
    st.title("🏗️ AWS Architecture Enhancer")
    st.markdown("*Potenciado por AWS Agent Strands*")
    
    # Entrada
    examples = {
        "Web Básica": "Una aplicación web simple con base de datos y almacenamiento de imágenes",
        "E-commerce": "Plataforma de comercio electrónico con alta disponibilidad"
    }
    
    selected = st.selectbox("Ejemplos:", ["Personalizado"] + list(examples.keys()))
    default_text = examples.get(selected, "")
    
    # Opción de imagen
    uploaded_file = st.file_uploader("📷 O sube una imagen de arquitectura:", type=['png', 'jpg', 'jpeg'])
    
    user_description = st.text_area(
        "Describe tu arquitectura:",
        value=default_text if not uploaded_file else "Analiza esta imagen de arquitectura y describe los componentes, servicios AWS y flujo de datos que observas",
        height=100
    )
    
    if st.button("🚀 Mejorar Arquitectura", type="primary"):
        if user_description:
            with st.spinner("🤖 Mejorando arquitectura..."):
                enhanced = await enhance_architecture(user_description, uploaded_file)
                st.session_state.result = enhanced
          
    
    # Resultados
    if 'result' in st.session_state:
        result = st.session_state.result
        
        # 1. Descripción Mejorada
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Descripción Mejorada")
            st.write(result['enhanced_description'])
        
        with col2:
            st.subheader("☁️ Servicios AWS")
            for service in result['aws_services']:
                st.write(f"• **{service['service']}**: {service['purpose']}")
        
        with st.spinner("🤖 Generando diagrama mermaid..."):
            st.session_state.diagram = generate_mermaid_diagram(result)

        # 2. Diagrama
        st.subheader("📊 Diagrama")
        if 'diagram' in st.session_state:
            tab1, tab2 = st.tabs(["🎨 Visualización", "📝 Código"])
            
            with tab1:
                st.components.v1.html(f"""
                <div style="overflow: auto; max-height: 800px; border: 1px solid #ddd; border-radius: 5px;">
                    <div class="mermaid">{st.session_state.diagram}</div>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                <script>mermaid.initialize({{startOnLoad: true}});</script>
                """, height=800, scrolling=True)
            
            with tab2:
                st.code(st.session_state.diagram, language="mermaid")
                st.download_button(
                    label="💾 Descargar .mmd",
                    data=st.session_state.diagram,
                    file_name="architecture_diagram.mmd",
                    mime="text/plain"
                )
        
        # 3. Infrastructure as Code
        st.subheader("🏗️ Infrastructure as Code")
        iac_tab1, = st.tabs(["📝 Código Terraform"])
        
        with iac_tab1:
            if 'terraform_code' not in st.session_state:
                with st.spinner("🔧 Generando Terraform..."):
                    st.session_state.terraform_code = await generate_terraform_code(result)
            
            # st.code(st.session_state.terraform_code, language="hcl", height=400)
            st.download_button("💾 Descargar .tf", st.session_state.terraform_code, "main.tf", "text/plain")

if __name__ == "__main__":
    # main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())