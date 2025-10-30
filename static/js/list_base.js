var selected;
function showAddForm()
{
    const container = document.getElementById("addFormContainer");
    container.style.display = "flex";
}

function showEditForm()
{
    const container = document.getElementById("editFormContainer");
    container.style.display = "flex";
}

function showDeleteForm()
{
    const container = document.getElementById("deleteFormContainer");
    container.style.display = "flex";
}

function select(element) {
    if (selected === element) {
        deselect(element);
        return;
    }

    if (selected) deselect(selected);
    selected = element;
    element.style.backgroundColor = "rgba(255, 255, 255, 0.2)";
    if (document.getElementById('editEntryButton') != null) 
    {
        document.getElementById("editEntryButton").disabled = false;
    }
    if (document.getElementById("deleteEntryButton") != null)
    {
        document.getElementById("deleteEntryButton").disabled = false;
    }
}

function deselect(element) {
    selected = null;
    element.style.backgroundColor = "";
    if (document.getElementById('editEntryButton') != null) 
    {
        document.getElementById("editEntryButton").disabled = true;
    }
    if (document.getElementById("deleteEntryButton") != null)
    {
        document.getElementById("deleteEntryButton").disabled = true;
    }
}