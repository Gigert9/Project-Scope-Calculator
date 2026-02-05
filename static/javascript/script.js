const isChecked = (id) => {
    const el = document.getElementById(id);
    return el ? el.checked : false;
};

const getValue = (id) => {
    const el = document.getElementById(id);
    return el ? el.value : '';
};

function buildProjectData() {
    return {
        bre_include: isChecked('bre_include'),
        app_include: isChecked('app_include'),
        abs_include: isChecked('abs_include'),
        exh_include: isChecked('exh_include'),
        appointments_include: isChecked('appointments_include'),
        kiosk_include: isChecked('kiosk_include'),

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
    };
}

function syncPrintHeader() {
    const name = (getValue('customer-name') || '').trim();
    const namePrint = document.getElementById('customer-name-print');
    if (namePrint) namePrint.textContent = name;

    const dateEl = document.getElementById('print-date');
    if (dateEl) {
        const now = new Date();
        dateEl.textContent = now.toLocaleString();
    }
}

function requireCustomerName() {
    const input = document.getElementById('customer-name');
    if (!input) return true;

    // Uses native browser validation UI
    if (!input.checkValidity()) {
        input.reportValidity();
        input.focus();
        return false;
    }
    return true;
}

function setEmailStatus(text) {
    const el = document.getElementById('email-status');
    if (el) el.textContent = text || '';
}

async function openServerPdf() {
    if (!requireCustomerName()) return;

    const customerName = (getValue('customer-name') || '').trim();
    const payload = {
        customer_name: customerName,
        features: buildProjectData()
    };

    setEmailStatus('Preparing PDF…');

    // Open a window synchronously to avoid popup blockers.
    const pdfWindow = window.open('', '_blank');
    if (pdfWindow) {
        try {
            pdfWindow.document.title = 'Preparing PDF…';
            pdfWindow.document.body.innerHTML = '<p style="font-family:Segoe UI,Arial,sans-serif; padding:16px;">Preparing PDF…</p>';
        } catch {
            // ignore
        }
    }

    let objectUrl = '';
    try {
        const response = await fetch('pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            let detail = '';
            try {
                detail = await response.text();
            } catch {
                detail = '';
            }
            throw new Error(detail || `PDF failed (${response.status})`);
        }

        const blob = await response.blob();
        objectUrl = URL.createObjectURL(blob);

        if (pdfWindow) {
            pdfWindow.location = objectUrl;
        } else {
            const a = document.createElement('a');
            a.href = objectUrl;
            a.target = '_blank';
            a.download = `PSC_Hours_${customerName || 'Results'}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        }

        setEmailStatus('');
    } catch (err) {
        console.error(err);
        if (pdfWindow) {
            try { pdfWindow.close(); } catch { /* ignore */ }
        }
        const msg = String(err && (err.message || err) ? (err.message || err) : 'PDF failed');
        if (msg.includes('NetworkError') || msg.includes('Failed to fetch') || msg.includes('Load failed')) {
            setEmailStatus('PDF error: Could not reach the server. Confirm the app is running and you are using http://127.0.0.1:8010/ (not a static file or Live Server).');
        } else {
            setEmailStatus(`PDF error: ${msg}`);
        }
    } finally {
        if (objectUrl) {
            setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
        }
    }
}

async function updateClassification() {
    const projectData = buildProjectData();

    try {
        const response = await fetch('calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData),
        });

        if (!response.ok) throw new Error('Network response was not ok');
        const result = await response.json();

        const reasonsContainer = document.getElementById('reasons-container');
        const reasonsList = document.getElementById('reasons-list');
        if (reasonsList) reasonsList.innerHTML = '';

        const moduleBreakdowns = result.module_breakdowns || null;

        if (moduleBreakdowns && typeof moduleBreakdowns === 'object') {
            const entries = Object.values(moduleBreakdowns)
                .filter(m => m && m.total_hours && m.total_hours > 0);

            if (entries.length > 0) {
                reasonsContainer.style.display = 'block';

                entries.forEach(m => {
                    const headerLi = document.createElement('li');
                    headerLi.innerHTML = `<strong>${m.label}</strong> — ${m.total_hours} hour${m.total_hours === 1 ? '' : 's'}`;
                    reasonsList.appendChild(headerLi);

                    if (Array.isArray(m.items) && m.items.length > 0) {
                        m.items.forEach(item => {
                            if (!item || !item.hours || item.hours <= 0) return;
                            const li = document.createElement('li');
                            li.textContent = `${item.label}: ${item.hours} hour${item.hours === 1 ? '' : 's'}`;
                            li.classList.add('sub-item');
                            reasonsList.appendChild(li);
                        });
                    }
                });
            } else {
                reasonsContainer.style.display = 'none';
            }
        } else if (result.justifications && Array.isArray(result.justifications) && result.justifications.length > 0) {
            reasonsContainer.style.display = 'block';
            result.justifications.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.label}: ${item.hours} hour${item.hours === 1 ? '' : 's'}`;
                reasonsList.appendChild(li);
            });
        } else if (result.reasons && result.reasons.length > 0) {
            reasonsContainer.style.display = 'block';
            result.reasons.forEach(reason => {
                const li = document.createElement('li');
                li.textContent = reason;
                reasonsList.appendChild(li);
            });
        } else {
            reasonsContainer.style.display = 'none';
        }

        const updateModuleUI = (prefix, label, hours) => {
            const classEl = document.getElementById(`${prefix}-classification`);
            const scoreEl = document.getElementById(`${prefix}-score`);

            if (classEl) classEl.innerText = '';

            if (!hours || hours === 0) {
                scoreEl.innerText = '';
            } else {
                scoreEl.innerText = `${label} Hours: ${hours}`;
            }
        };

        updateModuleUI('bre', 'Attendee Registration', result.bre_score);
        updateModuleUI('app', 'APP and CO', result.app_score);
        updateModuleUI('abs', 'Abstract', result.abs_score);
        updateModuleUI('exh', 'Exhibits', result.exh_score);
        updateModuleUI('appointments', 'Appointments', result.appointments_score);
        updateModuleUI('kiosk', 'Kiosk / Badges', result.kiosk_score);

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

