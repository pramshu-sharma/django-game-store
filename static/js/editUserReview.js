document.addEventListener('DOMContentLoaded', function() {
    let editLink = document.getElementById('edit-user-review')

    if (editLink) {
        editLink.addEventListener('click', function(event) {
            let dataReviewID = this.parentElement.getAttribute('data-review-id')
            let postURL = this.parentElement.getAttribute('data-post-url')
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            event.preventDefault()
            editReview(dataReviewID, postURL, csrfToken)
        })
    }
})

function editReview(dataReviewID, postURL, csrfToken) {
    let reviewSpan = document.getElementById('user-review')
    let reviewText = reviewSpan.textContent.replace('Edit', '')
    reviewSpan.innerHTML = ''

    let editReviewTextArea = document.createElement('textarea')
    editReviewTextArea.cols = 20
    editReviewTextArea.rows = 3
    editReviewTextArea.textContent = reviewText

    let saveButton = document.createElement('a')
    saveButton.id = 'save-user-review'
    saveButton.textContent = 'Save'
    saveButton.href = '#'

    reviewSpan.appendChild(editReviewTextArea)
    reviewSpan.appendChild(saveButton)

    saveButton.addEventListener('click', function(event) {
        event.preventDefault()
        let newReview = reviewSpan.querySelector('textarea').value
        
        fetch(postURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({'id': dataReviewID, 'review': newReview})
        })
        .then(response => response.json())
        .then(data => console.log(data))

        editReviewTextArea.remove()
        saveButton.remove()

        let editButton = document.createElement('a')
        editButton.id = 'edit-user-review'
        editButton.className = 'edit-link'
        editButton.href = '#'
        editButton.textContent = 'Edit'

        editButton.addEventListener('click', function(event) {
            event.preventDefault()
            editReview(dataReviewID, postURL, csrfToken)
        })

        reviewSpan.textContent = newReview
        reviewSpan.appendChild(editButton)
    })
}

