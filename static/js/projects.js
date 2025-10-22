var selected = null;

// Receive all project entries from backend, and while containerizing,
// populate the projects container/list.
function populateProjects(projects)
{
    const container = document.getElementById("contentContainer");
    for (const [key, val] of Object.entries(projects)) 
    {
        const entry = document.createElement("div"); entry.className = "entry";
        const header = document.createElement("span"); header.className = "entryHeader";
        const project_URL = document.createElement("a");
        const name = document.createElement("h3");
        const ID = document.createElement("p");
        const description = document.createElement("p");

        project_URL.href = "/projects/" + key;

        name.textContent = val["project_name"];
        description.textContent = val["project_description"];
        ID.textContent = key;

        project_URL.appendChild(name);
        header.appendChild(project_URL);
        header.appendChild(ID);
        entry.appendChild(header);
        entry.appendChild(description);
        
        entry.onclick = function() {select(entry)};
        entry.setAttribute("entryID", key);
        entry.setAttribute("entryName", val["project_name"]);
        entry.setAttribute("entryDescription", val["project_description"]);
        container.appendChild(entry);
    }
}

function populateEditForm()
{
    if (!selected) return;
    document.getElementById("editFormIDInput").value = selected.getAttribute("entryID");
    document.getElementById("editFormNameInput").value = selected.getAttribute("entryName");
    document.getElementById("editFormDescriptionInput").value = selected.getAttribute("entryDescription");
}

function populateDeleteForm()
{
    if (!selected) return;
    document.getElementById("deleteFormIDInput").value = selected.getAttribute("entryID");
    document.getElementById("deleteFormNameInput").value = selected.getAttribute("entryName");
}

document.addEventListener("DOMContentLoaded", function() {
    const editButton = document.getElementById("editEntryButton");
    const deleteButton = document.getElementById("deleteEntryButton");
    editButton.addEventListener("click", populateEditForm)
    deleteButton.addEventListener("click", populateDeleteForm)
});