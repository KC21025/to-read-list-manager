const modal = document.getElementById('bookModal'); // Get modal element
const button = document.getElementById('openModal'); // Get button element to open modal
const span = document.getElementsByClassName('close')[0]; // Get span element to close modal
const bookItems = document.querySelectorAll('li[manage-data-id]'); // Getting all book items with data-id attribute for displaying book details in the manage page
const bookDescription = document.querySelectorAll('li[home-data-id]') // Getting all book items with data-id attribute for displaying book description in the home page

if (button) { // Check if button exists
    button.onclick = function() {
        modal.style.display = 'block'; // When button is clicked, display modal
    }
}

if (span) { // Checks if span exists
    span.onclick = function() {
        modal.style.display = 'none'; // When span is cliked, hide modal
    }
}

if (modal) { // Checks if modal exists
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none'; // When user clicks out of modal, hide modal
        }
    }
}

for (let item of bookItems) { // Looping through each book item, adding click event listener to display book
    item.onclick = function() { // On click
        const bookId = this.getAttribute('manage-data-id'); // Get book ID from data-id attribute of the clicked book item
        fetch('/get_book/' + bookId) // Fetch book details from app.py using book ID from data-id attribute
            .then(response => response.json()) // Convert response to JSON
            .then(data => { // Display book details in the modal
                const display = document.getElementById('bookDisplay');

                display.innerHTML = '<h2>' + data.book.Title + '</h2>' +
                    '<p><strong>Author:</strong> ' + data.book.Author_Name + '</p>' +
                    '<p><strong>Status:</strong> ' + data.book.Status_Name + '</p>' +
                    '<p><strong>Progress:</strong> ' + data.book.Pages_Read + '/' + data.book.Total_Pages + ' pages</p>' +
                    '<p><strong>Rating:</strong>' + data.book.Rating + '/' + '5</p>' + 
                    '<button id="editBtn">Edit</button>' +
                    // Form for editing book details, prefilled with current book details, and button to submit the form to edit_book route in app.py with book ID as a parameter
                    '<div id="editForm" style="display:none;">' + 
                    '<span class="closeEditForm">&times;</span>' +
                    '<form id="editBookForm" method="POST" action="/edit_book/' + bookId + '">' + '<p class = "inline-p"> *Book Title: </p>' +
                    '<input type="text" name="title" placeholder="Title" value="' + data.book.Title + '" required><br>' + '<p class = "inline-p"> *Author Name: </p>' +
                    '<input type="text" name="author" placeholder="Author" value="' + data.book.Author_Name + '" required><br>' + '<p class = "inline-p"> *Status: </p>' +
                    '<select name="status">' +
                    '<option value="">Select Status</option>' +
                    '<option value="1" ' + (data.book.Status_ID == 1 ? 'selected' : '') + '>Reading</option>' +
                    '<option value="2" ' + (data.book.Status_ID == 2 ? 'selected' : '') + '>Completed</option>' +
                    '<option value="3" ' + (data.book.Status_ID == 3 ? 'selected' : '') + '>To Read</option>' +
                    '</select><br>' + '<p class = "inline-p"> Pages Read: </p>' +
                    '<input type="number" name="pages_read" placeholder="Pages Read" value="' + data.book.Pages_Read + '" min="0"><br>' + '<p class = "inline-p"> Total Pages: </p>' +
                    '<input type="number" name="total_pages" placeholder="Total Pages" value="' + data.book.Total_Pages + '" min="1"><br>' + '<p class = "inline-p"> Rating: </p>' +
                    '<input type="number" name="rating" placeholder="Rating (1-5)" value="' + data.book.Rating + '" min="1" max="5"><br>' + '<p class = "inline-p"> Date Started: </p>' +
                    '<input type="date" name="date_started" placeholder="Date Started" value="' + data.book.Date_Started + '"><br>' + '<p class = "inline-p"> Date Finished: </p>' +
                    '<input type="date" name="date_finished" placeholder="Date Finished" value="' + data.book.Date_Finished + '"><br>' + '<p class = "inline-p"> Book Description: </p>' +
                    '<input type="text" name="description" placeholder="Description" value="' + (data.book.Book_Description || '') + '"><br>' +
                    '<button type="submit">Save Changes</button></form></div>' +
                    '<button id="deleteBtn">Delete</button>';

                const deleteButton = document.getElementById("deleteBtn");
                deleteButton.onclick = function() { // On click of delete button, delete and POST request to delete_book route in app.py with book ID as parameter, and confirm before deletion
                    if (confirm("Are you sure you want to delete this book?")) {
                        fetch('/delete_book/' + bookId, {method: "POST"}) // Send POST request to delete_book route in app.py with the book ID as a parameter to delete it from the database
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) { // If delete successful, alert user and reload page
                                    alert("Book deleted successfully!");
                                    location.reload();
                                }
                            });
                    }
                };

                const editButton = document.getElementById("editBtn"); // Get edit button element
                const editForm = document.getElementById("editForm"); // Get edit form element
                const closeEditForm = document.getElementsByClassName("closeEditForm")[0]; // Get span to close edit form
                closeEditForm.onclick = function() {
                    editForm.style.display = "none"; // On click of span, hide edit form
                };
                editButton.onclick = function() {
                    editForm.style.display = "block"; // On click of edit button, display edit form
                };
            })
    }}

for (let item of bookDescription) {
    item.onclick = function() { // On click of book item in home page, display book description
        const bookId = this.getAttribute('home-data-id'); // Gets ID from data-id attribute of the clicked book item
        fetch('/get_book/' + bookId) // Fetch book details from app.py using book ID
            .then(response => response.json()) // Convert response to JSON
            .then(data => { 
                const displayDescription = document.getElementById('BookDescriptionDisplay');
                displayDescription.innerHTML = '<p id = "home_page_book_description"><strong>Description of ' + data.book.Title + ': </strong>'  + (data.book.Book_Description || 'No description available.') + '</p>';
            })
}}


const goalCanvas = document.getElementById('goal_chart'); // Gets the goal chart
if (goalCanvas) { // If goal chart exists
    const readCount = goalCanvas.getAttribute('data-read'); // Gets book read count
    const goalCount = goalCanvas.getAttribute('data-goal'); // Gets goal count
    
    new Chart(goalCanvas, {
        type: 'bar',
        data: {
            labels: ['Books Read', 'Goal'],
            datasets: [{
                label: 'Reading progress',
                data: [readCount, goalCount],
                backgroundColor: ['#36a2eb', '#3df500']
            }]
        },
     options: {
            responsive: true, // So it can shrink when window shrinks
            maintainAspectRatio: false, // To fit inside the div
            scales: {
                y: { beginAtZero: true } // Ensures the chart starts at 0
            }
        }
    });
}

