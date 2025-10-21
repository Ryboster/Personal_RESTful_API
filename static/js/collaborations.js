function populateCollaborations(projects)
{
    const container = document.getElementById("contentContainer");
    for (const [key,val] of Object.entries(projects))
    {
        const entry = document.createElement("div"); entry.className = "entry";
        const header = document.createElement("span"); header.className = "entryHeader";
        const name = document.createElement("h3"); name.className = "entryName";
        const ID = document.createElement("p"); ID.className = "entryID";
        const description = document.createElement("p"); description.className = "entryDescription";

        name.textContent = val["Name"];
        description.textContent = val["Description"];
        ID.textContent = key;

        header.appendChild(name);
        header.appendChild(ID);
        entry.appendChild(header);
        entry.appendChild(description);
        container.appendChild(entry);

        entry.onclick = function() {select(entry)};
        entry.setAttribute("entryID", key);
        entry.setAttribute("entryName", val["Name"]);
        entry.setAttribute("entryDescription", val["Description"]);
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