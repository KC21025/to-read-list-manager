const modal = document.getElementById('bookModal');
const button = document .getElementById('openModal');
const span = document.getElementsByClassName('close')[0];
const bookItems = document.querySelectorAll('li[data-id]'); 

button.onclick = function() {
    modal.style.display = 'block';
}

span.onclick = function() {
    modal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

for (let item of bookItems) {
    item.onclick = function() {
        const bookId = this.getAttribute('data-id');
        fetch('/get_book/' + bookId)
            .then(response => response.json())
            .then(data => {
                const display = document.getElementById('bookDisplay');

                display.innerHTML = '<h2>' + data.book.Title + '</h2>' +
                    '<p><strong>Author:</strong> ' + data.book.Author_Name + '</p>' +
                    '<p><strong>Status:</strong> ' + data.book.Status_Name + '</p>' +
                    '<p><strong>Progress:</strong> ' + data.book.Pages_Read + '/' + data.book.Total_Pages + ' pages</p>' +
                    '<p><strong>Rating:</strong>' + data.book.Rating + '/' + '5</p>' + 
                    '<button id="editBtn">Edit</button>' +
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
                    '<input type="text" name="description" placeholder="Description" value="' + (data.book.Book_Description || '') + '"><br>' +
                    '<button type="submit">Save Changes</button></form></div>' +
                    '<button id="deleteBtn">Delete</button>';

                const deleteButton = document.getElementById("deleteBtn");
                deleteButton.onclick = function() {
                    if (confirm("Are you sure you want to delete this book?")) {
                        fetch('/delete_book/' + bookId, {method: "POST"})
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    alert("Book deleted successfully!");
                                    location.reload();
                                }
                            });
                    }
                };

                const editButton = document.getElementById("editBtn");
                const editForm = document.getElementById("editForm");
                const closeEditForm = document.getElementsByClassName("closeEditForm")[0];
                closeEditForm.onclick = function() {
                    editForm.style.display = "none";
                };
                editButton.onclick = function() {
                    editForm.style.display = "block";
                };
            })
    }}

