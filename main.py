from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
import asyncio
import os
import smtplib
import sys
from email.message import EmailMessage
from email.utils import parseaddr
from typing import Dict, List, Any
import env

# Playwright spawns subprocesses; on Windows, the Selector event loop policy
# does not implement subprocess APIs and can raise NotImplementedError().
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        # If this fails for any reason, let runtime surface the error.
        pass

SMTP_HOST= env.SMTP_HOST
SMTP_PORT=env.SMTP_PORT
SMTP_USE_TLS=env.SMTP_USE_TLS
SMTP_USERNAME=env.SMTP_USERNAME
SMTP_PASSWORD=env.SMTP_PASSWORD
SMTP_FROM=env.SMTP_FROM


app = FastAPI()

origins = [
    '*',
    'http://127.0.0.1:8010',
    'http://localhost:8010',
    'http://34.239.216.53:8010'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class ProjectFeatures(BaseModel):
    workflows: bool = False
    field_logic: bool = False
    product_logic: bool = False
    session_logic: bool = False
    complex_reporting: bool = False
    housing: bool = False
    table_seating: bool = False
    lookup_integration: bool = False
    hybrid_virtual: bool = False
    multi_event: bool = False
    CEUs: bool = False
    sponsor_branding: bool = False
    leads: bool = False
    complex_workflows: bool = False
    multiple_review_rounds: bool = False
    multiple_proposal_calls: bool = False
    floor_plan: bool = False
    year_round: bool = False
    complex_sponsors: bool = False
    multi_scheduling: bool = False
    first_time_system: bool = False
    matchmaking: bool = False
    personal_agenda: bool = False
    double_sided: bool = False
    logic_based_badges: bool = False
    multi_badge_types: bool = False
    customer_hardware: bool = False
    integrations: bool = False
    SSO: bool = False
    multiple_POCs: bool = False
    recurring_calls: bool = False
    more_than_8_events: bool = False
    bre_include: bool = False
    app_include: bool = False
    abs_include: bool = False
    exh_include: bool = False
    appointments_include: bool = False
    kiosk_include: bool = False


class EmailRequest(BaseModel):
    to_email: str
    customer_name: str
    features: ProjectFeatures


class PdfRequest(BaseModel):
    customer_name: str
    features: ProjectFeatures


@app.get("/")
def index():
    return FileResponse('html/index.html')

@app.get("/health")
def health():
    return {"ok": True}

DESCRIPTIONS = {
    "A": "Additional kick off call / follow ups and questions",
    "B": "Additional training",
    "C": "Review and testing work"
}

JUSTIFICATIONS: Dict[str, str] = {
    "kickoff_wrapup": "Kick Off and Wrap Up calls",
    "module_training": "Module Level Training",
    "support": "Feedback, Questions, and Support",
    "build_config": "Build and Configure",
    "review_testing": "Review and Testing",
    "prepost_meetings": "Meetings for pre and post launch",
}

FEATURE_RULES: Dict[str, Dict[str, Any]] = {
    # --- Attendee Registration (BRE) ---
    "bre_include": {
        "module": "bre",
        "requires": None,
        "hours": {
            "kickoff_wrapup": 2,
            "module_training": 2,
            "support": 2,
            "build_config": 2,
            "review_testing": 1,
            "prepost_meetings": 1,
        },
    },
    "workflows": {
        "module": "bre",
        "requires": "bre_include",
        "hours": {
            "support": 2,
            "build_config": 2,
            "review_testing": 2,
        },
    },

    "field_logic": {
        "module": "bre",
        "requires": "bre_include",
        "hours": {
            "module_training": 1,
            "support": 3,
            "build_config": 4,
            "review_testing": 2,
        },
    },
    "product_logic": {
        "module": "bre",
        "requires": "bre_include",
        "hours": {
            "module_training": 1,
            "support": 3,
            "build_config": 4,
            "review_testing": 2,
        },
    },
    "session_logic": {
        "module": "bre",
        "requires": "bre_include",
        "hours": {
            "module_training": 1,
            "support": 3,
            "build_config": 4,
            "review_testing": 2,
        },
    },
    "complex_reporting": {
        "module": "bre",
        "requires": "bre_include",
        "hours": {
            "module_training": 2,
            "support": 6,
            "build_config": 6,
            "review_testing": 6,
        },
    },
    "housing": {
        "module": "bre",
        "requires": "bre_include",
        "hours": {
            "module_training": 1,
            "support": 3,
            "build_config": 4,
            "review_testing": 2,
            "prepost_meetings": 1,
        },
    },
    "table_seating": {
        "module": "bre",
        "requires": "bre_include",
        "hours": {
            "module_training": 1,
            "support": 3,
            "build_config": 4,
            "review_testing": 2,
            "prepost_meetings": 1,
        },
    },
    "lookup_integration": {
        "module": "bre",
        "requires": "bre_include",
        "hours": {
            "support": 2,
            "build_config": 2,
            "review_testing": 2,
        },
    },

    # --- Mobile App (APP) ---
    "app_include": {
        "module": "app",
        "requires": None,
        "hours": {
            "kickoff_wrapup": 2,
            "module_training": 1,
            "support": 1,
            "review_testing": 1,
        },
    },
    "hybrid_virtual": {
        "module": "app",
        "requires": "app_include",
        "hours": {
            "module_training": 2,
            "support": 4,
            "build_config": 4,
            "review_testing": 4,
            "prepost_meetings": 2,
        },
    },
    "multi_event": {
        "module": "app",
        "requires": "app_include",
        "hours": {
            "build_config": 1,
            "review_testing": 1,
        },
    },
    "CEUs": {
        "module": "app",
        "requires": "app_include",
        "hours": {
            "support": 2,
            "build_config": 2,
            "review_testing": 2,
            "prepost_meetings": 1,
        },
    },
    "sponsor_branding": {
        "module": "app",
        "requires": "app_include",
        "hours": {
            "support": 2,
            "build_config": 2,
            "review_testing": 2,
        },
    },
    "leads": {
        "module": "app",
        "requires": "app_include",
        "hours": {
            "module_training": 1,
            "prepost_meetings": 1,
        },
    },
}

MODULE_LABELS: Dict[str, str] = {
    "bre": "Attendee Registration",
    "app": "Mobile App (Connect) and Connect Online",
}

def _add_hours(target: Dict[str, float], key: str, amount: float) -> None:
    if not amount:
        return
    target[key] = float(target.get(key, 0)) + float(amount)

@app.post("/calculate")
def calculate_classification(features: ProjectFeatures):
    per_module_buckets: Dict[str, Dict[str, float]] = {
        module_key: {k: 0.0 for k in JUSTIFICATIONS.keys()} for module_key in MODULE_LABELS.keys()
    }

    for feature_name, rule in FEATURE_RULES.items():
        if not getattr(features, feature_name, False):
            continue

        requires = rule.get("requires")
        if requires and not getattr(features, requires, False):
            continue

        module_key = rule["module"]
        hours_map: Dict[str, float] = rule.get("hours", {})
        for bucket_key, amount in hours_map.items():
            _add_hours(per_module_buckets[module_key], bucket_key, amount)

    bre_hours = 0
    if getattr(features, "bre_include", False):
        bre_hours = sum(per_module_buckets["bre"].values())
    else:
        per_module_buckets["bre"] = {k: 0.0 for k in JUSTIFICATIONS.keys()}

    app_hours = 0
    if getattr(features, "app_include", False):
        app_hours = sum(per_module_buckets["app"].values())
    else:
        per_module_buckets["app"] = {k: 0.0 for k in JUSTIFICATIONS.keys()}

    # Legacy scoring system for modules not yet migrated to hour breakdown
    BRE_SCORE = 0
    APP_SCORE = 0
    ABS_SCORE = 0
    EXH_SCORE = 0
    APPOINTMENTS_SCORE = 0
    KIOSK_SCORE = 0
    CUSTOM_SCORE = 0
    PM_SCORE = 0

    active_keys = set()

    ## ABSTRACT
    if features.complex_workflows:
        ABS_SCORE += 1
        active_keys.update(["A", "B", "C"])
    if features.multiple_review_rounds:
        ABS_SCORE += 1
        active_keys.update(["A"])
    if features.multiple_proposal_calls:
        ABS_SCORE += 1
        active_keys.update(["A"])

    ## EXHIBITOR REGISTRATION
    if features.floor_plan:
        EXH_SCORE += 1
        active_keys.update(["B", "C"])
    if features.year_round:
        EXH_SCORE += 1
        active_keys.update(["A", "B", "C"])
    if features.complex_sponsors:
        EXH_SCORE += 1
        active_keys.update(["B", "C"])

    ## APPOINTMENTS
    if features.multi_scheduling:
        APPOINTMENTS_SCORE += 1
        active_keys.update(["A", "B", "C"])
    if features.first_time_system:
        APPOINTMENTS_SCORE += 1
        active_keys.update(["A", "B", "C"])
    if features.matchmaking:
        APPOINTMENTS_SCORE += 1
        active_keys.update(["B", "C"])

    ## KIOSK/BADGES
    if features.personal_agenda:
        KIOSK_SCORE += 1
        active_keys.update(["A", "C"])
    if features.double_sided:
        KIOSK_SCORE += 1
        active_keys.update(["A", "C"])
    if features.logic_based_badges:
        KIOSK_SCORE += 1
        active_keys.update(["A", "B", "C"])
    if features.multi_badge_types:
        KIOSK_SCORE += 1
        active_keys.update(["A", "B", "C"])
    if features.customer_hardware:
        KIOSK_SCORE += 1
        active_keys.update(["A", "B", "C"])

    ## CUSTOM
    if features.integrations:
        CUSTOM_SCORE += 1
        active_keys.update(["A", "C"])
    if features.SSO:
        CUSTOM_SCORE += 1
        active_keys.update(["A", "C"])

    ## PROJECT MANAGEMENT
    if features.multiple_POCs:
        PM_SCORE += 1
        active_keys.update(["A", "B"])
    if features.recurring_calls:
        PM_SCORE += 1
        active_keys.update(["A"])
    if features.more_than_8_events:
        PM_SCORE += 1
        active_keys.update(["A"])

    BRE_result = ""
    APP_result = ""

    if not features.abs_include:
        abs_hours = 0
        ABS_result = ""
    else:
        ABS_result = ""
        if ABS_SCORE <= 0:
            abs_hours = 5
        elif ABS_SCORE <= 1:
            abs_hours = 10
        elif ABS_SCORE <= 2:
            abs_hours = 15
        else:
            abs_hours = 30

    if not features.exh_include:
        exh_hours = 0
        EXH_result = ""
    else:
        EXH_result = ""
        if EXH_SCORE <= 0:
            exh_hours = 5
        elif EXH_SCORE <= 1:
            exh_hours = 10
        elif EXH_SCORE <= 2:
            exh_hours = 20
        else:
            exh_hours = 40

    if not features.appointments_include:
        appointments_hours = 0
        APPOINTMENTS_result = ""
    else:
        APPOINTMENTS_result = ""
        if APPOINTMENTS_SCORE <= 0:
            appointments_hours = 5
        elif APPOINTMENTS_SCORE <= 1:
            appointments_hours = 10
        elif APPOINTMENTS_SCORE <= 2:
            appointments_hours = 25
        else:
            appointments_hours = 50

    if not features.kiosk_include:
        kiosk_hours = 0
        KIOSK_result = ""
    else:
        KIOSK_result = ""
        if KIOSK_SCORE <= 0:
            kiosk_hours = 5
        elif KIOSK_SCORE <= 1:
            kiosk_hours = 10
        elif KIOSK_SCORE <= 2:
            kiosk_hours = 15
        else:
            kiosk_hours = 30

    if CUSTOM_SCORE + PM_SCORE == 0:
        additional_hours = 0
        additional_result = "None"
    elif CUSTOM_SCORE + PM_SCORE <= 2:
        additional_hours = 15
        additional_result = ""
    elif CUSTOM_SCORE + PM_SCORE <= 4:
        additional_hours = 20
        additional_result = ""
    else:
        additional_hours = 30
        additional_result = ""

    total_hours = bre_hours + app_hours + abs_hours + exh_hours + appointments_hours + kiosk_hours + additional_hours
    final_reasons = [DESCRIPTIONS[k] for k in sorted(active_keys)]

    return {
        "bre_score": bre_hours,
        "bre_classification":"",
        "app_score": app_hours,
        "app_classification": "",
        "abs_score": abs_hours,
        "abs_classification": "",
        "exh_score": exh_hours,
        "exh_classification": "",
        "appointments_score": appointments_hours,
        "appointments_classification": "",
        "kiosk_score": kiosk_hours,
        "kiosk_classification": "",
        "additional_hours": additional_hours,
        "additional_classification": "",
        "total_hours": total_hours,
        "reasons": final_reasons,
        "module_breakdowns": {
            module_key: {
                "key": module_key,
                "label": MODULE_LABELS[module_key],
                "total_hours": int(sum(per_module_buckets[module_key].values())),
                "items": [
                    {
                        "key": bucket_key,
                        "label": JUSTIFICATIONS[bucket_key],
                        "hours": int(per_module_buckets[module_key].get(bucket_key, 0)),
                    }
                    for bucket_key in JUSTIFICATIONS.keys()
                    if per_module_buckets[module_key].get(bucket_key, 0) and per_module_buckets[module_key].get(bucket_key, 0) > 0
                ],
            }
            for module_key in MODULE_LABELS.keys()
        },
        "justifications": [
            {
                "key": bucket_key,
                "label": JUSTIFICATIONS[bucket_key],
                "hours": int(per_module_buckets["bre"].get(bucket_key, 0) + per_module_buckets["app"].get(bucket_key, 0)),
            }
            for bucket_key in JUSTIFICATIONS.keys()
            if (per_module_buckets["bre"].get(bucket_key, 0) + per_module_buckets["app"].get(bucket_key, 0)) > 0
        ],
    }

FEATURE_LABELS: Dict[str, str] = {
    # Base toggles
    "bre_include": "Attendee Registration — Basic Implementation",
    "app_include": "Mobile App (Connect) and Connect Online — Basic Implementation",
    "abs_include": "Abstract / Speaker Management — Basic Implementation",
    "exh_include": "Exhibitor Registration / Booth Selection — Basic Implementation",
    "appointments_include": "Appointment Management — Basic Implementation",
    "kiosk_include": "Kiosk / Badge Printing — Basic Implementation",

    # BRE
    "workflows": "More than 3 workflows",
    "field_logic": "Complex logic for fields",
    "product_logic": "Product logic",
    "session_logic": "Session logic",
    "complex_reporting": "Custom or complex reporting needs",
    "housing": "Housing",
    "table_seating": "Table seating",
    "lookup_integration": "Lookup integration",

    # APP
    "hybrid_virtual": "Hybrid or Virtual",
    "multi_event": "Multi-Event App",
    "CEUs": "Complex CEs",
    "sponsor_branding": "Emphasis on branding or sponsorship",
    "leads": "Leads",

    # ABS
    "complex_workflows": "Complex workflows for submission",
    "multiple_review_rounds": "Multiple rounds of review",
    "multiple_proposal_calls": "Multiple calls for proposals",

    # EXH
    "floor_plan": "Floor plans",
    "year_round": "Year-Round",
    "complex_sponsors": "Complex sponsorship options",

    # Appointments
    "multi_scheduling": "Multiple types of scheduling",
    "first_time_system": "First time appointment system user",
    "matchmaking": "Matchmaking required",

    # Kiosk
    "personal_agenda": "Personal Agenda",
    "double_sided": "Double sided",
    "logic_based_badges": "Logic based badges",
    "multi_badge_types": "Multiple types of badges by attendee type",
    "customer_hardware": "Customer using their own hardware",

    # Custom + PM
    "integrations": "Integrations",
    "SSO": "SSO",
    "multiple_POCs": "Multiple POCs / Divisions",
    "recurring_calls": "Recurring Calls",
    "more_than_8_events": "More than 8 events in a calendar year",
}

MODULE_GROUPS: Dict[str, List[str]] = {
    "Attendee Registration": ["bre_include", "workflows", "field_logic", "product_logic", "session_logic", "complex_reporting", "housing", "table_seating", "lookup_integration"],
    "Mobile App (Connect) and Connect Online": ["app_include", "hybrid_virtual", "multi_event", "CEUs", "sponsor_branding", "leads"],
    "Kiosk / Badge Printing": ["kiosk_include", "personal_agenda", "double_sided", "logic_based_badges", "multi_badge_types", "customer_hardware"],
    "Exhibitor Registration / Booth Selection": ["exh_include", "floor_plan", "year_round", "complex_sponsors"],
    "Abstract / Speaker Management": ["abs_include", "complex_workflows", "multiple_review_rounds", "multiple_proposal_calls"],
    "Appointment Management": ["appointments_include", "multi_scheduling", "first_time_system", "matchmaking"],
    "Custom / Development": ["integrations", "SSO"],
    "Project Management": ["multiple_POCs", "recurring_calls", "more_than_8_events"],
}

def _smtp_send_pdf(to_email: str, subject: str, body_text: str, pdf_bytes: bytes, filename: str) -> None:
    host = SMTP_HOST
    port = int(SMTP_PORT)
    username = SMTP_USERNAME
    password = SMTP_PASSWORD
    from_addr = SMTP_FROM or username
    use_tls = SMTP_USE_TLS

    if isinstance(use_tls, str):
        use_tls = use_tls.lower() in ("1", "true", "yes", "y")

    if not host:
        raise RuntimeError("SMTP_HOST is not configured (check env.py)")

    if not from_addr:
        raise RuntimeError("SMTP_FROM is not configured (check env.py)")

    if isinstance(password, str):
        password = password.replace(" ", "").strip()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_email
    msg.set_content(body_text)
    msg.add_attachment(pdf_bytes, maintype="application", subtype="pdf", filename=filename)

    with smtplib.SMTP(host, port, timeout=20) as server:
        server.ehlo()
        if use_tls:
            server.starttls()
            server.ehlo()
        if username and password:
            server.login(username, password)

        server.send_message(msg)

def _build_print_html(customer_name: str, selected_by_module: Dict[str, List[str]], calc: Dict[str, Any]) -> str:
    scope_lines = ""
    if "justifications" in calc and isinstance(calc["justifications"], list):
        items = "".join([f"<li>{j['label']}: {j['hours']} hour{'s' if j['hours'] != 1 else ''}</li>" for j in calc["justifications"]])
        scope_lines = f"<h4>Scope Breakdown</h4><ul>{items}</ul>"
    elif "reasons" in calc and isinstance(calc["reasons"], list) and calc["reasons"]:
        items = "".join([f"<li>{r}</li>" for r in calc["reasons"]])
        scope_lines = f"<h4>Scope Justification</h4><ul>{items}</ul>"

    modules_html = ""
    for module_name, items in selected_by_module.items():
        if not items:
            continue
        lis = "".join([f"<li>{i}</li>" for i in items])
        modules_html += f"""
        <section class="module">
            <h2>{module_name}</h2>
            <ul class="checked-list">{lis}</ul>
        </section>
        """

    return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8" />
        <title>PSC Hours - {customer_name}</title>
        <style>
            body {{ font-family: Segoe UI, Arial, sans-serif; color: #111827; }}
            .header {{ border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; margin-bottom: 16px; }}
            .title {{ font-size: 14pt; font-weight: 700; }}
            .meta {{ font-size: 10pt; color: #374151; }}
            .customer {{ margin-top: 6px; font-size: 11pt; font-weight: 600; }}
            .layout {{ display: grid; grid-template-columns: 1.6fr 1fr; gap: 18px; align-items: start; }}
            .module {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; margin-bottom: 12px; break-inside: avoid; }}
            .module h2 {{ margin: 0 0 8px 0; font-size: 11pt; border-bottom: 1px solid #f3f4f6; padding-bottom: 6px; }}
            .checked-list {{ margin: 0; padding-left: 18px; }}
            .result-card {{ border: 2px solid #111827; border-radius: 8px; padding: 14px; break-inside: avoid; }}
            .row {{ margin: 6px 0; font-weight: 700; text-transform: uppercase; font-size: 10pt; }}
            .hours {{ margin-top: 10px; font-size: 12pt; font-weight: 800; }}
            h4 {{ margin: 14px 0 6px 0; font-size: 10pt; }}
            ul {{ margin: 0; padding-left: 18px; }}
        </style>
        </head>
        <body>
        <div class="header">
            <div class="title">PSC Hours Calculator</div>
            <div class="meta">{""}</div>
            <div class="customer">Customer: {customer_name}</div>
        </div>

        <div class="layout">
            <div>
            {modules_html}
            </div>

            <aside class="result-card">
            <div class="row">Attendee Registration — {calc.get('bre_score',0)} hrs</div>
            <div class="row">APP and CO — {calc.get('app_score',0)} hrs</div>
            <div class="row">Abstract — {calc.get('abs_score',0)} hrs</div>
            <div class="row">Exhibits — {calc.get('exh_score',0)} hrs</div>
            <div class="row">Appointments — {calc.get('appointments_score',0)} hrs</div>
            <div class="row">Kiosk / Badges — {calc.get('kiosk_score',0)} hrs</div>
            <div class="row">Custom / PM — {calc.get('additional_hours',0)} hrs</div>

            {scope_lines}

            <div class="hours">Total PSC Hours: {calc.get('total_hours',0)}</div>
            </aside>
        </div>
        </body>
        </html>
    """

async def _html_to_pdf_bytes(html: str) -> bytes:
    def _format_exc(e: Exception) -> str:
        msg = str(e).strip()
        if msg:
            return msg
        return repr(e)

    def _render_pdf_sync(html_content: str) -> bytes:
        # Using Playwright sync API avoids relying on the server's asyncio event loop
        # (which can be configured to a Windows selector loop and raise NotImplementedError).
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page()
                page.set_content(html_content, wait_until="load")
                return page.pdf(format="Letter", print_background=True)
            finally:
                browser.close()

    try:
        return await asyncio.to_thread(_render_pdf_sync, html)
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "Playwright is not installed in the active Python environment. "
            "Install it with: python -m pip install playwright && python -m playwright install chromium"
        ) from e
    except Exception as e:
        msg = _format_exc(e)
        if "executable" in msg.lower() and ("doesn't exist" in msg.lower() or "does not exist" in msg.lower()):
            raise RuntimeError(
                "Playwright Chromium browser binaries are not installed. "
                "Run this once in your venv: python -m playwright install chromium. "
                f"Original error: {msg}"
            ) from e
        raise

@app.post("/email")
async def email_endpoint(req: EmailRequest):
    customer = (req.customer_name or "").strip()
    if len(customer) < 2:
        raise HTTPException(status_code=400, detail="Customer name is required")

    to_email = (req.to_email or "").strip()
    _, parsed_email = parseaddr(to_email)
    if not parsed_email or "@" not in parsed_email:
        raise HTTPException(status_code=400, detail="A valid recipient email is required")

    selected_by_module: Dict[str, List[str]] = {}
    for module_name, feature_ids in MODULE_GROUPS.items():
        selected: List[str] = []
        for fid in feature_ids:
            if getattr(req.features, fid, False):
                selected.append(FEATURE_LABELS.get(fid, fid))
        selected_by_module[module_name] = selected

    calc = calculate_classification(req.features)
    html = _build_print_html(customer, selected_by_module, calc)

    try:
        pdf_bytes = await _html_to_pdf_bytes(html)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed ({type(e).__name__}): {e!r}",
        )

    subject = f"PSC Hours Calculator - {customer}"
    body = f"Attached are the PSC Hours Calculator results for {customer}."

    try:
        _smtp_send_pdf(parsed_email, subject, body, pdf_bytes, f"PSC_Hours_{customer}.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email send failed: {e}")

    return {"ok": True}


@app.post("/pdf")
async def pdf_endpoint(req: PdfRequest):
    customer = (req.customer_name or "").strip()
    if len(customer) < 2:
        raise HTTPException(status_code=400, detail="Customer name is required")

    selected_by_module: Dict[str, List[str]] = {}
    for module_name, feature_ids in MODULE_GROUPS.items():
        selected: List[str] = []
        for fid in feature_ids:
            if getattr(req.features, fid, False):
                selected.append(FEATURE_LABELS.get(fid, fid))
        selected_by_module[module_name] = selected

    calc = calculate_classification(req.features)
    html = _build_print_html(customer, selected_by_module, calc)

    try:
        pdf_bytes = await _html_to_pdf_bytes(html)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed ({type(e).__name__}): {e!r}",
        )

    filename = f"PSC_Hours_{customer}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=\"{filename}\""},
    )