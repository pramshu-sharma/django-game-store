document.addEventListener('DOMContentLoaded', function() {
    let editLink = document.getElementById('edit-user-review')

    if (editLink) {
        editLink.addEventListener('click', function(event) {
            let dataReviewID = this.parentElement.getAttribute('data-review-id')
            let postURL = this.parentElement.getAttribute('data-post-url')
            
            event.preventDefault()
            editReview(dataReviewID, postURL)
        })
    }
})

function editReview(dataReviewID, postURL) {
    console.log('{{ csrf_token }}')
    let reviewSpan = document.getElementById('user-review')
    let reviewText = reviewSpan.textContent.replace('Edit', '')
    reviewSpan.innerHTML = ''

    let editReviewTextArea = document.createElement('textarea')
    editReviewTextArea.cols = 20
    editReviewTextArea.rows = 3
    editReviewTextArea.textContent = reviewText

    let saveButton = document.createElement('button')
    saveButton.id = 'save-user-review'
    saveButton.name = 'action'
    saveButton.value = 'save-user-review'
    saveButton.textContent = 'Save'

    reviewSpan.appendChild(editReviewTextArea)
    reviewSpan.appendChild(saveButton)

    saveButton.addEventListener('click', function(event) {
        event.preventDefault()
        let newReview = reviewSpan.querySelector('textarea').value
        
        fetch(postURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
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
            editReview(dataReviewID, postURL)
        })

        reviewSpan.textContent = newReview
        reviewSpan.appendChild(editButton)
    })
}