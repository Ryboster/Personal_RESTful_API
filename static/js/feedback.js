// Receive all feedback entries from the backend,
// and while containerizing each item, populate the
// feedbacks container
function populateFeedbacks(feedbacks)
{
    const container = document.getElementById("contentContainer");
    for (const [key, val] of Object.entries(feedbacks))
    {
        const entry = document.createElement("div"); entry.className = "entry";
        const header = document.createElement("span"); header.className = "entryHeader";
        const ID = document.createElement("p");
        const author = document.createElement("h3");
        const feedback = document.createElement("p");

        ID.textContent = key;
        author.textContent = val["author"];
        feedback.textContent = val["feedback"];
        
        header.appendChild(author);
        header.appendChild(ID);
        entry.appendChild(header);
        entry.appendChild(feedback);

        entry.onclick = function() {select(entry);}
        entry.setAttribute("entryID", key);
        entry.setAttribute("entryAuthor", val["author"]);
        entry.setAttribute("entryFeedback", val["feedback"]);
        container.appendChild(entry);
    }
}


//function populateEditForm()
//{
//    if (!selected) return;
//    document.getElementById("editFormIDInput").value = selected.getAttribute("entryID");
//    document.getElementById("editFormNameInput").value = selected.getAttribute("entryName");
//    document.getElementById("editFormDescriptionInput").value = selected.getAttribute("entryDescription");
//}

function populateDeleteForm()
{
    if (!selected) return;
    document.getElementById("deleteFormIDInput").value = selected.getAttribute("entryID");
    document.getElementById("deleteFormAuthorInput").value = selected.getAttribute("entryAuthor");
    document.getElementById("deleteFormFeedbackInput").value = selected.getAttribute("entryFeedback");
}

document.addEventListener("DOMContentLoaded", function() {
    const editButton = document.getElementById("editEntryButton");
    const deleteButton = document.getElementById("deleteEntryButton");
    //editButton.addEventListener("click", populateEditForm)
    deleteButton.addEventListener("click", populateDeleteForm)
});