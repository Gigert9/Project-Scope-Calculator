from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

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
    wayfinding: bool = False
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
    new_dev: bool = False
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

@app.get("/")
def index():
    return FileResponse('html/index.html')

@app.post("/calculate")
def calculate_classification(features: ProjectFeatures):
    BRE_SCORE = 0
    APP_SCORE = 0
    ABS_SCORE = 0
    EXH_SCORE = 0
    APPOINTMENTS_SCORE = 0
    KIOSK_SCORE = 0
    CUSTOM_SCORE = 0
    PM_SCORE = 0
    
    ## ATTENDEE REGISTRATION
    if features.workflows: BRE_SCORE += 0.5
    if features.field_logic: BRE_SCORE += 2
    if features.product_logic: BRE_SCORE += 2
    if features.session_logic: BRE_SCORE += 2
    if features.complex_reporting: BRE_SCORE += 3
    if features.housing: BRE_SCORE += 2
    if features.table_seating: BRE_SCORE += 2
    if features.lookup_integration: BRE_SCORE += 0.5
    ## APP and CO 
    if features.hybrid_virtual: APP_SCORE += 1
    if features.multi_event: APP_SCORE += 1
    if features.wayfinding: APP_SCORE += 1
    if features.CEUs: APP_SCORE += 1
    if features.sponsor_branding: APP_SCORE += 1
    if features.leads: APP_SCORE += 1
    ## ABSTRACT
    if features.complex_workflows: ABS_SCORE += 1
    if features.multiple_review_rounds: ABS_SCORE += 1
    if features.multiple_proposal_calls: ABS_SCORE += 1
    ## EXHIBITOR REGISTRATION
    if features.floor_plan: EXH_SCORE += 1
    if features.year_round: EXH_SCORE += 1
    if features.complex_sponsors: EXH_SCORE += 1
    ## APPOINTMENTS
    if features.multi_scheduling: APPOINTMENTS_SCORE += 1
    if features.first_time_system: APPOINTMENTS_SCORE += 1
    if features.matchmaking: APPOINTMENTS_SCORE += 1
    ## KIOSK/BADGES
    if features.personal_agenda: KIOSK_SCORE += 1
    if features.double_sided: KIOSK_SCORE += 1
    if features.logic_based_badges: KIOSK_SCORE += 1
    if features.multi_badge_types: KIOSK_SCORE += 1
    if features.customer_hardware: KIOSK_SCORE += 1
    ## CUSTOM
    if features.new_dev: CUSTOM_SCORE += 1
    if features.integrations: CUSTOM_SCORE += 1
    if features.SSO: CUSTOM_SCORE += 1
    ## PROJECT MANAGEMENT
    if features.multiple_POCs: PM_SCORE += 1
    if features.recurring_calls: PM_SCORE += 1
    if features.more_than_8_events: PM_SCORE += 1

    if not features.bre_include: 
        bre_hours = 0
        BRE_result = "N/A"
    else:
        if BRE_SCORE <= 0:
            BRE_result = "Low"
            bre_hours = 10
        elif BRE_SCORE <= 5:
            BRE_result = "Medium"
            bre_hours = 25
        elif BRE_SCORE <= 7:
            BRE_result = "High"
            bre_hours = 50
        else:
            BRE_result = "Extreme"
            bre_hours = 100

    if not features.app_include:
        app_hours = 0
        APP_result = "N/A"
    else:
        if APP_SCORE <= 0:
            APP_result = "Low"
            app_hours = 5
        elif APP_SCORE <= 2:
            APP_result = "Medium"
            app_hours = 10
        elif APP_SCORE <= 4:
            APP_result = "High"
            app_hours = 25
        else:
            APP_result = "Extreme"
            app_hours = 50

    if not features.abs_include:
        abs_hours = 0
        ABS_result = "N/A"
    else:
        if ABS_SCORE <= 0:
            ABS_result = "Low"
            abs_hours = 5
        elif ABS_SCORE <= 1:
            ABS_result = "Medium"
            abs_hours = 10
        elif ABS_SCORE <= 2:
            ABS_result = "High"
            abs_hours = 15
        else:
            ABS_result = "Extreme"
            abs_hours = 30

    if not features.exh_include:
        exh_hours = 0
        EXH_result = "N/A"
    else:
        if EXH_SCORE <= 0:
            EXH_result = "Low"
            exh_hours = 5
        elif EXH_SCORE <= 1:
            EXH_result = "Medium"
            exh_hours = 10
        elif EXH_SCORE <= 2:
            EXH_result = "High"
            exh_hours = 20
        else:
            EXH_result = "Extreme"
            exh_hours = 40

    if not features.appointments_include:
        appointments_hours = 0
        APPOINTMENTS_result = "N/A"
    else:
        if APPOINTMENTS_SCORE <= 0:
            APPOINTMENTS_result = "Low"
            appointments_hours = 5
        elif APPOINTMENTS_SCORE <= 1:
            APPOINTMENTS_result = "Medium"
            appointments_hours = 10
        elif APPOINTMENTS_SCORE <= 2:
            APPOINTMENTS_result = "High"
            appointments_hours = 25
        else:
            APPOINTMENTS_result = "Extreme"
            appointments_hours = 50

    if not features.kiosk_include:
        kiosk_hours = 0
        KIOSK_result = "N/A"
    else:
        if KIOSK_SCORE <= 0:
            KIOSK_result = "Low"
            kiosk_hours = 5
        elif KIOSK_SCORE <= 1:
            KIOSK_result = "Medium"
            kiosk_hours = 10
        elif KIOSK_SCORE <= 2:
            KIOSK_result = "High"
            kiosk_hours = 15
        else:
            KIOSK_result = "Extreme"
            kiosk_hours = 30

    if CUSTOM_SCORE + PM_SCORE == 0:
        additional_hours = 0
        additional_result = "None"
    elif CUSTOM_SCORE + PM_SCORE <= 2:
        additional_hours = 15
        additional_result = "Medium"
    elif CUSTOM_SCORE + PM_SCORE <= 4:
        additional_hours = 20
        additional_result = "High"
    else:
        additional_hours = 30
        additional_result = "Extreme"


    total_hours = bre_hours + app_hours + abs_hours + exh_hours + appointments_hours + kiosk_hours + additional_hours

    return {
        "bre_score": bre_hours,
        "bre_classification": BRE_result,
        "app_score": app_hours,
        "app_classification": APP_result,
        "abs_score": abs_hours,
        "abs_classification": ABS_result,
        "exh_score": exh_hours,
        "exh_classification": EXH_result,
        "appointments_score": appointments_hours,
        "appointments_classification": APPOINTMENTS_result,
        "kiosk_score": kiosk_hours,
        "kiosk_classification": KIOSK_result,
        "additional_hours": additional_hours,
        "additional_classification": additional_result,
        "total_hours": total_hours
    }