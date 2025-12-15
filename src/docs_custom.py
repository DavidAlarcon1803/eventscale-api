from fastapi.openapi.docs import get_swagger_ui_html

def custom_openapi(app):
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Docs",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}
    )

custom_css = """
<style>
    /* --- FONDO NEGRO PROFUNDO TOTAL --- */
    body {
        background-color: #000000 !important; /* Negro puro */
        color: #e6edf3 !important;
    }
    
    /* El contenedor principal también en negro */
    .swagger-ui {
        background-color: #000000 !important;
    }

    /* --- CORRECCIÓN DE LA FRANJA BLANCA (Authorize) --- */
    .swagger-ui .scheme-container {
        background-color: #000000 !important; /* Fondo negro */
        box-shadow: none !important;           /* Quitar sombra */
        border-bottom: 1px solid #333 !important; /* Línea sutil separadora */
        margin-bottom: 30px !important;
        padding: 30px 0 !important;
    }

    /* --- BARRA SUPERIOR (Donde dice el título) --- */
    .swagger-ui .topbar { 
        background-color: #000000 !important; 
        border-bottom: 1px solid #00ff99; /* Línea neón separadora */
    }
    .swagger-ui .topbar-wrapper img {
        content: url('https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png'); /* Opcional: Logo que combine */
    }

    /* --- TEXTOS Y TÍTULOS --- */
    .swagger-ui .info .title, 
    .swagger-ui .info h1, .swagger-ui .info h2, 
    .swagger-ui .info h3, .swagger-ui .info h4, 
    .swagger-ui .info h5 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif; /* Fuente más moderna si está disponible */
        letter-spacing: 0.5px;
    }
    
    /* Badge de versión y links */
    .swagger-ui .info .title small {
        background-color: #00ff99 !important;
        color: #000 !important;
        font-weight: bold;
        border-radius: 4px;
        padding: 4px 10px;
    }
    .swagger-ui a.nostyle, .swagger-ui .info a {
        color: #00ff99 !important;
        text-decoration: none;
    }
    
    /* --- BLOQUES DE OPERACIONES (Las tarjetas) --- */
    .swagger-ui .opblock {
        background: #080808 !important; /* Ligeramente más claro que el fondo #000 */
        border: 1px solid #222 !important;
        border-radius: 12px !important; /* Bordes más redondeados */
        box-shadow: none !important;
        margin-bottom: 20px !important;
        transition: all 0.3s ease;
    }
    
    /* Efecto Hover estilo Neón */
    .swagger-ui .opblock:hover {
        border-color: #00ff99 !important;
        box-shadow: 0 0 15px rgba(0, 255, 153, 0.15) !important;
    }
    
    /* Resumen de la operación (La barra visible siempre) */
    .swagger-ui .opblock .opblock-summary {
        border-bottom: 1px solid #1a1a1a !important;
    }
    
    /* Textos dentro de los bloques */
    .swagger-ui .opblock .opblock-summary-operation-id,
    .swagger-ui .opblock .opblock-summary-path,
    .swagger-ui .opblock .opblock-summary-path__deprecated,
    .swagger-ui .opblock-description-wrapper p,
    .swagger-ui .responses-inner h4,
    .swagger-ui .responses-inner h5 {
        color: #cccccc !important;
    }
    
    /* Flecha desplegable */
    .swagger-ui .opblock .opblock-summary .view-line-link.copy-to-clipboard {
        display: none !important; /* Ocultar icono de copiar ruidoso */
    }
    .swagger-ui .opblock-summary-control svg {
        fill: #666 !important;
    }

    /* --- BOTONES (Authorize y Execute) --- */
    .swagger-ui .btn.authorize {
        background-color: transparent !important;
        border: 1px solid #00ff99 !important;
        color: #00ff99 !important;
        border-radius: 8px !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .swagger-ui .btn.authorize:hover {
        background-color: rgba(0, 255, 153, 0.1) !important;
        box-shadow: 0 0 15px rgba(0, 255, 153, 0.4) !important;
    }
    .swagger-ui .btn.authorize svg {
        fill: #00ff99 !important;
    }
    
    .swagger-ui .btn.execute {
        background-color: #00ff99 !important;
        color: #000 !important;
        border: none !important;
        width: 100%; /* Botón grande y cómodo */
        border-radius: 6px;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.3);
    }

    /* --- FORMULARIOS E INPUTS --- */
    .swagger-ui input[type=text], 
    .swagger-ui input[type=email], 
    .swagger-ui input[type=password], 
    .swagger-ui textarea,
    .swagger-ui select {
        background-color: #000000 !important;
        border: 1px solid #333 !important;
        color: #fff !important;
        border-radius: 6px !important;
    }
    .swagger-ui input:focus, .swagger-ui textarea:focus {
        border-color: #00ff99 !important;
        outline: none !important;
    }

    /* --- MODELOS / SCHEMAS --- */
    .swagger-ui section.models {
        border: 1px solid #222;
        border-radius: 12px;
        background: #050505;
        padding: 20px;
    }
    .swagger-ui section.models h4 {
        color: #fff !important;
    }
    .swagger-ui .model-box {
        background-color: transparent !important;
    }
    .swagger-ui .model {
        color: #ccc !important;
    }
    .swagger-ui .prop-type {
        color: #00ff99 !important; /* Tipos de datos en verde neón */
    }
</style>
"""
