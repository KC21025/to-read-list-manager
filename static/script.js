const modal = document.getElementById('bookModal'); // Get modal element
const button = document .getElementById('openModal'); // Get button element to open modal
const span = document.getElementsByClassName('close')[0]; // Get span element to close modal
const bookItems = document.querySelectorAll('li[data-id]'); // Getting all book items with data-id attribute for displaying book details

button.onclick = function() {
    modal.style.display = 'block'; // When button is clicked, display modal
}

span.onclick = function() {
    modal.style.display = 'none'; // When span is cliked, hide modal
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none'; // When user clicks out of modal, hide modal
    }
}

for (let item of bookItems) { // Looping through each book item, adding click event listener to display book
    item.onclick = function() { // On click
        const bookId = this.getAttribute('data-id');
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
                    '<form id="editBookForm" method="POST" action="/edit_book/' + bookId + '">' +
                    '<input type="text" name="title" placeholder="Title" value="' + data.book.Title + '" required><br>' +
                    '<input type="text" name="author" placeholder="Author" value="' + data.book.Author_Name + '" required><br>' +
                    '<select name="status" required>' +
                    '<option value="">Select Status</option>' +
                    '<option value="1" ' + (data.book.Status_ID == 1 ? 'selected' : '') + '>Reading</option>' +
                    '<option value="2" ' + (data.book.Status_ID == 2 ? 'selected' : '') + '>Completed</option>' +
                    '<option value="3" ' + (data.book.Status_ID == 3 ? 'selected' : '') + '>To Read</option>' +
                    '</select><br>' +
                    '<input type="number" name="pages_read" placeholder="Pages Read" value="' + data.book.Pages_Read + '" min="0"><br>' +
                    '<input type="number" name="total_pages" placeholder="Total Pages" value="' + data.book.Total_Pages + '" min="1"><br>' +
                    '<input type="number" name="rating" placeholder="Rating (1-5)" value="' + data.book.Rating + '" min="1" max="5"><br>' +
                    '<input type="date" name="date_started" placeholder="Date Started" value="' + data.book.Date_Started + '"><br>' +
                    '<input type="date" name="date_finished" placeholder="Date Finished" value="' + data.book.Date_Finished + '"><br>' +
                    '<input type="text" name="description" placeholder="Description" value="' + (data.book.Book_Description || '') + '"><br>' +
                    '<button type="submit">Save Changes</button></form></div>' +
                    '<button id="deleteBtn">Delete</button>';

                const deleteButton = document.getElementById("deleteBtn");
                deleteButton.onclick = function() { // On click of delete button, delete and POST request to delete_book route in app.py with book ID as parameter, and confirm before deletion
                    if (confirm("Are you sure you want to delete this book?")) {
                        fetch('/delete_book/' + bookId, {method: "POST"})
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

