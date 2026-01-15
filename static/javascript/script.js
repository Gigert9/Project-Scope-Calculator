const isChecked = (id) => {
    const el = document.getElementById(id);
    return el ? el.checked : false;
};

async function updateClassification() {
    // console.log("Updating classification..."); // Debug log

    const projectData = {
        // Module Toggles
        bre_include: isChecked('bre_include'),
        app_include: isChecked('app_include'),
        abs_include: isChecked('abs_include'),
        exh_include: isChecked('exh_include'),
        appointments_include: isChecked('appointments_include'),
        kiosk_include: isChecked('kiosk_include'),

        // Sub-features
        workflows: isChecked('workflows'), 
        field_logic: isChecked('field_logic'),
        product_logic: isChecked('product_logic'),
        session_logic: isChecked('session_logic'),
        complex_reporting: isChecked('complex_reporting'),
        housing: isChecked('housing'),
        table_seating: isChecked('table_seating'),
        lookup_integration: isChecked('lookup_integration'),
        hybrid_virtual: isChecked('hybrid_virtual'),
        multi_event: isChecked('multi_event'),
        CEUs: isChecked('CEUs'),
        sponsor_branding: isChecked('sponsor_branding'),
        leads: isChecked('leads'),
        complex_workflows: isChecked('complex_workflows'),
        multiple_review_rounds: isChecked('multiple_review_rounds'),
        multiple_proposal_calls: isChecked('multiple_proposal_calls'),
        floor_plan: isChecked('floor_plan'),
        year_round: isChecked('year_round'),
        complex_sponsors: isChecked('complex_sponsors'),
        multi_scheduling: isChecked('multi_scheduling'),
        first_time_system: isChecked('first_time_system'),
        matchmaking: isChecked('matchmaking'),
        personal_agenda: isChecked('personal_agenda'),
        double_sided: isChecked('double_sided'),
        logic_based_badges: isChecked('logic_based_badges'),
        multi_badge_types: isChecked('multi_badge_types'),
        customer_hardware: isChecked('customer_hardware'),
        integrations: isChecked('integrations'),
        SSO: isChecked('SSO'),
        multiple_POCs: isChecked('multiple_POCs'),
        recurring_calls: isChecked('recurring_calls'),
        more_than_8_events: isChecked('more_than_8_events')
    };

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify(projectData),
        });

        if (!response.ok) throw new Error('Network response was not ok');
        const result = await response.json();

        const reasonsContainer = document.getElementById('reasons-container');
        const reasonsList = document.getElementById('reasons-list');
        reasonsList.innerHTML = '';

        if (result.reasons && result.reasons.length > 0) {
            reasonsContainer.style.display = 'block';
            
            result.reasons.forEach(reason => {
                const li = document.createElement('li');
                li.textContent = reason;
                reasonsList.appendChild(li);
            });
        } else {
            reasonsContainer.style.display = 'none';
        }

        const updateModuleUI = (prefix, label, score, classification) => {
            const classEl = document.getElementById(`${prefix}-classification`);
            const scoreEl = document.getElementById(`${prefix}-score`);

            if (classification === 'N/A' || !classification) {
                classEl.innerText = '';
                scoreEl.innerText = '';
            } else {
                classEl.innerText = `${label} Classification: ${classification}`;
                scoreEl.innerText = `${label} Hours: ${score}`;
            }
        };

        updateModuleUI('bre', 'Attendee Registration', result.bre_score, result.bre_classification);
        updateModuleUI('app', 'APP and CO', result.app_score, result.app_classification);
        updateModuleUI('abs', 'Abstract', result.abs_score, result.abs_classification);
        updateModuleUI('exh', 'Exhibits', result.exh_score, result.exh_classification);
        updateModuleUI('appointments', 'Appointments', result.appointments_score, result.appointments_classification);
        updateModuleUI('kiosk', 'Kiosk/Badges', result.kiosk_score, result.kiosk_classification);
        updateModuleUI('additional', 'Custom / PM', result.additional_hours, result.additional_classification);
        
        document.getElementById('total-hours').innerText = `Total PSC Hours: ${result.total_hours}`;
    } catch (error) {
        console.error('Error:', error);
    }
}

function toggleModule(includeCheckboxId, targetContainerId) {
    const includeCheckbox = document.getElementById(includeCheckboxId);
    const container = document.getElementById(targetContainerId);

    if (!includeCheckbox || !container) return;

    container.style.display = includeCheckbox.checked ? 'block' : 'none';

    if (!includeCheckbox.checked) {
        container.querySelectorAll('input[type="checkbox"]').forEach(box => {
            box.checked = false;
        });
    }
    updateClassification();
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateClassification);
    });

    const moduleToggles = [
        { check: 'bre_include', feat: 'bre-features' },
        { check: 'app_include', feat: 'app-features' },
        { check: 'abs_include', feat: 'abs-features' },
        { check: 'exh_include', feat: 'exh-features' },
        { check: 'appointments_include', feat: 'appointment-features' },
        { check: 'kiosk_include', feat: 'kiosk-features' }
    ];

    moduleToggles.forEach(t => {
        const el = document.getElementById(t.check);
        if (el) {
            el.addEventListener('change', () => toggleModule(t.check, t.feat));
        }
    });

    document.getElementById('reset-btn').addEventListener('click', () => {
        document.querySelectorAll('input[type="checkbox"]').forEach(box => box.checked = false);
        document.querySelectorAll('[id$="-features"]').forEach(span => span.style.display = 'none');

        document.getElementById('reasons-container').style.display = 'none';
        document.getElementById('reasons-list').innerHTML = '';
        
        const sections = ['bre', 'app', 'abs', 'exh', 'appointments', 'kiosk', 'additional'];
        sections.forEach(s => {
            document.getElementById(`${s}-classification`).innerText = s === 'bre' ? "Waiting for selection..." : "";
            document.getElementById(`${s}-score`).innerText = "";
        });
        document.getElementById('total-hours').innerText = '';
    });
});