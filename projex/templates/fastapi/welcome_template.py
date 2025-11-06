WELCOME_HTML = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>FastAPI - Powered by Projex</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;background:#FAFAFA;color:#1A1A1A;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem}
        .container{max-width:900px;width:100%}
        .header{text-align:center;margin-bottom:4rem}
        .logo{font-size:48px;margin-bottom:1rem}
        .title{font-size:48px;font-weight:700;margin-bottom:.5rem;color:#1A1A1A}
        .subtitle{font-size:18px;color:#666}
        .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.5rem;margin-bottom:4rem}
        .card{background:#fff;border:1px solid #E5E5E5;border-radius:8px;padding:2rem;text-decoration:none;color:inherit;transition:all .2s ease}
        .card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,150,136,.08);border-color:#009688}
        .card-icon{font-size:24px;margin-bottom:1rem}
        .card-title{font-size:20px;font-weight:600;margin-bottom:.5rem;color:#1A1A1A}
        .card-title::after{content:' →';color:#009688}
        .card-description{font-size:16px;color:#666;line-height:1.5}
        .footer{text-align:center;padding-top:2rem;border-top:1px solid #E5E5E5}
        .footer a{color:#666;text-decoration:none;font-size:14px;transition:color .2s ease}
        .footer a:hover{color:#009688}
        @media (max-width:768px){.title{font-size:32px}.cards{grid-template-columns:1fr}}
    </style>
</head>
<body>
    <div class=\"container\">
        <div class=\"header\">
            <div class=\"logo\">⚡</div>
            <h1 class=\"title\">FastAPI</h1>
            <p class=\"subtitle\">Modern, fast (high-performance) Python web framework</p>
        </div>
        <div class=\"cards\">
            <a href=\"/docs\" class=\"card\">
                <div class=\"card-icon\">📖</div>
                <h3 class=\"card-title\">Documentation</h3>
                <p class=\"card-description\">Interactive API docs at /docs</p>
            </a>
            <a href=\"https://fastapi.tiangolo.com\" target=\"_blank\" class=\"card\">
                <div class=\"card-icon\">📚</div>
                <h3 class=\"card-title\">Learn</h3>
                <p class=\"card-description\">Explore the official FastAPI documentation</p>
            </a>
            <a href=\"https://chabdulwahhab.github.io/projex/\" target=\"_blank\" class=\"card\">
                <div class=\"card-icon\">🔨</div>
                <h3 class=\"card-title\">Projex Docs</h3>
                <p class=\"card-description\">Guides and references for Projex CLI</p>
            </a>
            <a href=\"https://github.com/ChAbdulWahhab/projex\" target=\"_blank\" class=\"card\">
                <div class=\"card-icon\">⭐</div>
                <h3 class=\"card-title\">Star on GitHub</h3>
                <p class=\"card-description\">Support the project by leaving a star</p>
            </a>
        </div>
        <div class=\"footer\">
            <a href=\"https://github.com/ChAbdulWahhab/projex\" target=\"_blank\">By Projex →</a>
        </div>
    </div>
</body>
</html>
"""


def get_welcome_template() -> str:
    return WELCOME_HTML


