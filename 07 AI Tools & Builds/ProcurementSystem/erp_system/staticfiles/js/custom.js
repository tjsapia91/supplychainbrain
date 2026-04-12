/* Michael Todd Beauty ERP - Custom JavaScript */

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirm before destructive actions
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-confirm]').forEach(function(el) {
        el.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
});

// PPO Line Item dynamic formset management
function initLineItemFormset() {
    const addBtn = document.getElementById('add-line-item');
    if (!addBtn) return;

    addBtn.addEventListener('click', function() {
        const totalForms = document.getElementById('id_lines-TOTAL_FORMS');
        if (!totalForms) return;

        const currentCount = parseInt(totalForms.value);
        const emptyForm = document.getElementById('empty-form-template');
        if (!emptyForm) return;

        const newForm = emptyForm.innerHTML.replace(/__prefix__/g, currentCount);
        const tbody = document.getElementById('line-items-body');
        tbody.insertAdjacentHTML('beforeend', newForm);
        totalForms.value = currentCount + 1;

        // Update line numbers
        updateLineNumbers();
    });
}

function removeLineItem(btn) {
    const row = btn.closest('tr');
    const deleteCheckbox = row.querySelector('input[type="checkbox"][name$="-DELETE"]');
    if (deleteCheckbox) {
        deleteCheckbox.checked = true;
        row.style.display = 'none';
    } else {
        row.remove();
        const totalForms = document.getElementById('id_lines-TOTAL_FORMS');
        if (totalForms) {
            totalForms.value = parseInt(totalForms.value) - 1;
        }
    }
    updateLineNumbers();
}

function updateLineNumbers() {
    const rows = document.querySelectorAll('#line-items-body tr:not([style*="display: none"])');
    rows.forEach(function(row, index) {
        const lineNumInput = row.querySelector('input[name$="-line_number"]');
        if (lineNumInput) {
            lineNumInput.value = index + 1;
        }
    });
}

// Item search autocomplete for PPO line items
function initItemSearch() {
    document.addEventListener('change', function(e) {
        if (e.target && e.target.name && e.target.name.includes('-item')) {
            const itemId = e.target.value;
            if (!itemId) return;

            fetch(`/procurement/api/items/${itemId}/`)
                .then(response => response.json())
                .then(data => {
                    const row = e.target.closest('tr');
                    if (!row) return;

                    const descInput = row.querySelector('input[name$="-description"]');
                    if (descInput && !descInput.value) {
                        descInput.value = data.description || '';
                    }
                })
                .catch(err => console.log('Item lookup error:', err));
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initLineItemFormset();
    initItemSearch();
});