async function emailResults() {
    if (!requireCustomerName()) return;

    const toEmail = (getValue('recipient-email') || '').trim() || prompt('Send results to what email address?');
    if (!toEmail) return;

    setEmailStatus('Sending email…');

    const payload = {
        to_email: toEmail,
        customer_name: (getValue('customer-name') || '').trim(),
        features: buildProjectData()
    };

    try {
        const response = await fetch('email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        let detail = '';
        try {
            const data = await response.json();
            detail = (data && data.detail) ? String(data.detail) : '';
        } catch {
            try {
                detail = await response.text();
            } catch {
                detail = '';
            }
        }

        if (!response.ok) {
            throw new Error(detail || `Email failed (${response.status})`);
        }

        setEmailStatus('Email sent.');
        setTimeout(() => setEmailStatus(''), 4000);
    } catch (err) {
        console.error(err);
        const msg = String(err && (err.message || err) ? (err.message || err) : 'Email failed');
        if (msg.includes('NetworkError') || msg.includes('Failed to fetch') || msg.includes('Load failed')) {
            setEmailStatus('Email error: Could not reach the server. Confirm the app is running and you are using http://127.0.0.1:8010/ (not a static file or Live Server).');
        } else {
            setEmailStatus(`Email error: ${msg}`);
        }
    }
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
        if (el) el.addEventListener('change', () => toggleModule(t.check, t.feat));
    });

    const nameInput = document.getElementById('customer-name');
    if (nameInput) nameInput.addEventListener('input', syncPrintHeader);
    syncPrintHeader();

    const printBtn = document.getElementById('print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', openServerPdf);
    }

    const emailBtn = document.getElementById('email-btn');
    if (emailBtn) emailBtn.addEventListener('click', emailResults);

    document.getElementById('reset-btn').addEventListener('click', () => {
        document.querySelectorAll('input[type="checkbox"]').forEach(box => box.checked = false);
        document.querySelectorAll('[id$="-features"]').forEach(span => span.style.display = 'none');

        document.getElementById('reasons-container').style.display = 'none';
        document.getElementById('reasons-list').innerHTML = '';

        const sections = ['bre', 'app', 'abs', 'exh', 'appointments', 'kiosk'];
        sections.forEach(s => {
            document.getElementById(`${s}-classification`).innerText = s === 'bre' ? "Waiting for selection..." : "";
            document.getElementById(`${s}-score`).innerText = "";
        });

        document.getElementById('total-hours').innerText = '';
        setEmailStatus('');
        if (nameInput) nameInput.value = '';
        const emailInput = document.getElementById('recipient-email');
        if (emailInput) emailInput.value = '';
        syncPrintHeader();
    });
});