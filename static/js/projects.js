var selected = null;

function showAddProjectForm()
{
    var formContainer = document.getElementById("addProjectFormContainer");
    formContainer.style.display = "flex";
}

// Display and populate the Edit form with the selected entry.
function showEditProjectForm()
{
    var formContainer = document.getElementById("editProjectFormContainer");
    formContainer.style.display = "flex";
    document.getElementById("editProjectFormIDInput").value = selected.getAttribute("projectID");
    document.getElementById("editProjectFormNameInput").value = selected.getAttribute("projectName");
    document.getElementById("editProjectFormDescriptionInput").value = selected.getAttribute("projectDescription");
}

// Display and populate the Delete form with the selected entry.
function showRemoveProjectForm()
{
    var formContainer = document.getElementById("removeProjectFormContainer");
    formContainer.style.display = "flex";
    document.getElementById("removeProjectFormIDInput").value = selected.getAttribute("projectID");
    document.getElementById("removeProjectFormNameInput").value = selected.getAttribute("projectName");
}

function hideForm(form)
{
    form.style.display = "none";
}

// Saves an entry into the 'selected' variable as well as
// alters its background color to signify selection.
function select(element) {
    if (selected === element) {
        deselect(element);
        return;
    }

    if (selected) deselect(selected);
    selected = element;
    element.style.backgroundColor = "rgba(255, 255, 255, 0.2)";
    document.getElementById("editProjectButton").disabled = false;
    document.getElementById("removeProjectButton").disabled = false;
}

function deselect(element) {
    selected = null;
    element.style.backgroundColor = "";
    document.getElementById("editProjectButton").disabled = true;
    document.getElementById("removeProjectButton").disabled = true;
}

// Receive all project entries from backend, and while containerizing,
// populate the projects container/list.
function populateProjects(projects)
{
    const projectsContainer = document.getElementById("projectsContainer");
    for (const [key, val] of Object.entries(projects)) 
    {
        const entry = document.createElement("div"); entry.className = "projectEntry";
        const header = document.createElement("span"); header.className = "projectEntryHeader";
        const name = document.createElement("h3"); name.className = "projectEntryName";
        const ID = document.createElement("p"); ID.className = "projectEntryID";
        const description = document.createElement("p"); description.className = "projectEntryDescription";

        name.textContent = val["project_name"];
        description.textContent = val["project_description"];
        ID.textContent = key;

        header.appendChild(name);
        header.appendChild(ID);
        entry.appendChild(header);
        entry.appendChild(description);
        projectsContainer.appendChild(entry);

        entry.onclick = function() {select(entry)};
        entry.setAttribute("projectID", key);
        entry.setAttribute("projectName", val["project_name"]);
        entry.setAttribute("projectDescription", val["project_description"]);
    }
}