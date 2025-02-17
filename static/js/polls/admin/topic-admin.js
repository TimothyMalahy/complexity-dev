document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.js-inline-admin-formset.inline-group').forEach(function(element) {
        const heading = element.querySelector('h2');
        if (heading) {
            const label = heading.innerHTML.trim();
            wrapInDetails(element, label);
        }
    });

    function wrapInDetails(element, label) {
        const details = document.createElement('details');
        const summary = document.createElement('summary');
        summary.innerHTML = label;
        details.appendChild(summary);
        element.parentElement.insertBefore(details, element);
        details.appendChild(element);
    }
});

