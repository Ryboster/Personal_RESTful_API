function populateCollaborators(collaborators)
{
    const container = document.getElementById("contentContainer");
    for (const [key, val] of Object.entries(collaborators))
    {
        const entry = document.createElement("div"); entry.className = "entry";
        const header = document.createElement("span"); header.className = "entryHeader";
        const name = document.createElement("h3");
        const ID = document.createElement("p");
        const Role = document.createElement("p");
        const Social = document.createElement("p");

        name.textContent = val["Name"];
        Role.textContent = val["Role"];
        Social.textContent = val["Social_URL"];
        ID.textContent = key;

        header.appendChild(name);
        header.appendChild(ID);
        entry.appendChild(header);
        entry.appendChild(Role);
        entry.appendChild(Social);
        container.appendChild(entry);

        entry.onclick = function() {select(entry)};
        entry.setAttribute("entryID", key);
        entry.setAttribute("entryName", val["Name"]);
        entry.setAttribute("entryRole", val["Role"]);
        entry.setAttribute("entrySocial", val["Social_URL"])
    }
}

function populateEditForm()
{
    if (!selected) return;
    document.getElementById("editFormIDInput").value = selected.getAttribute("entryID");
    document.getElementById("editFormNameInput").value = selected.getAttribute("entryName");
    document.getElementById("editFormRoleInput").value = selected.getAttribute("entryRole");
    document.getElementById("editFormSocialInput").value = selected.getAttribute("entrySocial");
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