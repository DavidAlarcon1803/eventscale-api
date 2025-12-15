from fastapi.openapi.docs import get_swagger_ui_html

def custom_openapi(app):
    """
    Genera una interfaz de Swagger personalizada con tema Oscuro y Neón.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Docs",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        html_content_custom=None 
    )

custom_css = """
<style>
    /* Fondo General */
    body {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
    }
    .swagger-ui .topbar { 
        background-color: #161b22 !important; 
        border-bottom: 1px solid #30363d;
    }
    
    /* Textos y Títulos */
    .swagger-ui .info .title, 
    .swagger-ui .info h1, .swagger-ui .info h2, 
    .swagger-ui .info h3, .swagger-ui .info h4, 
    .swagger-ui .info h5 {
        color: #e6edf3 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* El toque NEÓN (Tu color de marca #00ff99) */
    .swagger-ui .info .title small {
        background-color: #00ff99 !important;
        color: #000 !important;
        border-radius: 4px;
        padding: 2px 8px;
    }
    .swagger-ui a.nostyle, .swagger-ui .info a {
        color: #00ff99 !important;
    }
    
    /* Bloques de Operaciones (GET, POST, etc.) */
    .swagger-ui .opblock {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }
    .swagger-ui .opblock:hover {
        border-color: #00ff99 !important; /* Glow al pasar el mouse */
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.1) !important;
    }
    
    /* Textos dentro de los bloques */
    .swagger-ui .opblock .opblock-summary-operation-id,
    .swagger-ui .opblock .opblock-summary-path,
    .swagger-ui .opblock .opblock-summary-path__deprecated,
    .swagger-ui .opblock-description-wrapper p,
    .swagger-ui .responses-inner h4,
    .swagger-ui .responses-inner h5 {
        color: #c9d1d9 !important;
    }
    
    /* Botones (Authorize y Execute) */
    .swagger-ui .btn.authorize, .swagger-ui .btn.execute {
        background-color: transparent !important;
        border: 1px solid #00ff99 !important;
        color: #00ff99 !important;
        box-shadow: none !important;
    }
    .swagger-ui .btn.authorize:hover, .swagger-ui .btn.execute:hover {
        background-color: #00ff99 !important;
        color: #000 !important;
        box-shadow: 0 0 15px rgba(0, 255, 153, 0.4) !important;
    }
    .swagger-ui .btn.authorize svg {
        fill: #00ff99 !important;
    }
    
    /* Inputs y Formularios */
    .swagger-ui input[type=text], .swagger-ui input[type=email], .swagger-ui input[type=password], .swagger-ui textarea {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #fff !important;
    }
    .swagger-ui select {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #fff !important;
    }
    
    /* Modelos/Schemas */
    .swagger-ui .model-box {
        background-color: #161b22 !important;
    }
    .swagger-ui section.models h4 {
        color: #c9d1d9 !important;
    }
    .swagger-ui .model {
        color: #c9d1d9 !important;
    }
    
    /* Flechas y decoraciones */
    .swagger-ui .expand-methods svg, .swagger-ui .expand-operation svg {
        fill: #8b949e !important;
    }
</style>
"""
