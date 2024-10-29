

document.getElementById('rent').addEventListener('click', function() {
    document.getElementById('post_type').value = 'rent';
    this.classList.add('active');
    document.getElementById('sale').classList.remove('active');
});

document.getElementById('sale').addEventListener('click', function() {
    document.getElementById('post_type').value = 'sale';
    this.classList.add('active');
    document.getElementById('rent').classList.remove('active');
});

// Toggle button functionality for "property_type"
document.getElementById('residential').addEventListener('click', function() {
    document.getElementById('property_type1').value = 'residential';
    this.classList.add('active');
    document.getElementById('commercial').classList.remove('active');
    document.getElementById('residential-options').classList.remove('d-none');
    document.getElementById('commercial-options').classList.add('d-none');
    document.getElementById('balconies-group').classList.add('d-none');
    document.getElementById('bedrooms-group').classList.add('d-none');
});

document.getElementById('commercial').addEventListener('click', function() {
    document.getElementById('property_type1').value = 'commercial';
    this.classList.add('active');
    document.getElementById('residential').classList.remove('active');
    document.getElementById('residential-options').classList.add('d-none');
    document.getElementById('commercial-options').classList.remove('d-none');
});

document.getElementById('apartment').addEventListener('click', function() {
    document.getElementById('specific_type1').value = 'apartment';
    this.classList.add('active');
    document.getElementById('villa').classList.remove('active');
    document.getElementById('builder-floor').classList.remove('active');
    document.getElementById('res-new-project').classList.remove('active');
    document.getElementById('weekend-homes').classList.remove('active');
});

document.getElementById('villa').addEventListener('click', function() {
    document.getElementById('specific_type1').value = 'villa';
    this.classList.add('active');
    document.getElementById('apartment').classList.remove('active');
    document.getElementById('builder-floor').classList.remove('active');
    document.getElementById('res-new-project').classList.remove('active');
    document.getElementById('weekend-homes').classList.remove('active');
});
document.getElementById('builder-floor').addEventListener('click', function() {
    document.getElementById('specific_type1').value = 'builder-floor';
    this.classList.add('active');
    document.getElementById('villa').classList.remove('active');
    document.getElementById('apartment').classList.remove('active');
    document.getElementById('res-new-project').classList.remove('active');
    document.getElementById('weekend-homes').classList.remove('active');
});
document.getElementById('res-new-project').addEventListener('click', function() {
    document.getElementById('specific_type1').value = 'res-new-project';
    this.classList.add('active');
    document.getElementById('villa').classList.remove('active');
    document.getElementById('builder-floor').classList.remove('active');
    document.getElementById('apartment').classList.remove('active');
    document.getElementById('weekend-homes').classList.remove('active');
});
document.getElementById('weekend-homes').addEventListener('click', function() {
    document.getElementById('specific_type1').value = 'weekend-homes';
    this.classList.add('active');
    document.getElementById('villa').classList.remove('active');
    document.getElementById('builder-floor').classList.remove('active');
    document.getElementById('res-new-project').classList.remove('active');
    document.getElementById('apartment').classList.remove('active');
});
document.getElementById('office').addEventListener('click', function() {
    document.getElementById('specific_type2').value = 'office';
    this.classList.add('active');
    document.getElementById('retail').classList.remove('active');
    document.getElementById('com-new-project').classList.remove('active');
});
document.getElementById('retail').addEventListener('click', function() {
    document.getElementById('specific_type2').value = 'retail';
    this.classList.add('active');
    document.getElementById('office').classList.remove('active');
    document.getElementById('com-new-project').classList.remove('active');
    
});
document.getElementById('com-new-project').addEventListener('click', function() {
    document.getElementById('specific_type2').value = 'com-new-project';
    this.classList.add('active');
    document.getElementById('retail').classList.remove('active');
    document.getElementById('office').classList.remove('active');
});

document.getElementById('owner').addEventListener('click', function() {
    document.getElementById('poster').value = 'owner';
    this.classList.add('active');
    document.getElementById('agent').classList.remove('active');
});

document.getElementById('agent').addEventListener('click', function() {
    document.getElementById('poster').value = 'agent';
    this.classList.add('active');
    document.getElementById('owner').classList.remove('active');
});






// General function to handle dropdown selections
function setupDropdown(dropdownGroupId, hiddenInputId) {
    // Select all dropdown items within the specified dropdown group
    document.querySelectorAll(`#${dropdownGroupId} .dropdown-item`).forEach(function(item) {
        item.addEventListener('click', function(event) {
            // Prevent default action
            event.preventDefault();
            
            // Get the selected value from the item text
            const selectedValue = this.textContent;
            
            // Update the hidden input field value
            document.getElementById(hiddenInputId).value = selectedValue;
            
            // Update the dropdown toggle text to show the selected value
            document.querySelector(`#${dropdownGroupId} .dropdown-toggle span`).textContent = selectedValue;
            
            // Add active class to the selected item and remove from others
            document.querySelectorAll(`#${dropdownGroupId} .dropdown-item`).forEach(function(el) {
                el.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
}

// Setup dropdowns for all groups
setupDropdown('bedrooms-group', 'bedrooms-count'); // For bedrooms
setupDropdown('bathrooms-group', 'bathrooms-count'); // Replace with actual IDs
setupDropdown('balconies-group', 'balconies-count'); // Replace with actual IDs
setupDropdown('availibility-group', 'status'); // Replace with actual IDs
