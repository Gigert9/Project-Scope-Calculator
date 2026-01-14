async function updateClassification() {
    const projectData = {
        workflows: document.getElementById('workflows').checked, 
        field_logic: document.getElementById('field_logic').checked,
        product_logic: document.getElementById('product_logic').checked,
        session_logic: document.getElementById('session_logic').checked,
        complex_reporting: document.getElementById('complex_reporting').checked,
        housing: document.getElementById('housing').checked,
        table_seating: document.getElementById('table_seating').checked,
        lookup_integration: document.getElementById('lookup_integration').checked,
        hybrid_virtual: document.getElementById('hybrid_virtual').checked,
        multi_event: document.getElementById('multi_event').checked,
        wayfinding: document.getElementById('wayfinding').checked,
        CEUs: document.getElementById('CEUs').checked,
        sponsor_branding: document.getElementById('sponsor_branding').checked,
        leads: document.getElementById('leads').checked,
        complex_workflows: document.getElementById('complex_workflows').checked,
        multiple_review_rounds: document.getElementById('multiple_review_rounds').checked,
        multiple_proposal_calls: document.getElementById('multiple_proposal_calls').checked,
        floor_plan: document.getElementById('floor_plan').checked,
        year_round: document.getElementById('year_round').checked,
        complex_sponsors: document.getElementById('complex_sponsors').checked,
        multi_scheduling: document.getElementById('multi_scheduling').checked,
        first_time_system: document.getElementById('first_time_system').checked,
        matchmaking: document.getElementById('matchmaking').checked,
        personal_agenda: document.getElementById('personal_agenda').checked,
        double_sided: document.getElementById('double_sided').checked,
        logic_based_badges: document.getElementById('logic_based_badges').checked,
        multi_badge_types: document.getElementById('multi_badge_types').checked,
        customer_hardware: document.getElementById('customer_hardware').checked,
        new_dev: document.getElementById('new_dev').checked,
        integrations: document.getElementById('integrations').checked,
        SSO: document.getElementById('SSO').checked,
        multiple_POCs: document.getElementById('multiple_POCs').checked,
        recurring_calls: document.getElementById('recurring_calls').checked,
        more_than_8_events: document.getElementById('more_than_8_events').checked,
        bre_noscope: document.getElementById('bre_noscope').checked,
        app_noscope: document.getElementById('app_noscope').checked,
        abs_noscope: document.getElementById('abs_noscope').checked,
        exh_noscope: document.getElementById('exh_noscope').checked,
        appointments_noscope: document.getElementById('appointments_noscope').checked,
        kiosk_noscope: document.getElementById('kiosk_noscope').checked
    };

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }, 
            body: JSON.stringify(projectData),
        });

        if (!response.ok) throw new Error('Network response was not ok');
        const result = await response.json();

        const updateModuleUI = (prefix, label, score, classification) => {
            const classEl = document.getElementById(`${prefix}-classification`);
            const scoreEl = document.getElementById(`${prefix}-score`);

            if (classification === 'N/A') {
                classEl.innerText = '';
                scoreEl.innerText = '';
            } else {
                classEl.innerText = `${label} Classification: ${classification}`;
                scoreEl.innerText = `${label} Hours: ${score}`;
            }
        };

        // Update all sections
        updateModuleUI('bre', 'Attendee Registration', result.bre_score, result.bre_classification);
        updateModuleUI('app', 'APP and CO', result.app_score, result.app_classification);
        updateModuleUI('abs', 'Abstract', result.abs_score, result.abs_classification);
        updateModuleUI('exh', 'Exhibits', result.exh_score, result.exh_classification);
        updateModuleUI('appointments', 'Appointments', result.appointments_score, result.appointments_classification);
        updateModuleUI('kiosk', 'Kiosk/Badges', result.kiosk_score, result.kiosk_classification);
        updateModuleUI('additional', 'Custom / PM', result.additional_hours, result.additional_classification)
        // Update Total
        document.getElementById('total-hours').innerText = `Total PSC Hours: ${result.total_hours}`;
    } catch (error) {
        console.error('Error:', error);
    }
}

function hideSection(checkboxId, targetContainerId) {
    const checkbox = document.getElementById(checkboxId);
    const container = document.getElementById(targetContainerId);

    container.hidden = checkbox.checked;

    if (checkbox.checked) {
        container.querySelectorAll('input[type="checkbox"]').forEach(box => box.checked = false);
    }
}

document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', updateClassification);
});

document.getElementById('bre_noscope').addEventListener('change', () => {
    hideSection('bre_noscope', 'bre-features');
    updateClassification();
});

document.getElementById('app_noscope').addEventListener('change', () => {
    hideSection('app_noscope', 'app-features');
    updateClassification();
});

document.getElementById('abs_noscope').addEventListener('change', () => {
    hideSection('abs_noscope', 'abs-features');
    updateClassification();
});

document.getElementById('exh_noscope').addEventListener('change', () => {
    hideSection('exh_noscope', 'exh-features');
    updateClassification();
});

document.getElementById('appointments_noscope').addEventListener('change', () => {
    hideSection('appointments_noscope', 'appointment-features');
    updateClassification();
});

document.getElementById('kiosk_noscope').addEventListener('change', () => {
    hideSection('kiosk_noscope', 'kiosk-features');
    updateClassification();
});

document.getElementById('reset-btn').addEventListener('click', () => {
    document.querySelectorAll('input[type="checkbox"]').forEach(box => {
        box.checked = false;
    });

    document.getElementById('bre-classification').innerText = "Waiting for selection...";
    document.getElementById('bre-score').innerText = "";

    document.getElementById('total-hours').innerText = '';

    document.querySelectorAll('[id$="-features"]').forEach(container => {
        container.hidden = false;
    })
    
    const scores = ['app', 'abs', 'exh', 'appointments', 'kiosk', 'additional'];
    scores.forEach(s => {
        document.getElementById(`${s}-score`).innerText = "";
        document.getElementById(`${s}-classification`).innerText = "";
    });
});