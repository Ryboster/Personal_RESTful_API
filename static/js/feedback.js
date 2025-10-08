// Receive all feedback entries from the backend,
// and while containerizing each item, populate the
// feedbacks container
function populateFeedbacks(feedbacks)
{
    for (const [key, val] of Object.entries(feedbacks))
    {
        const container = document.createElement("div");
        const topBar = document.createElement("span");
        const ID = document.createElement("p");
        const author = document.createElement("h3");
        const feedback = document.createElement("p");

        ID.textContent = key;
        author.textContent = val["author"];
        feedback.textContent = val["feedback"];
        
        topBar.appendChild(author);
        topBar.appendChild(ID);
        container.appendChild(topBar);
        container.appendChild(feedback);

        document.getElementById("feedbacksContainer").appendChild(container);
    }
}

function showSubmitFeedbackForm()
{
    document.getElementById("submitFeedbackFormContainer").style.display = "flex";
}