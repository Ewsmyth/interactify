document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (confirm('Are you sure you want to delete this post?')) {
            e.target.submit();
        }
    });
});

// Function to show the custom pop-up menu
function showPopup(event, columnIndex) {
    event.preventDefault();
    var popupMenu = document.getElementById("popup-menu");
    var th = event.target.closest('th'); // Get the closest th element
    var h1 = th.querySelector('h1'); // Get the h1 element inside the th
    var title = h1.innerText; // Get the text content of the h1 element
    var popupTitle = popupMenu.querySelector('.popup-title'); // Get the p element for title
    popupTitle.innerText = title; // Update the text content with the title
    popupMenu.style.left = event.pageX + 'px';
    popupMenu.style.top = event.pageY + 'px';
    popupMenu.style.display = 'block';
    popupMenu.dataset.columnIndex = columnIndex;
}


// Function to hide the custom pop-up menu
document.addEventListener('click', function(event) {
    var popupMenu = document.getElementById("popup-menu");
    if (!event.target.closest('#popup-menu') && !event.target.closest('th')) {
        popupMenu.style.display = 'none';
    }
});

// Function to parse datetime string into Date object
function parseDateTime(dateTimeString) {
    // Regular expression to match datetime string
    var regex = /^(\w{3}) (\d{1,2}), (\d{4}): (\d{2}):(\d{2})$/;

    // Extract date and time components using regular expression
    var match = dateTimeString.match(regex);
    if (!match) {
        return null; // Return null if datetime string doesn't match expected format
    }

    var month = match[1];
    var day = parseInt(match[2], 10);
    var year = parseInt(match[3], 10);
    var hours = parseInt(match[4], 10);
    var minutes = parseInt(match[5], 10);

    // Convert month abbreviation to number
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var monthNumber = monthNames.indexOf(month);

    // Construct and return Date object
    return new Date(year, monthNumber, day, hours, minutes);
}

// Function to sort the table based on the selected order
function sortTable(order) {

    var columnIndex = parseInt(document.getElementById("popup-menu").dataset.columnIndex);
    var table, rows, switching, i, shouldSwitch;
    table = document.getElementById("posts-table");
    switching = true;
    while (switching) {
        switching = false;
        rows = table.getElementsByTagName("tr");
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            var x = rows[i].getElementsByTagName("td")[columnIndex];
            var y = rows[i + 1].getElementsByTagName("td")[columnIndex];
            
            if (columnIndex === 0 || columnIndex === 1) { // Treat as integers
                var xInt = parseInt(x.innerHTML);
                var yInt = parseInt(y.innerHTML);
                if (order === 'asc') {
                    if (xInt > yInt) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (order === 'desc') {
                    if (xInt < yInt) {
                        shouldSwitch = true;
                        break;
                    }
                }
            } else if (columnIndex === 2 || columnIndex === 3) { // Treat as strings
                if (order === 'asc') {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (order === 'desc') {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
            } else if (columnIndex === 4 || columnIndex === 5) { // Treat as datetime
                var xDateTime = parseDateTime(x.innerHTML);
                var yDateTime = parseDateTime(y.innerHTML);
                if (order === 'asc') {
                    if (xDateTime > yDateTime) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (order === 'desc') {
                    if (xDateTime < yDateTime) {
                        shouldSwitch = true;
                        break;
                    }
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }

    document.getElementById("popup-menu").style.display = 'none'; // Hide the pop-up menu after sorting
}

// Function to show tooltip when hovering over th elements
document.querySelectorAll('#posts-table th').forEach(th => {
    th.addEventListener('mouseover', (e) => {
        var tooltip = document.getElementById("tooltip");
        tooltip.innerText = "Right-click to filter"; // Get the text content of h1 inside th
        tooltip.style.display = 'block';
        tooltip.style.left = (e.pageX + 10) + 'px'; // Position the tooltip next to the mouse cursor
        tooltip.style.top = (e.pageY + 10) + 'px';
    });
    th.addEventListener('mouseout', () => {
        var tooltip = document.getElementById("tooltip");
        tooltip.style.display = 'none'; // Hide the tooltip when mouse leaves th
    });
});
